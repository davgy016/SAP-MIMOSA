using Microsoft.AspNetCore.Mvc;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Collections.Generic;
using SAP_MIMOSAapp.Models;
using System.Net.Http.Json;

namespace SAP_MIMOSAapp.Controllers
{
    public class HomeController : Controller
    {
        private readonly HttpClient _httpClient;
        private readonly ILogger<HomeController> _logger;

        public HomeController(IHttpClientFactory httpClientFactory, ILogger<HomeController> logger)
        {
            //set a base address for all requests
            //Avoid creating new HttpClient instances for each request
            _httpClient = httpClientFactory.CreateClient();
            _httpClient.BaseAddress = new Uri("http://127.0.0.1:8000/");
            _httpClient.Timeout = TimeSpan.FromMinutes(5); 
            _logger = logger;
        }

        public async Task<IActionResult> Index(SearchViewModel model)
        {
            var documents = new List<MappingDocument>();

            try
            {
                // Use ViewModel method to set LLMTypes with selected value
                model.SetLLMTypes(model.SelectedLLM);

                // Search by Entity Name or LLM type
                if (!string.IsNullOrEmpty(model.SearchByEntityName) || !string.IsNullOrEmpty(model.SearchByLLM))
                {
                    var response = await _httpClient.GetStringAsync("workorders");
                    var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                    documents = JsonSerializer.Deserialize<List<MappingDocument>>(response, options) ?? new List<MappingDocument>();

                    model.TotalDocuments = documents.Count;

                    if (!string.IsNullOrEmpty(model.SearchByEntityName))
                    {
                        documents = documents
                            .Where(d => d.mappings.Any(m =>
                                m.sap.entityName.Contains(model.SearchByEntityName, System.StringComparison.OrdinalIgnoreCase) ||
                                m.mimosa.entityName.Contains(model.SearchByEntityName, System.StringComparison.OrdinalIgnoreCase)))
                            .ToList();
                    }
                    else if (!string.IsNullOrEmpty(model.SearchByLLM))
                    {
                        documents = documents
                            .Where(d => d.LLMType.Contains(model.SearchByLLM, System.StringComparison.OrdinalIgnoreCase))
                            .ToList();
                    }

                    model.FilteredCount = documents.Count;
                    model.SearchResults = documents;
                }

                else if (!string.IsNullOrEmpty(model.Query))
                {
                    var aiResponse = await GetAIResponse(model.Query, model.SelectedLLM, null);
                    //_logger.LogInformation("AI raw response: {AIResponse}", aiResponse);
                    //Console.WriteLine("AI raw response: " + aiResponse);
                    if (!string.IsNullOrWhiteSpace(aiResponse))
                    {
                        try
                        {
                            var parseResponse = JsonSerializer.Deserialize<MappingDocument>(aiResponse, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                            if (parseResponse != null)
                            {
                                //parseResponse = await CheckAccuracy(parseResponse);
                                SaveMappingTempFile(parseResponse);
                                return RedirectToAction("Create");
                            }
                            else
                            {
                                ViewBag.ErrorMessage = "AI did not return a valid mapping document.";
                                return View(model);
                            }
                        }
                        catch (System.Text.Json.JsonException ex)
                        {
                            _logger.LogError(ex, "Failed to deserialize AI mapping response");
                            ViewBag.ErrorMessage = "AI returned an invalid mapping format.";
                            return View(model);
                        }
                    }
                    else
                    {
                        ViewBag.ErrorMessage = "AI did not return a valid mapping (no response or invalid format).";
                        return View(model);
                    }
                }
                else
                {
                    model.SearchResults = new List<MappingDocument>();
                    model.FilteredCount = 0;
                    model.TotalDocuments = 0;
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in Index");
                ViewBag.ErrorMessage = $"Error: {ex.Message}";
            }

            return View(model);
        }


        // Store MappingDocument in TempData
        // Save MappingDocument to temp file
        private void SaveMappingTempFile(MappingDocument doc)
        {
            var tempPath = Path.Combine(Path.GetTempPath(), "tempImportData.json");
            System.IO.File.WriteAllText(tempPath, JsonSerializer.Serialize(doc));
        }

        // Retrieve MappingDocument from TempData
        // Load MappingDocument from temp file (and delete after reading)
        private MappingDocument? LoadMappingTempFile()
        {
            var tempPath = Path.Combine(Path.GetTempPath(), "tempImportData.json");
            if (!System.IO.File.Exists(tempPath)) return null;
            try
            {
                var json = System.IO.File.ReadAllText(tempPath);
                var doc = JsonSerializer.Deserialize<MappingDocument>(json, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                System.IO.File.Delete(tempPath);
                return doc;
            }
            catch
            {
                return null;
            }
        }

        //AI Search Method
        private async Task<string> GetAIResponse(string query, string llmModel, List<MappingPair>? mappings)
        {
            try
            {
                Console.WriteLine($"GetAIResponse called with query: {query}");

                // Create the request object exactly matching the Python model
                var request = new { query = query, llm_model = llmModel, mappings = mappings ?? new List<MappingPair>() };

                // Serialize with proper casing
                var jsonOptions = new JsonSerializerOptions
                {
                    PropertyNamingPolicy = JsonNamingPolicy.CamelCase
                };
                var jsonRequest = new StringContent(
                    JsonSerializer.Serialize(request, jsonOptions),
                    Encoding.UTF8,
                    "application/json"
                );

                // Log the request for debugging
                var requestContent = await jsonRequest.ReadAsStringAsync();
                Console.WriteLine($"Sending request: {requestContent}");

                // Send the request
                var response = await _httpClient.PostAsync("ask_AI", jsonRequest);

                // Log the response status
                Console.WriteLine($"Response status: {response.StatusCode}");

                if (!response.IsSuccessStatusCode)
                {
                    var errorContent = await response.Content.ReadAsStringAsync();
                    Console.WriteLine($"Error content: {errorContent}");
                    return $"Error: AI service returned status code {response.StatusCode}. Details: {errorContent}";
                }

                // Read and log the response
                var responseString = await response.Content.ReadAsStringAsync();
                Console.WriteLine($"AI response: {responseString}");

                try
                {
                    return responseString;
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Error deserializing response: {ex.Message}");
                    return $"Raw response: {responseString}";
                }
            }
            catch (System.Exception ex)
            {
                Console.WriteLine($"Exception in GetAIResponse: {ex}");
                return $"Error: {ex.Message}";
            }
        }

        [HttpGet]
        public IActionResult Create(string? query = null, string? llmType = null)
        {
            // Try to load from temp file (imported CSV), then fall back to TempData
            MappingDocument? model = LoadMappingTempFile();
            if (model == null)
            {
                model = LoadMappingTempFile();
            }
            if (model != null)
            {

                if (query != null)
                    model.prompt = query;
                if (llmType != null)
                {
                    model.LLMType = llmType;
                }
                Console.WriteLine($"AI Mapping: {JsonSerializer.Serialize(model)}");
            }

            return View(model);
        }

        [HttpPost]
        public async Task<IActionResult> Create(MappingDocument newDocument)
        {
            if (!ModelState.IsValid)
            {
                return View(newDocument);
            }

            try
            {
                // mapID is a string for backend validation
                if (newDocument.mapID == null)
                {
                    newDocument.mapID = "";
                }
                // Ensure platform values are set correctly
                if (newDocument.mappings != null)
                {
                    foreach (var mapping in newDocument.mappings)
                    {
                        if (mapping.sap != null && string.IsNullOrEmpty(mapping.sap.platform))
                        {
                            mapping.sap.platform = "SAP";
                        }

                        if (mapping.mimosa != null && string.IsNullOrEmpty(mapping.mimosa.platform))
                        {
                            mapping.mimosa.platform = "MIMOSA";
                        }
                    }
                }

                // POST to backend to create new mapping (backend will generate mapID)
                var json = JsonSerializer.Serialize(newDocument);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var createResponse = await _httpClient.PostAsync("workorders", content);
                var responseText = await createResponse.Content.ReadAsStringAsync();

                if (!createResponse.IsSuccessStatusCode)
                {
                    ViewBag.ErrorMessage = $"Error creating record: {createResponse.StatusCode} - {responseText}";
                    return View(newDocument);
                }

                // Get the created mapping with mapID from backend response
                var createdDoc = JsonSerializer.Deserialize<MappingDocument>(responseText, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

                TempData["SuccessMessage"] = $"Mapping with #ID {createdDoc?.mapID} created successfully!";
                return RedirectToAction("Index");
            }
            catch (System.Exception ex)
            {
                ViewBag.ErrorMessage = $"Error creating record: {ex.Message}";
                return View(newDocument);
            }
        }

        public async Task<IActionResult> Edit(string id)
        {
            try
            {
                var response = await _httpClient.GetStringAsync("workorders");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var documents = JsonSerializer.Deserialize<List<MappingDocument>>(response, options);

                if (documents == null)
                {
                    return NotFound();
                }

                var document = documents.FirstOrDefault(d => d.mapID == id);
                if (document == null)
                {
                    return NotFound();
                }

                return View(document);
            }
            catch (System.Exception ex)
            {
                ViewBag.ErrorMessage = $"Error: {ex.Message}";
                return RedirectToAction("Index");
            }
        }

        [HttpPost]
        public async Task<IActionResult> Edit(MappingDocument updatedDocument)
        {
            if (!ModelState.IsValid)
            {
                return View(updatedDocument);
            }

            try
            {
                var response = await _httpClient.GetStringAsync("workorders");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var documents = JsonSerializer.Deserialize<List<MappingDocument>>(response, options);

                if (documents == null)
                {
                    ViewBag.ErrorMessage = "Mapping documents not found";
                    return View(updatedDocument);
                }

                var documentIndex = documents.FindIndex(d => d.mapID == updatedDocument.mapID);
                if (documentIndex == -1)
                {
                    ViewBag.ErrorMessage = "Mapping document not found";
                    return View(updatedDocument);
                }


                // Ensure platform values are set correctly
                if (updatedDocument.mappings != null)
                {
                    foreach (var mapping in updatedDocument.mappings)
                    {
                        if (mapping.sap != null && string.IsNullOrEmpty(mapping.sap.platform))
                        {
                            mapping.sap.platform = "SAP";
                        }

                        if (mapping.mimosa != null && string.IsNullOrEmpty(mapping.mimosa.platform))
                        {
                            mapping.mimosa.platform = "MIMOSA";
                        }
                    }
                }

                // Update the document
                documents[documentIndex] = updatedDocument;

                // Save the updated documents
                var json = JsonSerializer.Serialize(documents);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var updateResponse = await _httpClient.PutAsync("workorders", content);
                updateResponse.EnsureSuccessStatusCode();

                TempData["SuccessMessage"] = $"Mapping with #ID {updatedDocument.mapID} updated successfully!";

                return RedirectToAction("Index");
            }
            catch (System.Exception ex)
            {
                ViewBag.ErrorMessage = $"Error updating record: {ex.Message}";
                return View(updatedDocument);
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(string id)
        {
            try
            {
                var deleteResponse = await _httpClient.DeleteAsync($"workorders/{id}");
                if (!deleteResponse.IsSuccessStatusCode)
                {
                    var error = await deleteResponse.Content.ReadAsStringAsync();
                    return Json(new { success = false, message = $"Error deleting record: {error}" });
                }

                return Json(new { success = true, message = "Mapping deleted successfully!" });
            }
            catch (System.Exception ex)
            {
                return Json(new { success = false, message = $"Error deleting record: {ex.Message}" });
            }
        }

        //// check accuracy of a mapping
        //private async Task<MappingDocument> CheckAccuracy(MappingDocument document)
        //{
        //    try
        //    {
        //        var mappingQuery = new List<MappingDocument> { document };                

        //        var jsonRequest = new StringContent(JsonSerializer.Serialize(mappingQuery), Encoding.UTF8, "application/json");

        //        // Send the request to check accuracy
        //        var response = await _httpClient.PostAsync("check_accuracy", jsonRequest);

        //        if (!response.IsSuccessStatusCode)
        //        {
        //            _logger.LogError($"Error checking accuracy: {response.StatusCode}");
        //            return document;
        //        }

        //        // Parse the response
        //        var responseContent = await response.Content.ReadAsStringAsync();
        //        var accuracyResult = JsonSerializer.Deserialize<AccuracyResult>(responseContent);

        //        if (accuracyResult != null)
        //        {                    
        //            document.accuracyRate = accuracyResult.accuracy_score;
        //            document.qualityRate = accuracyResult.quality_score;
        //            document.matchingRate = accuracyResult.matching_score;
        //        }

        //        return document;
        //    }
        //    catch (Exception ex)
        //    {
        //        _logger.LogError(ex, "Error checking accuracy");
        //        return document;
        //    }
        //}

        // Class to deserialize accuracy response
        //private class AccuracyResult
        //{
        //    public float accuracy_score { get; set; }
        //    public float quality_score { get; set; }
        //    public float matching_score { get; set; }            
        //}

        // --- AJAX endpoint for AI Assistant in Create view ---
        [HttpPost]
        public async Task<IActionResult> AskAI([FromBody] AskAIRequest req)
        {
            if (string.IsNullOrWhiteSpace(req?.prompt) || string.IsNullOrWhiteSpace(req?.llmType))
                return Json(new { success = false, message = "Prompt and LLM Type are required." });
            try
            {
                if (req.mappings != null && req.mappings.Any())
                {
                    Console.WriteLine("mappings passed");
                }
                else
                {
                    Console.WriteLine("no mappings passed");
                }
                var aiResponse = await GetAIResponse(req.prompt, req.llmType, req.mappings);
                if (!string.IsNullOrWhiteSpace(aiResponse))
                {
                    try
                    {
                        var parseResponse = JsonSerializer.Deserialize<MappingDocument>(aiResponse, new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
                        if (parseResponse != null)
                        {
                            SaveMappingTempFile(parseResponse);
                            return Json(new { success = true, redirectUrl = Url.Action("Create") });
                        }
                        else
                        {
                            return Json(new { success = false, message = "AI did not return a valid mapping document." });
                        }
                    }
                    catch (System.Text.Json.JsonException)
                    {
                        Console.WriteLine($"Raw AI response: {aiResponse}");
                       
                        return Json(new { success = false, message = "AI returned an invalid mapping format." });
                    }
                }
                else
                {
                    return Json(new { success = false, message = "AI did not return a valid mapping (no response or invalid format)." });
                }
            }
            catch (System.Exception ex)
            {
                return Json(new { success = false, message = $"Error communicating with AI: {ex.Message}" });
            }
        }

        public class AskAIRequest
        {
            public string prompt { get; set; }
            public string llmType { get; set; }
            public List <MappingPair>? mappings { get; set; }
        }


        [HttpPost]
        public async Task<IActionResult> ImportCsv()
        {
            try
            {
                var file = Request.Form.Files["csvFile"];
                if (file == null || file.Length == 0)
                    return BadRequest("No file uploaded.");

                var mappings = new List<MappingPair>();
                var config = new CsvHelper.Configuration.CsvConfiguration(System.Globalization.CultureInfo.InvariantCulture)
                {
                    // Ignores missing fields and header validation errors in csv
                    MissingFieldFound = null,
                    HeaderValidated = null,
                    PrepareHeaderForMatch = args => args.Header?.Trim()
                };

                using (var reader = new StreamReader(file.OpenReadStream()))
                using (var csv = new CsvHelper.CsvReader(reader, config))
                {
                    var records = csv.GetRecords<MappingPairCsvRow>().ToList();
                    foreach (var row in records)
                    {
                        var pair = new MappingPair
                        {
                            sap = new MappingField
                            {
                                entityName = row.SAP_EntityName ?? "",
                                fieldName = row.SAP_FieldName ?? "",
                                dataType = row.SAP_DataType ?? "",
                                description = row.SAP_Description ?? "",
                                fieldLength = row.SAP_FieldLength ?? "",
                                notes = row.SAP_Notes ?? ""
                            },
                            mimosa = new MappingField
                            {
                                entityName = row.MIMOSA_EntityName ?? "",
                                fieldName = row.MIMOSA_FieldName ?? "",
                                dataType = row.MIMOSA_DataType ?? "",
                                description = row.MIMOSA_Description ?? "",
                                fieldLength = row.MIMOSA_FieldLength ?? ""
                            }
                        };
                        // Only add if at least one side is filled
                        if (!string.IsNullOrWhiteSpace(pair.sap.entityName) || !string.IsNullOrWhiteSpace(pair.mimosa.entityName))
                        {
                            mappings.Add(pair);
                        }
                    }
                }
                // Store new MappingDocument with only mappings, reset all other fields
                var model = new MappingDocument { mappings = mappings };
                SaveMappingTempFile(model); // Save to temp file instead of TempData
                return Json(new { redirectUrl = Url.Action("Create") });
            }
            catch (Exception ex)
            {
                return BadRequest($"Failed to import CSV: {ex.Message}");
            }
        }


    }
}


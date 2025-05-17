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
                else
                {
                    return View(model);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in Index");
                ViewBag.ErrorMessage = $"Error: {ex.Message}";
            }

            return View(model);
        }

        // Save MappingDocument to temp file
        private void SaveMappingTempFile(MappingDocument doc)
        {
            var tempPath = Path.Combine(Path.GetTempPath(), "tempImportData.json");
            System.IO.File.WriteAllText(tempPath, JsonSerializer.Serialize(doc));
        }
        // Load MappingDocument from temp file and delete after reading
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
                model = new MappingDocument();
            }
            if (model != null)
            {

                if (query != null)
                {
                    model.prompt = query;
                }
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
            // Handle prompts posted as a single string with newlines
            if (Request.Form.ContainsKey("prompts") && Request.Form["prompts"].Count == 1)
            {
                var promptsRaw = Request.Form["prompts"].ToString();
                newDocument.prompts = promptsRaw.Split(',').Where(p => !string.IsNullOrWhiteSpace(p)).ToList();
            }

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
                // platform values set correctly
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
                var response = await _httpClient.GetStringAsync($"workorders/{id}");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var document = JsonSerializer.Deserialize<MappingDocument>(response, options);

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
                // Ensure platform values are properly set
                if (updatedDocument.mappings != null)
                {
                    foreach (var mapping in updatedDocument.mappings)
                    {
                        if (mapping.sap != null && string.IsNullOrWhiteSpace(mapping.sap.platform))
                        {
                            mapping.sap.platform = "SAP";
                        }

                        if (mapping.mimosa != null && string.IsNullOrWhiteSpace(mapping.mimosa.platform))
                        {
                            mapping.mimosa.platform = "MIMOSA";
                        }
                    }
                }

                // Send only the updated document to the correct endpoint
                var json = JsonSerializer.Serialize(updatedDocument);
                var content = new StringContent(json, Encoding.UTF8, "application/json");
                var updateResponse = await _httpClient.PutAsync($"workorders/{updatedDocument.mapID}", content);

                if (!updateResponse.IsSuccessStatusCode)
                {
                    var errorContent = await updateResponse.Content.ReadAsStringAsync();
                    ViewBag.ErrorMessage = $"Failed to update mapping: {errorContent}";
                    return View(updatedDocument);
                }

                TempData["SuccessMessage"] = $"Mapping with ID {updatedDocument.mapID} updated successfully.";
                return RedirectToAction("Index");
            }
            catch (Exception ex)
            {
                ViewBag.ErrorMessage = $"Error updating mapping: {ex.Message}";
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

        // Check accuracy of a mapping
        // Returns both overall and details as a tuple
        private async Task<(AccuracyResultViewModel? overall, List<AccuracyResultViewModel>? details)> CheckAccuracy(List<MappingPair> mappingPair)
        {
            try
            {
                var jsonRequest = new StringContent(
                    JsonSerializer.Serialize(mappingPair),
                    Encoding.UTF8,
                    "application/json"
                );

                var response = await _httpClient.PostAsync("check_accuracy", jsonRequest);
                if (!response.IsSuccessStatusCode)
                {
                    _logger.LogError($"Error checking accuracy: {response.StatusCode}");
                    return (null, null);
                }

                var responseContent = await response.Content.ReadAsStringAsync();
                // The response is: { "overall": { ... }, "details": [ {...}, {...} ] }
                using var doc = JsonDocument.Parse(responseContent);
                var root = doc.RootElement;
                AccuracyResultViewModel? overall = null;
                List<AccuracyResultViewModel>? details = null;
                if (root.TryGetProperty("overall", out var overallProp))
                {
                    overall = JsonSerializer.Deserialize<AccuracyResultViewModel>(overallProp.GetRawText());
                }
                if (root.TryGetProperty("details", out var detailsProp) && detailsProp.ValueKind == JsonValueKind.Array)
                {
                    details = JsonSerializer.Deserialize<List<AccuracyResultViewModel>>(detailsProp.GetRawText());
                }
                return (overall, details);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error checking accuracy");
                return (null, null);
            }
        }

       
        // --- Endpoint for AI Assistant in Create view ---
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
                            // Load previous prompts if any
                            parseResponse.prompts = req.prompts ?? new List<string>();

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
            public List<MappingPair>? mappings { get; set; }
            public List<string>? prompts { get; set; }
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
                                fieldLength = row.MIMOSA_FieldLength ?? "",
                                notes = row.MIMOSA_Notes ?? ""
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
                var (overall, details) = await CheckAccuracy(model.mappings);
                model.accuracyResult = overall;
                model.accuracySingleMappingPair = details;
                SaveMappingTempFile(model); 
                return Json(new { redirectUrl = Url.Action("Create") });
            }
            catch (Exception ex)
            {
                return BadRequest($"Failed to import CSV: {ex.Message}");
            }
        }


        [HttpGet]
        public async Task<IActionResult> ExportMappingCsv(string mapId)
        {
            try
            {
                // get mapping data for the given mapId
                var response = await _httpClient.GetAsync($"workorders/{mapId}");
                if (!response.IsSuccessStatusCode)
                {
                    return BadRequest("Failed to fetch mapping data.");
                }
                var json = await response.Content.ReadAsStringAsync();
                var options = new JsonSerializerOptions { PropertyNameCaseInsensitive = true };
                var mappingDoc = JsonSerializer.Deserialize<MappingDocument>(json, options);
                if (mappingDoc == null)
                {
                    return NotFound("No mapping found for the given Map ID.");
                }
                // Convert to CSV
                var csvBuilder = new StringBuilder();
                csvBuilder.AppendLine("SAP_EntityName,SAP_FieldName,SAP_Description,SAP_DataType,SAP_FieldLength,SAP_Notes,MIMOSA_EntityName,MIMOSA_FieldName,MIMOSA_Description,MIMOSA_DataType,MIMOSA_FieldLength");
                if (mappingDoc.mappings != null)
                {
                    foreach (var mapping in mappingDoc.mappings)
                    {
                        var row = string.Join(",",
                            EscapeCsv(mapping.sap?.entityName),
                            EscapeCsv(mapping.sap?.fieldName),
                            EscapeCsv(mapping.sap?.description),
                            EscapeCsv(mapping.sap?.dataType),
                            EscapeCsv(mapping.sap?.fieldLength),
                            EscapeCsv(mapping.sap?.notes),
                            EscapeCsv(mapping.mimosa?.entityName),
                            EscapeCsv(mapping.mimosa?.fieldName),
                            EscapeCsv(mapping.mimosa?.description),
                            EscapeCsv(mapping.mimosa?.dataType),
                            EscapeCsv(mapping.mimosa?.fieldLength),
                            EscapeCsv(mapping.mimosa?.notes)
                        );
                        csvBuilder.AppendLine(row);
                    }
                }
                var bytes = Encoding.UTF8.GetBytes(csvBuilder.ToString());
                var fileName = $"mapping_{mappingDoc.mappings[0].sap.entityName}_{mapId}.csv";
                return File(bytes, "text/csv", fileName);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error exporting mapping CSV");
                return BadRequest($"Error: {ex.Message}");
            }
        }

        private string EscapeCsv(string? value)
        {
            if (string.IsNullOrEmpty(value)) return "";
            if (value.Contains(",") || value.Contains("\""))
            {
                value = value.Replace("\"", "\"\"");
                return $"\"{value}\"";
            }
            return value;
        }

    }
}


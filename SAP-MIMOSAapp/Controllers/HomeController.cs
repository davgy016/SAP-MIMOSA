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
            _httpClient = httpClientFactory.CreateClient();
            _httpClient.BaseAddress = new Uri("http://127.0.0.1:5000/");
            _logger = logger;
        }

        // Work Order Management Methods
        public async Task<IActionResult> Index(string query = "")
        {
            try
            {
                // Fetch work orders from the API
                var response = await _httpClient.GetStringAsync("workorders");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var workOrders = JsonSerializer.Deserialize<List<WorkOrderMapping>>(response, options);

                // Create a SearchRequest model for AI search query
                var searchRequest = new SearchRequest { Query = query };

                // If there's a query, call OpenAI API for interaction
                if (!string.IsNullOrEmpty(query))
                {
                    var aiResponse = await GetAIResponse(query);
                    ViewBag.AIResponse = aiResponse;
                }

                // Return the view with work orders and searchRequest
                return View(new { workOrders, searchRequest });
            }
            catch (System.Exception ex)
            {
                _logger.LogError(ex, "An error occurred while processing the request.");
                return View(new { workOrders = new List<WorkOrderMapping>(), searchRequest = new SearchRequest() });
            }
        }

        // New AI Search Method
        private async Task<string> GetAIResponse(string query)
        {
            try
            {
                var request = new SearchRequest { Query = query };
                var jsonRequest = new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json");

                // Send the request to the FastAPI server for AI processing
                var response = await _httpClient.PostAsync("http://localhost:8000/ask_openai", jsonRequest);

                if (!response.IsSuccessStatusCode)
                {
                    throw new System.Exception("Error communicating with AI service");
                }

                // Read AI response and return it
                var responseString = await response.Content.ReadAsStringAsync();
                var aiResponse = JsonSerializer.Deserialize<AIResponse>(responseString);
                return aiResponse?.Response ?? "No response from AI";
            }
            catch (System.Exception ex)
            {
                return $"Error: {ex.Message}";
            }
        }

        public IActionResult Create()
        {
            return View(new WorkOrderMapping());
        }

        [HttpPost]
        public async Task<IActionResult> Create(WorkOrderMapping newWorkOrder)
        {
            if (!ModelState.IsValid)
            {
                return View(newWorkOrder);
            }

            try
            {
                var createResponse = await _httpClient.PostAsJsonAsync("workorders", newWorkOrder);
                var responseText = await createResponse.Content.ReadAsStringAsync();

                if (!createResponse.IsSuccessStatusCode)
                {
                    ViewBag.ErrorMessage = $"Error creating record: {createResponse.StatusCode} - {responseText}";
                    return View(newWorkOrder);
                }

                return RedirectToAction("Index");
            }
            catch (System.Exception ex)
            {
                ViewBag.ErrorMessage = $"Error creating record: {ex.Message}";
                return View(newWorkOrder);
            }
        }

        public async Task<IActionResult> Edit(int id)
        {
            try
            {
                var response = await _httpClient.GetStringAsync($"workorders/{id}");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var workOrder = JsonSerializer.Deserialize<WorkOrderMapping>(response, options);

                if (workOrder == null)
                {
                    return NotFound();
                }

                return View(workOrder);
            }
            catch (System.Exception ex)
            {
                ViewBag.ErrorMessage = $"Error: {ex.Message}";
                return RedirectToAction("Index");
            }
        }

        [HttpPost]
        public async Task<IActionResult> Edit(WorkOrderMapping updatedWorkOrder)
        {
            if (!ModelState.IsValid)
            {
                return View(updatedWorkOrder);
            }

            try
            {
                var existingResponse = await _httpClient.GetStringAsync($"workorders/{updatedWorkOrder.Id}");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var existingWorkOrder = JsonSerializer.Deserialize<WorkOrderMapping>(existingResponse, options);

                if (existingWorkOrder == null)
                {
                    ViewBag.ErrorMessage = "Record not found";
                    return View(updatedWorkOrder);
                }

                if (string.IsNullOrEmpty(updatedWorkOrder.Color))
                {
                    updatedWorkOrder.Color = existingWorkOrder.Color;
                }

                var json = JsonSerializer.Serialize(updatedWorkOrder);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var response = await _httpClient.PutAsync($"workorders/{updatedWorkOrder.Id}", content);
                response.EnsureSuccessStatusCode();

                return RedirectToAction("Index");
            }
            catch (System.Exception ex)
            {
                ViewBag.ErrorMessage = $"Error updating record: {ex.Message}";
                return View(updatedWorkOrder);
            }
        }

        [HttpPost]
        public async Task<IActionResult> Delete(int id)
        {
            try
            {
                var response = await _httpClient.DeleteAsync($"workorders/{id}");
                response.EnsureSuccessStatusCode();

                return RedirectToAction("Index");
            }
            catch (System.Exception ex)
            {
                TempData["ErrorMessage"] = $"Error deleting record: {ex.Message}";
                return RedirectToAction("Index");
            }
        }

        [HttpPost]
        public async Task<IActionResult> ChangeColor(int id, string color)
        {
            try
            {
                var response = await _httpClient.GetStringAsync($"workorders/{id}");
                var options = new JsonSerializerOptions
                {
                    PropertyNameCaseInsensitive = true
                };
                var workOrder = JsonSerializer.Deserialize<WorkOrderMapping>(response, options);

                if (workOrder == null)
                {
                    return Json(new { success = false, message = "Record not found" });
                }

                workOrder.Color = color;

                var json = JsonSerializer.Serialize(workOrder);
                var content = new StringContent(json, Encoding.UTF8, "application/json");

                var updateResponse = await _httpClient.PutAsync($"workorders/{id}", content);
                updateResponse.EnsureSuccessStatusCode();

                return Json(new { success = true });
            }
            catch (System.Exception ex)
            {
                return Json(new { success = false, message = $"Error updating color: {ex.Message}" });
            }
        }

        // New AI Search Method
        [HttpPost("search")]
        public async Task<IActionResult> SearchWithAI([FromBody] SearchRequest request)
        {
            if (string.IsNullOrEmpty(request.Query))
            {
                return BadRequest(new { response = "Query cannot be empty." });
            }

            var jsonRequest = new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json");

            var response = await _httpClient.PostAsync("http://localhost:8000/ask_openai", jsonRequest);
            if (!response.IsSuccessStatusCode)
            {
                return StatusCode((int)response.StatusCode, new { response = "Error with AI search" });
            }

            var aiResponse = await response.Content.ReadFromJsonAsync<AIResponse>();
            return Json(new { response = aiResponse?.Response ?? "No response from AI" });
        }
    }

    public class AIResponse
    {
        public string? Response { get; set; }
    }

    public class SearchRequest
    {
        public string? Query { get; set; }
    }
}

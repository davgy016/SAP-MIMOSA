
//  This code is not necessary anymore, this is merged with Homecontroller


//using Microsoft.AspNetCore.Mvc;
//using System.Net.Http;
//using System.Text;
//using System.Text.Json;
//using System.Threading.Tasks;

//[Route("api/[controller]")]
//[ApiController]
//public class PythonAIController : ControllerBase
//{
//    private readonly HttpClient _httpClient;

//    public PythonAIController(HttpClient httpClient)
//    {
//        _httpClient = httpClient;
//    }

//    [HttpPost("search")]
//    public async Task<IActionResult> SearchWithAI([FromBody] SearchRequest request)
//    {
//        if (string.IsNullOrEmpty(request.Query))
//        {
//            return BadRequest(new { response = "Query cannot be empty." });
//        }

//        var jsonRequest = new StringContent(JsonSerializer.Serialize(request), Encoding.UTF8, "application/json");

//        var response = await _httpClient.PostAsync("http://localhost:8000/ask_openai", jsonRequest);
//        if (!response.IsSuccessStatusCode)
//        {
//            return StatusCode((int)response.StatusCode, new { response = "Error from AI service." });
//        }

//        var jsonResponse = await response.Content.ReadAsStringAsync();
//        return Ok(JsonSerializer.Deserialize<object>(jsonResponse));
//    }
//}

//public class SearchRequest
//{
//    public string? Query { get; set; }
//}


using Microsoft.AspNetCore.Mvc.Rendering;

namespace SAP_MIMOSAapp.Models;

public class SearchViewModel
{
    // Static list of available LLMs
    public static readonly List<SelectListItem> AvailableLLMs = new List<SelectListItem>
        {
            new SelectListItem { Value = "", Text = "Select LLM" },
            new SelectListItem { Value = "gpt-4.1", Text = "GPT-4.1" },
            new SelectListItem { Value = "o4-mini", Text = "o4-mini" }
        };

    public string? SearchByEntityName { get; set; }
    public string? SearchByLLM { get; set; }
    public int TotalDocuments { get; set; }
    public int FilteredCount { get; set; }
    public List<MappingDocument> SearchResults { get; set; } = new List<MappingDocument>();

}


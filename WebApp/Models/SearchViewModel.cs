using System.Collections.Generic;

namespace SAP_MIMOSAapp.Models
{
    using Microsoft.AspNetCore.Mvc.Rendering;

using Microsoft.AspNetCore.Mvc.Rendering;

public class SearchViewModel
    {
        // Static list of available LLMs
        public static readonly List<SelectListItem> AvailableLLMs = new List<SelectListItem>
        {
            new SelectListItem { Value = "", Text = "Select LLM" },
            new SelectListItem { Value = "gpt-4.1", Text = "GPT-4.1" },
            new SelectListItem { Value = "o4-mini", Text = "o4-mini" }
        };

        public SearchViewModel()
        {
            LLMTypes = new SelectList(AvailableLLMs, "Value", "Text");
        }

        // Call this to set the selected value dynamically
        public void SetLLMTypes(string? selectedValue)
        {
            LLMTypes = new SelectList(AvailableLLMs, "Value", "Text", selectedValue);
        }
        public string? AIResponse { get; set; }
        public string? SearchByEntityName { get; set; }
        public string? SearchByLLM { get; set; }
        public int TotalDocuments { get; set; }
        public int FilteredCount { get; set; }
        public List<MappingDocument> SearchResults { get; set; } = new List<MappingDocument>();
        public string? Query { get; set; }
        public string? SelectedLLM { get; set; }
        public SelectList? LLMTypes { get; set; }
    }
}

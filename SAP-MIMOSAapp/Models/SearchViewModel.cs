using System.Collections.Generic;

namespace SAP_MIMOSAapp.Models
{
    public class SearchViewModel
    {
        public string? SearchByEntityName { get; set; }
        public string? SearchByLLM { get; set; }
        public int TotalDocuments { get; set; }
        public int FilteredCount { get; set; }
        public List<MappingDocument> SearchResults { get; set; } = new List<MappingDocument>();
    }
}

namespace SAP_MIMOSAapp.Models
{
    public class MappingDocument
    {
        public string? mapID { get; set; }
        public string LLMType { get; set; } = string.Empty;
        public List<MappingPair> mappings { get; set; } = new List<MappingPair>();     
        public string? prompt { get; set; } = string.Empty;
        public string? accuracyRate { get; set; }
        public string? qualityRate { get; set; }
        public string? matchingRate { get; set; }
      
    }
}


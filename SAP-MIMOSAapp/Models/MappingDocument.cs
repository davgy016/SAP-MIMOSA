namespace SAP_MIMOSAapp.Models
{
    public class MappingDocument
    {
        public string mapID { get; set; } = string.Empty;
        public string llmType { get; set; } = string.Empty;
        public List<MappingPair> mappings { get; set; } = new List<MappingPair>();
        public string? Color { get; set; }
        public string aiResponse { get; set; } = string.Empty;
    }
}


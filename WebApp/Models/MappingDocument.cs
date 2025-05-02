namespace SAP_MIMOSAapp.Models
{
    using System.Text.Json.Serialization;

    public class MappingDocument
    {
        [JsonPropertyName("mapID")]
        public string? mapID { get; set; }

        [JsonPropertyName("LLMType")]
        public string LLMType { get; set; } = string.Empty;

        [JsonPropertyName("mappings")]
        public List<MappingPair> mappings { get; set; } = new List<MappingPair>();

        [JsonPropertyName("prompt")]
        public string? prompt { get; set; } = string.Empty;

        [JsonPropertyName("accuracyRate")]
        public string? accuracyRate { get; set; }

        [JsonPropertyName("qualityRate")]
        public string? qualityRate { get; set; }

        [JsonPropertyName("matchingRate")]
        public string? matchingRate { get; set; }
    }
}


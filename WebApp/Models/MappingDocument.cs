namespace SAP_MIMOSAapp.Models;

using System.ComponentModel.DataAnnotations;
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

    [JsonPropertyName("accuracyResult")]
    public AccuracyResultViewModel? accuracyResult { get; set; }

    [JsonPropertyName("accuracySingleMappingPair")]
    public List<AccuracyResultViewModel>? accuracySingleMappingPair { get; set; }

    public List<string> prompts { get; set; } = new List<string>();

}



namespace SAP_MIMOSAapp.Models;

using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;


public class MappingDocument
{
    [JsonPropertyName("mapID")]
    public string? mapID { get; set; }

    [JsonPropertyName("LLMType")]
    public string LLMType { get; set; } = string.Empty;
    public List<promptEntry>? promptHistory { get; set; } = new List<promptEntry>();

    [JsonPropertyName("mappings")]
    public List<MappingPair> mappings { get; set; } = new List<MappingPair>();

    [JsonPropertyName("prompt")]
    public string? prompt { get; set; } = string.Empty;

    [JsonPropertyName("accuracyResult")]
    public AccuracyResultViewModel? accuracyResult { get; set; }

    [JsonPropertyName("accuracySingleMappingPair")]
    public List<AccuracyResultViewModel>? accuracySingleMappingPair { get; set; }

    public List<string> prompts { get; set; } = new List<string>();

    [DisplayFormat(DataFormatString = "{0:yyyy-MM-dd HH:mm:ss}", ApplyFormatInEditMode = true)]
    public DateTime? createdAt { get; set; }

}

public class promptEntry
{
    public string? text { get; set; } = string.Empty;

   
    public DateTime? createdAt { get; set; }
}


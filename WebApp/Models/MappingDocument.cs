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

    [JsonPropertyName("accuracyRate")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? accuracyRate { get; set; }

    [JsonPropertyName("descriptionSimilarity")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? descriptionSimilarity { get; set; }

    [JsonPropertyName("mimosaSimilarity")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? mimosaSimilarity { get; set; }

    [JsonPropertyName("sapSimilarity")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? sapSimilarity { get; set; }

    [JsonPropertyName("dataType")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? dataType { get; set; }

    [JsonPropertyName("infoOmitted")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? infoOmitted { get; set; }


    [JsonPropertyName("fieldLength")]
    [DisplayFormat(DataFormatString = "{0:N2}", ApplyFormatInEditMode = true)]
    public float? fieldLength { get; set; }

    public List<string> prompts { get; set; } = new List<string>();

}



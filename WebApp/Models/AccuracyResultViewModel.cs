using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace SAP_MIMOSAapp.Models
{
    public class AccuracyResultViewModel
    {
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

        [JsonPropertyName("missingFields")]
        public Dictionary<string, List<string>>? missingFields { get; set; } = new Dictionary<string, List<string>>();
    }
}

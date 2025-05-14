namespace SAP_MIMOSAapp.Models
{
    public class MappingField
    {
        public string platform { get; set; } = string.Empty;
        public string entityName { get; set; } = string.Empty;
        public string fieldName { get; set; } = string.Empty;
        public string description { get; set; } = string.Empty;
        public string dataType { get; set; } = string.Empty;
        public string? notes { get; set; } = string.Empty;
        public string? fieldLength { get; set; } = string.Empty;
    }
}


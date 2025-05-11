namespace SAP_MIMOSAapp.Models
{
    public class MappingPairCsvRow
    {
        public string? SAP_EntityName { get; set; }
        public string? SAP_FieldName { get; set; }
        public string? SAP_DataType { get; set; }
        public string? SAP_FieldLength { get; set; }
        public string? SAP_Description { get; set; }
        public string? MIMOSA_EntityName { get; set; }
        public string? MIMOSA_FieldName { get; set; }
        public string? MIMOSA_DataType { get; set; }
        public string? MIMOSA_FieldLength { get; set; }
        public string? MIMOSA_Description { get; set; }
    }
}

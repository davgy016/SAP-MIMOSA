using CsvHelper.Configuration.Attributes;

namespace SAP_MIMOSAapp.Models
{
    public class MappingPairCsvRow
    {
        [Name("SAP_EntityName", "Physical Entity")]
        public string? SAP_EntityName { get; set; }
        [Name("SAP_FieldName", "SAP PM Field Defn")]
        public string? SAP_FieldName { get; set; }
        public string? SAP_DataType { get; set; }
        public string? SAP_FieldLength { get; set; }
        public string? SAP_Description { get; set; }

        [Name("SAP_Notes", "Notes")]
        public string? SAP_Notes { get; set; }


        [Name("MIMOSA_EntityName", "Final Entity Name")]
        public string? MIMOSA_EntityName { get; set; }
        [Name("MIMOSA_FieldName", "Final Attribute Name")]
        public string? MIMOSA_FieldName { get; set; }
        public string? MIMOSA_DataType { get; set; }
        public string? MIMOSA_FieldLength { get; set; }
        public string? MIMOSA_Description { get; set; }
        public string? MIMOSA_Notes { get; set; }
    }
}

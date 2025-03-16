namespace SAP_MIMOSAapp.Models
{
    public class WorkOrderMapping
    {
        public int Id { get; set; }
        public string SapField { get; set; }
        public string Description { get; set; }
        public string DataType { get; set; }
        public string MimosaEquivalent { get; set; }
        public string Notes { get; set; }
        public string Color { get; set; }
    }

}

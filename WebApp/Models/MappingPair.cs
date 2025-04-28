namespace SAP_MIMOSAapp.Models
{
    public class MappingPair
    {
        public MappingField sap { get; set; } = new MappingField();
        public MappingField mimosa { get; set; } = new MappingField();
    }
}


using SAP_MIMOSAapp.Controllers;

namespace SAP_MIMOSAapp.Models
{
    public class WorkOrderViewModel
    {
        public List<WorkOrderMapping> workOrders { get; set; } = new();
        public SearchRequest searchRequest { get; set; } = new();
        public string aiResponse { get; set; } = "";
    }
}

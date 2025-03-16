using System.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using SAP_MIMOSAapp.Models;
using System.Text.Json;
using System.IO;
using System.Collections.Generic;
using System.Linq;
using Microsoft.AspNetCore.Hosting;

namespace SAP_MIMOSAapp.Controllers
{
    public class HomeController : Controller
    {
        private readonly string _jsonFilePath;

        public HomeController(IWebHostEnvironment env)
        {
            _jsonFilePath = Path.Combine(env.ContentRootPath, "Data", "SAPdata.json");
        }

        private List<WorkOrderMapping> LoadDataFromJson()
        {
            if (!System.IO.File.Exists(_jsonFilePath))
                return new List<WorkOrderMapping>();

            var jsonData = System.IO.File.ReadAllText(_jsonFilePath);
            return JsonSerializer.Deserialize<List<WorkOrderMapping>>(jsonData) ?? new List<WorkOrderMapping>();
        }

        private void SaveDataToJson(List<WorkOrderMapping> data)
        {
            var jsonData = JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true });
            System.IO.File.WriteAllText(_jsonFilePath, jsonData);
        }

        [HttpPost]
        public IActionResult ChangeColor(int id, string color)
        {
            var workOrders = LoadDataFromJson();
            var workOrder = workOrders.FirstOrDefault(x => x.Id == id);

            if (workOrder != null)
            {
                workOrder.Color = color; // Save the new color
                SaveDataToJson(workOrders);
            }

            return Json(new { success = true });
        }

        [HttpPost]
        public IActionResult ResetColors()
        {
            var workOrders = LoadDataFromJson(); // Load your existing data

            // Reset colors to the default state (e.g., null or empty)
            foreach (var workOrder in workOrders)
            {
                workOrder.Color = ""; // Or set it to a specific default color
            }

            SaveDataToJson(workOrders); // Save the changes

            return Json(new { success = true });
        }

        public IActionResult Index()
        {
            var workOrders = LoadDataFromJson();
            return View(workOrders);
        }

        [HttpGet]
        public IActionResult Create()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Create(WorkOrderMapping newWorkOrder)
        {
            if (ModelState.IsValid)
            {
                var workOrders = LoadDataFromJson();
                newWorkOrder.Id = workOrders.Any() ? workOrders.Max(x => x.Id) + 1 : 1;
                workOrders.Add(newWorkOrder);
                SaveDataToJson(workOrders);
                return RedirectToAction("Index");
            }
            return View(newWorkOrder); 
        }

        [HttpGet]
        public IActionResult Edit(int id)
        {
            var workOrders = LoadDataFromJson();
            var workOrder = workOrders.FirstOrDefault(x => x.Id == id);
            if (workOrder == null) return NotFound();
            return View(workOrder);
        }

        [HttpPost]
        public IActionResult Edit(WorkOrderMapping updatedWorkOrder)
        {
            var workOrders = LoadDataFromJson();
            var workOrder = workOrders.FirstOrDefault(x => x.Id == updatedWorkOrder.Id);
            if (workOrder == null) return NotFound();

            workOrder.SapField = updatedWorkOrder.SapField;
            workOrder.Description = updatedWorkOrder.Description;
            workOrder.DataType = updatedWorkOrder.DataType;
            workOrder.MimosaEquivalent = updatedWorkOrder.MimosaEquivalent;
            workOrder.Notes = updatedWorkOrder.Notes;

            SaveDataToJson(workOrders);
            return RedirectToAction("Index");
        }

        [HttpPost]
        public IActionResult Delete(int id)
        {
            var workOrders = LoadDataFromJson();
            var workOrder = workOrders.FirstOrDefault(x => x.Id == id);
            if (workOrder != null)
            {
                workOrders.Remove(workOrder);
                SaveDataToJson(workOrders);
            }
            return RedirectToAction("Index");
        }
    }
}

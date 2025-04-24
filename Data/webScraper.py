from urllib.request import urlopen
import re
import csv
from bs4 import BeautifulSoup
import json


class SAPWebScraper():
    def scrape(self, url):
        #open the url
        page = urlopen(url)
        #get the page contents
        html_bytes = page.read()
        #convert to text
        html = html_bytes.decode("utf-8")
        #print to console
        self.html = html
        return html
    def getSlices(self, regex):
        self.slices = re.findall(regex, self.html, re.DOTALL)
        print(self.slices)
        return self.slices

    def write_to_file(self, filename="output.txt"):
        if hasattr(self, 'slices'):
            with open(filename, "w", encoding="utf-8") as f:
                for slice in self.slices:
                    f.write(slice + "\n")
            print(f"Slices written to {filename}")
        else:
            print("No slices found. Run getSlices() first.")

    def extract_visible_text_to_csv(self,filename: str, output_csv: str = None):
        """
        Extracts visible HTML table text from the input file and saves it to a CSV file.
        
        Args:
            filename (str): The input HTML file.
            output_csv (str): Optional. If provided, output will be saved here.
                            Otherwise, it will use the same name with `.csv` extension.
        """
        if output_csv is None:
            output_csv = filename.rsplit('.', 1)[0] + '.csv'

        # Read the HTML content
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        # Find all rows in the table
        rows = soup.find_all('tr')
        data = []

        for row in rows:
            # Extract all cell text, using either <td> or <th>
            cells = row.find_all(['td', 'th'])
            text_cells = [cell.get_text(strip=True).replace(",","") for cell in cells if cell.get_text(strip=True)]
            if text_cells and len(text_cells) >= 7 and len(text_cells) <= 9:  # Skip empty rows
                data.append(text_cells)

        # Save to CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"CSV file saved to: {output_csv}")


    def extract_visible_text_to_json(self, filename: str, output_json: str = None):
        """
        Extracts visible HTML table text from the input file and saves it to a JSON file.
        
        Args:
            filename (str): The input HTML file.
            output_json (str): Optional. If provided, output will be saved here.
                            Otherwise, it will use the same name with `.json` extension.
        """
        if output_json is None:
            output_json = filename.rsplit('.', 1)[0] + '.json'

        # Read the HTML content
        with open(filename, 'r', encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'html.parser')

        rows = soup.find_all('tr')
        data = []

        for row in rows:
            cells = row.find_all(['td', 'th'])
            text_cells = [cell.get_text(strip=True) for cell in cells if cell.get_text(strip=True)]
            if text_cells and 10 <= len(text_cells) <= 13:
                data.append(text_cells)

        # Convert to JSON
        if not data:
            print("No valid table data found.")
            return

        # Use first row as header, rest as data
        headers = data[0]
        json_data = [dict(zip(headers, row)) for row in data[1:]]

        return json_data
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)


    
scraper = SAPWebScraper()
tableNames = []

# scraper.scrape(url="https://sap.erpref.com/?schema=ERP6EHP7&module_id=1295")
# scraper.getSlices("<tr.*?>.*?</tr>")
# scraper.write_to_file("mainTable.txt")
# scraper.extract_visible_text_to_csv("mainTable.txt","mainTable.csv")

with open("mainTable.csv", "r+") as f:
    for line in f.readlines():
        line = line.split(",")
        tableName = line[3]
        tableNames.append(tableName)

print(tableNames)


scraper.scrape(url="https://sap.erpref.com/?schema=ERP6EHP7&module_id=1295&table=EAMS_KPIPARAM")
scraper.getSlices(r"<tr.*?>.*?</tr>")
scraper.write_to_file("output.txt")
json_data = scraper.extract_visible_text_to_json("output.txt","output.json")
with open("output.json", 'w', encoding='utf-8') as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)


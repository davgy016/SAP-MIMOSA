from urllib.request import urlopen
import re
import csv
from bs4 import BeautifulSoup


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
            text_cells = [cell.get_text(strip=True) for cell in cells]
            if text_cells:  # Skip empty rows
                data.append(text_cells)

        # Save to CSV
        with open(output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(data)

        print(f"CSV file saved to: {output_csv}")
    
scraper = SAPWebScraper()

# scraper.scrape(url="https://sap.erpref.com/?schema=ERP6EHP7&module_id=1295")
# scraper.getSlices("<tr>.+?</tr>")
# scraper.write_to_file("output.txt")

scraper.scrape(url="https://sap.erpref.com/?schema=ERP6EHP7&module_id=1295&table=EAMS_CVBEXTDS")
scraper.getSlices(r"<tr.*?>.*?</tr>")
scraper.write_to_file("output.txt")
scraper.extract_visible_text_to_csv("output.txt","output.csv")
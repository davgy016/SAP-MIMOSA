from urllib.request import urlopen
import re


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
        slices = re.findall(regex, self.html)
        print(slices)
    
scraper = SAPWebScraper()
scraper.scrape(url="https://sap.erpref.com/?schema=ERP6EHP7&module_id=1295")
scraper.getSlices("<th>.+</th>")
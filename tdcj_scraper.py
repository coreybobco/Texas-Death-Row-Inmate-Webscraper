from lxml import html
import requests

class TDCJScraper():

    def __init__(self):
        self.base_url = "https://www.tdcj.state.tx.us/death_row/"
        self.directory_url = self.base_url + "dr_offenders_on_dr.html"

    def get_tree(url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def get_inmate_pages(self):
        tree = self.get_tree(self.directory_url)
        for row_index in range(2, len(tree.xpath("//table/tbody//tr"))):
            inmate_url = self.base_url + tree.xpath("//table/tbody/tr[" + str(row_index) + "]/td[2]/a/@href")[0]
            print(inmate_url)

    def get_inmate_info(self, inmate_url):
        tree = self.get_tree(inmate_url)
        inmate_data = tree.xpath("//table//tr/td[3]/text()")
        name = data[0]
        age_when_received = int(data[1])
        county = str(data[2])
        tdcj_number = 
        dob = 
         
TDCJ Number
Date of Birth
Date Received
Age (when Received)
Education Level (Highest Grade Completed)
Date of Offense
Age (at the time of Offense)
County (offense occured in)
Race
Gender
Native County
Native State
Prior Occupation
Prior Prison Record

if __name__ == '__main__':
    tdcj_s = TDCJScraper()
    tdcj_s.get_inmate_pages()

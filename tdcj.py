import csv
from lxml import html
import requests
from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta

class TDCJScraper():

    def __init__(self):
        self.base_url = "https://www.tdcj.state.tx.us/death_row/"
        self.directory_url = self.base_url + "dr_offenders_on_dr.html"
        self.important_keys = ["TDCJ Number", "Name", "Date of Birth", "Age", "Date Received", "Age (when Received)", "Education Level (Highest Grade Completed)", "Date of Offense", "Age (at the time of Offense)", "County", "Race", "Gender", "Native County", "Native State", "Prior Occupation", "Prior Prison Record"]

    def get_tree(self, url):
        page = requests.get(url)
        return html.fromstring(page.content)

    def get_inmate_pages(self):
        tree = self.get_tree(self.directory_url)
        with open('tdcj.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.important_keys)
            writer.writeheader()
            for row_index in range(2, len(tree.xpath("//table/tbody//tr"))):
                inmate_url = self.base_url + tree.xpath("//table/tbody/tr[" + str(row_index) + "]/td[2]/a/@href")[0]
                if not inmate_url.endswith("jpg"):
                    print(inmate_url)
                    inmate_datum = self.get_inmate_info(inmate_url)
                    writer.writerow(inmate_datum)

    def get_inmate_info(self, inmate_url):
        tree = self.get_tree(inmate_url)
        raw_data = tree.xpath("//table//tr/td/text()")
        last_text = ''
        inmate_data = {}

        for text in raw_data:
            if last_text in self.important_keys:
                inmate_data[last_text] = text
            last_text = text

        try:
            now = datetime.now()
            inmate_dob = datetime.strptime(inmate_data["Date of Birth"], "%m/%d/%Y")
            inmate_data['Age'] = str(relativedelta(now, inmate_dob).years) + " yrs " + str(relativedelta(now, inmate_dob).months) + " months "
        except:
            print ("Couldn't calc the age, whatever")
        try:
            inmate_data['Prior Occupation'] = tree.xpath("//span[child::text() = 'Prior Occupation']/following-sibling::text()")[0].strip("\r\n")
        except IndexError:
            inmate_data['Prior Occupation'] = ""
        try:
            inmate_data['Prior Prison Record'] = tree.xpath("//span[child::text() = 'Prior Prison Record']/following-sibling::text()")[0].strip("\r\n")
        except IndexError:
            inmate_data['Prior Occupation'] = ""

        pprint(inmate_data)
        return inmate_data

class Inmate():
    def __init__(self):
        return

if __name__ == '__main__':
    tdcj_s = TDCJScraper()
    tdcj_s.get_inmate_pages()

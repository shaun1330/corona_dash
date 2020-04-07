from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

class corona_scraper():
    def __init__(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17'}

        html = Request('https://www.worldometers.info/coronavirus/', headers=headers)
        response = urlopen(html)

        bsobj = BeautifulSoup(response, "html.parser")
        body = bsobj.find("tbody")  # table of data

        self.corona_data_dict = {}
        for row in body.findAll("tr"):
            columns = row.findAll("td")
            values = []
            for col in columns[1:]:
                if len(col.text.strip()) != 0:
                    col = col.text
                else:
                    col = 0
                values.append(col)
            self.corona_data_dict[columns[0].text] = values

    def get_countries(self):
        return list(self.corona_data_dict.keys())

    def get_country_stats(self, country):
        numbers = self.corona_data_dict[country]
        return numbers

    def number_of_countries(self):
        return len(self.get_countries())

if __name__ == "__main__":
    corona = corona_scraper()
    print(corona.get_country_stats('Australia'))

    print(corona.get_countries())

    print(corona.number_of_countries())
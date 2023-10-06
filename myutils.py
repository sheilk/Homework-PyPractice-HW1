import requests
from bs4 import BeautifulSoup
import bibtexparser
import os


class DownPDF:
    def __init__(self, down_folder_path, reference):
        self.down_path = down_folder_path
        self.reference = reference
    def download(self):
        url = f"https://xueshu.baidu.com/s?wd={self.reference}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Get the first pdf link
        # Assumed to get the right paper(i.e. first paper)
        first_pdf_link = soup.find('a', {'data-click': "{'button_tp':'cite'}"}).get('data-link')
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36",
            "Referer": "https://www.baidu.com/",
        }
        pdf = requests.get(first_pdf_link,headers = headers)
        # test
        file_name = "output.pdf"
        file_path = os.path.join(self.down_path, file_name)
        with open(file_path, 'wb') as file:
            file.write(pdf.content)



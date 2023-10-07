import requests
from bs4 import BeautifulSoup
import bibtexparser
import os
from paperdinfo import*

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

class Downfile:
    def __init__(self,pdf_reader,down_path,filetype = 1):
        # filetype: bibtex is 1, pdf is 0.
        self.pdf = pdf_reader
        self.path = down_path
        self.filetype = filetype 
        self.bibtexes = []

    def getbibfromDBLP(self):
        for ref in self.pdf.ref_titles:
            bibtex = ""
            url = f"https://dblp.org/search?q={ref}&h=1000&f=0&t=o"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            search_res = requests.get(url,headers = headers)
            soup = BeautifulSoup(search_res.content, "html.parser")
            nav_e = soup.find('nav', class_='publ')
            if(nav_e == None):
                continue
            bibtex_url = nav_e.find("a", {"rel": "nofollow"}).get("href")
            
            bib_res = requests.get(bibtex_url,headers=headers)
            soup2 = BeautifulSoup(bib_res.content,"html.parser")
            div_e = soup2.find('div', id='bibtex-section')
            pre_e = div_e.find('pre', class_='verbatim select-on-click')
            bibtex = pre_e.get_text(strip=True)
            self.bibtexes.append(bibtex)
            
        # test
        with open('output.bib', 'w') as bibfile:
            for bibtex in self.bibtexes:
                bibfile.write(bibtex + '\n')
        

# Debug
# path = "C:/Users/liutr/Desktop/1"
# pdf_reader = PDFReader("C:/Users/liutr/Desktop/demo.pdf")
# pdf_reader.read_pdf()
# downfile = Downfile(pdf_reader,path)
# downfile.getbibfromDBLP()
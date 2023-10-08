import requests
from bs4 import BeautifulSoup
import os
import re

# from paperdinfo import*
# Deal with references

class DownPDF:
    # Down arXiv file
    def __init__(self, references, down_path):
        self.path = down_path
        self.references = references
        self.arxiv_ids = []
    def getarxivpdf(self):
        if self.arxiv_ids:
            for i, arxiv_id in enumerate(self.arxiv_ids):
                pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1000.0 Safari/537.36"}
                response = requests.get(pdf_url, headers=headers)
                if response.status_code == 200:
                    file_name = f"ref{i+1}.pdf"
                    file_path = os.path.join(self.path, file_name)
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                else:
                    print("Something Error!")
                    continue
    
    def extract_arxiv_ids(self):
        for string in self.references:
            match = re.search(r'arXiv:\d+\.\d+', string)
            if match:
                self.arxiv_ids.append(match.group())
        

class Downfile:
    # Down bibtex from dblp
    def __init__(self,ref_titles,down_path):
        self.ref_titles = ref_titles
        self.path = down_path
        self.bibtexes = []

    def getbibfromDBLP(self):
        for ref in self.ref_titles:
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
            
        # Write the bibtex
        file_name = "references.bib"
        file_path = os.path.join(self.path, file_name)
        with open(file_path, 'w') as bibfile:
            for bibtex in self.bibtexes:
                bibfile.write(bibtex + '\n')
                
        

# Debug
# path = "C:/Users/liutr/Desktop/1"
# pdf_reader = PDFReader("C:/Users/liutr/Desktop/demo.pdf")
# pdf_reader.read_pdf()
# down_pdfs = DownPDF(pdf_reader.references,path)
# down_pdfs.extract_arxiv_ids()
# down_pdfs.getarxivpdf()
# downfile = Downfile(pdf_reader,path)
# downfile.getbibfromDBLP()
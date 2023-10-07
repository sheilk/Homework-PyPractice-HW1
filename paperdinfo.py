import fitz
import re

class PDFReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.title = ""
        self.firstauthor = ""
        self.references = []
        self.ref_titles = []
        self.ref_num    = []

    def read_pdf(self):
        # Title
        doc = fitz.open(self.file_path)
        first_page = doc[0]
        blocks = first_page.get_text("dict")["blocks"]
        for line in blocks[0]['lines']:
            self.title += str(line['spans'][0]['text'])
        # FirstAuthor
        self.firstauthor = blocks[1]['lines'][0]['spans'][0]['text']
        # References
        text = ""
        find_ref = False
        for page in doc:
            text_content = page.get_text()
            if find_ref == True:
                text += text_content
            if "References\n" in text_content:
                text += text_content.split("References\n")[1]
                find_ref = True

        # Get each reference
        text = text.replace('-\n', '\n')
        for s in text.split('[')[1:]:
            self.references.append(s.split(']')[1].replace('\n', ' ').strip().rsplit('.', 1)[0] + '.')
        
        self.ref_num = len(self.references)
        # Get each reference_title
        for ref in self.references:
            temp = ref
            temp = re.sub(r'(?<=\d)\.(?=\d)', '', temp) 
            self.ref_titles.append(temp.rsplit('.')[-3].strip())
        
# Debug
# pdf_reader = PDFReader("C:/Users/liutr/Desktop/demo.pdf")
# pdf_reader.read_pdf()
# print("标题:", pdf_reader.title)
# print("第一个作者:", pdf_reader.firstauthor)
# print("参考文献:", pdf_reader.references)
# print("参考文献标题:", pdf_reader.ref_titles)
# i = 1
# for s in pdf_reader.ref_titles:
#     print(f"{i}:" + s)
#     i+=1
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
        with fitz.open(self.file_path) as doc:
            first_page = doc[0]
            # read page text as a dictionary, suppressing extra spaces in CJK fonts
            t_texts = []
            sizes = []
            blocks = first_page.get_text("dict", flags=10)["blocks"]
            for b in blocks:                    # iterate through the text blocks
                for l in b["lines"]:            # iterate through the text lines
                    for s in l["spans"]:        # iterate through the text spans
                        t_texts.append(s["text"])
                        sizes.append(s["size"])
            
            # Title and FirstAuthor
            max_size = max(sizes[:10])             #  The last few lines may be a watermark in a larger font
            max_indices = [i for i, size in enumerate(sizes) if size == max_size] 
            self.title = "".join(t_texts[i] for i in max_indices)     
            self.firstauthor = t_texts[max(max_indices)+1].split(',')[0].replace(' ', '')
            # Old way    
            # for line in blocks[0]['lines']:
            #     self.title += str(line['spans'][0]['text'])
            # # FirstAuthor
            # self.firstauthor = blocks[1]['lines'][0]['spans'][0]['text']
        
            # References : assuming that they're at the ending.
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
    
    def extract_title(self):
        pdf_path = self.file_path
        texts = []
        sizes = []
        with fitz.open(pdf_path) as doc:
            page = doc[0]
            
            # read page text as a dictionary, suppressing extra spaces in CJK fonts
            blocks = page.get_text("dict", flags=10)["blocks"]
            for b in blocks:                    # iterate through the text blocks
                for l in b["lines"]:            # iterate through the text lines
                    for s in l["spans"]:        # iterate through the text spans
                        texts.append(s["text"])
                        sizes.append(s["size"])
        
        max_size = max(sizes[:10])             #  The last few lines may be a watermark in a larger font
        max_indices = [i for i, size in enumerate(sizes) if size == max_size] 
        title = "".join(texts[i] for i in max_indices)     
        firstauthor = texts[max(max_indices)+1].split(',')[0].replace(' ', '')
            
        return title,firstauthor  
        
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
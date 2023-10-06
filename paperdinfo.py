import fitz


class PDFReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.title = ""
        self.firstauthor = ""
        self.references = []

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
        ref_index = 0   
        for page_index, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            if blocks[0].get('lines') and blocks[0]['lines'][0].get('spans'):
                if 'Reference' in blocks[0]['lines'][0]['spans'][0]['text']:
                    ref_index = page_index
                    break
        for i in range(ref_index, doc.page_count):
            page = doc[i]
            blocks = page.get_text("dict")["blocks"]
            for block in blocks:
                reference = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        reference += span["text"]
                self.references.append(reference)
        self.references = self.references[1:]
            

# Debug
# pdf_reader = PDFReader("C:/Users/liutr/Desktop/v1.pdf")
# pdf_reader.read_pdf()
# print("标题:", pdf_reader.title)
# print("第一个作者:", pdf_reader.firstauthor)
# print("参考文献:", pdf_reader.references)

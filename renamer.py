import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
import fitz
from pathlib import Path

class RenamerGUI:
    def __init__(self):
        self._set()
        self.pdf_files_paths = []
        self.newnames = []
    def _set(self):
        self.root = TkinterDnD.Tk()
        self.root.title("PDF Files Renamer")
        self.root.geometry("300x200")
        # Create a frame for drag-and-drop input
        self.input = tk.Frame(self.root, borderwidth=2, relief="ridge")
        self.input.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        self.input.drop_target_register(DND_FILES)
        self.input.dnd_bind('<<Drop>>', self._drop_input)
        
        custom_font = ("Helvetica", 11)  
        
        self.prompt_label = tk.Label(self.input, text="Drag and drop input PDF files here", anchor="center", font=custom_font)
        self.prompt_label.pack()
        
    def _drop_input(self, event):
        paths_string = event.data
        self.pdf_files_paths = paths_string.split()
        for path_str in self.pdf_files_paths:
            path_obj = Path(path_str)
            if path_obj.suffix != ".pdf":
                self.pdf_files_paths.remove(path_str)
        if self.pdf_files_paths:
            self._rename()

    def start(self):
        self.root.mainloop()
        
    def _rename(self):
        path_objects = []
        dirs = []
        for path_str in self.pdf_files_paths:
            path_objects.append(Path(path_str))
            self._readpdf(path_str)
        for path_obj in path_objects:
            dirs.append(path_obj.parent)
        for dir, newname, path_obj in zip(dirs,self.newnames,path_objects):
            new_path = dir / newname
            path_obj.rename(new_path)
            
    def _readpdf(self,path):

        title, firstauthor = self.extract_title(path)  
              
        newname = title.strip().replace(':', '') + '-' + firstauthor + ".pdf"
        self.newnames.append(newname)

    def extract_title(self, pdf_path):
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
        

def main():
    renamer =  RenamerGUI()
    renamer.start()   
if __name__ == "__main__":
    main()
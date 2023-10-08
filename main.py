from paperdinfo import PDFReader
from myutils import*
from gui import GUI

def execute_program(gui):
        # Get information from PDF
        pdf_reader = PDFReader(gui.input_path.get())
        pdf_reader.read_pdf()

        # Update the gui information
        gui.update_title(pdf_reader.title)
        gui.update_author(pdf_reader.firstauthor)
        gui.update_references(pdf_reader.references)

        # Down the bibtex
        down_file = Downfile(pdf_reader.ref_titles, gui.output_path.get())
        down_file.getbibfromDBLP()
        down_pdfs = DownPDF(pdf_reader.references, gui.output_path.get())
        down_pdfs.extract_arxiv_ids()
        down_pdfs.getarxivpdf()
        
def main():
    gui = GUI()
    gui.set_execute_callback(lambda: execute_program(gui))
    gui.start_gui()

if __name__ == "__main__":
    main()

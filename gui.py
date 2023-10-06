import tkinter as tk
from tkinter import filedialog, messagebox
from paperdinfo import*
from myutils import*


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Download Paper References")
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        self.input_label = tk.Label(self.root, text="Input Path:")
        self.input_label.pack()
        self.input_entry = tk.Entry(self.root, textvariable=self.input_path)
        self.input_entry.pack()
        self.input_button = tk.Button(self.root, text="Browse", command=self.browse_input)
        self.input_button.pack()
        self.output_label = tk.Label(self.root, text="Output Path:")
        self.output_label.pack()
        self.output_entry = tk.Entry(self.root, textvariable=self.output_path)
        self.output_entry.pack()
        self.output_button = tk.Button(self.root, text="Browse", command=self.browse_output)
        self.output_button.pack()
        
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.pack()
        self.title_text = tk.Text(self.root, height=1, width=50)
        self.title_text.pack()
        self.author_label = tk.Label(self.root, text="First Author:")
        self.author_label.pack()
        self.author_text = tk.Text(self.root, height=1, width=50)
        self.author_text.pack()
        self.references_label = tk.Label(self.root, text="References:")
        self.references_label.pack()
        self.references_text = tk.Text(self.root, height=10, width=50)
        self.references_text.pack()
        
        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute, width=16, height=3)
        self.execute_button.pack(side=tk.LEFT)
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop, width=16, height=3)
        self.stop_button.pack(side=tk.RIGHT)

    def browse_input(self):
        path = filedialog.askopenfilename()
        self.input_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        self.output_path.set(path)

    def execute(self):
        input_path = self.input_path.get()
        output_path = self.output_path.get()
        # Instantiate PDFReader and DownPDF classes and extract information
        pdf_reader = PDFReader(input_path)
        pdf_reader.read_pdf()
        down_pdf = DownPDF(output_path,pdf_reader.references[26])
        # debug and test
        down_pdf.download()
        # Update the GUI with the extracted information
        
        self.title_text.delete(1.0, tk.END)  
        self.title_text.insert(1.0, pdf_reader.title)  

        self.author_text.delete(1.0, tk.END)  
        self.author_text.insert(1.0, pdf_reader.firstauthor)  

        self.references_text.delete(1.0, tk.END)  
        self.references_text.insert(1.0, pdf_reader.references)  
    def stop(self):
        # Stop the execution of the program
        messagebox.showerror("Error", "Program manually stopped before completion!")
        raise Exception("Program manually stopped before completion!")




if __name__ == "__main__":
    gui = GUI()
    gui.root.mainloop()
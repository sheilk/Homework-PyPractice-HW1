import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox

class GUI:
    def __init__(self):
        self.root = TkinterDnD.Tk()
        self.root.title("Download Paper References")
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.isexecuted = False
        self.hascallback = False
        self.execute_callback = None
        
        self._set_input()
        self._set_output()
        self._set_info()

    def _set_input(self):
        # Create a frame for drag-and-drop input
        self.input_drop_frame = tk.Frame(self.root, width=300, height=50, borderwidth=2, relief="ridge")
        self.input_drop_frame.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.input_drop_frame.drop_target_register(DND_FILES)
        self.input_drop_frame.dnd_bind('<<Drop>>', self.drop_input)
        self.prompt_label = tk.Label(self.input_drop_frame, text="Drag and drop input file here to add path")
        self.prompt_label.pack()

        # Create a label for input
        self.input_label = tk.Label(self.root, text="Input Path:")
        self.input_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Entry for input path
        self.input_entry = tk.Entry(self.root, textvariable=self.input_path)
        self.input_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Browse button for input
        self.input_button = tk.Button(self.root, text="Browse", command=self.browse_input)
        self.input_button.grid(row=1, column=2, padx=5, pady=5, sticky="e")
        
    def _set_output(self):
        # Create a frame for drag-and-drop output
        self.output_drop_frame = tk.Frame(self.root, width=300, height=50, borderwidth=2, relief="ridge")
        self.output_drop_frame.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.output_drop_frame.drop_target_register(DND_FILES)
        self.output_drop_frame.dnd_bind('<<Drop>>', self.drop_output)
        self.prompt_label = tk.Label(self.output_drop_frame, text="Drag and drop output folder here to add path")
        self.prompt_label.pack()

        # Create a label for output
        self.output_label = tk.Label(self.root, text="Output Path:")
        self.output_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

        # Entry for output path
        self.output_entry = tk.Entry(self.root, textvariable=self.output_path)
        self.output_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Browse button for output
        self.output_button = tk.Button(self.root, text="Browse", command=self.browse_output)
        self.output_button.grid(row=3, column=2, padx=5, pady=5, sticky="e")
 
    def _set_info(self):
        # Additional title author references
        self.title_label = tk.Label(self.root, text="Title:")
        self.title_label.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.title_text = tk.Text(self.root, height=1, width=50)
        self.title_text.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.author_label = tk.Label(self.root, text="First Author:")
        self.author_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.author_text = tk.Text(self.root, height=1, width=50)
        self.author_text.grid(row=5, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        self.references_label = tk.Label(self.root, text="References:")
        self.references_label.grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.references_text = tk.Text(self.root, height=10, width=50)
        self.references_text.grid(row=6, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Execute and Stop
        self.execute_button = tk.Button(self.root, text="Execute", command=self.execute, width=16, height=3)
        self.execute_button.grid(row=7,column=0,sticky='w')
        self.stop_button = tk.Button(self.root, text="Stop", command=self.stop, width=16, height=3)
        self.stop_button.grid(row=7,column=2, sticky='e')
        
    def browse_input(self):
        path = filedialog.askopenfilename()
        self.input_path.set(path)

    def browse_output(self):
        path = filedialog.askdirectory()
        self.output_path.set(path)

    def drop_input(self, event):
        file_path = event.data
        self.input_path.set(file_path)

    def drop_output(self, event):
        folder_path = event.data
        self.output_path.set(folder_path)

    def stop(self):
        # Stop the execution of the program
        if self.isexecuted:
            messagebox.showerror("Error", "Program manually stopped before completion!")
            raise Exception("Program manually stopped before completion!")
    
    def start_gui(self):
        # Start the mainloop
        self.root.mainloop()
        
    def execute(self):
        # Check the execute_callback
        if self.hascallback:
            self.execute_callback()
            self.isexecuted = True
        else:
            raise Exception("No execute_callback function!")
        
    def set_execute_callback(self, callback):
        # Get the execute-callbak
        self.execute_callback = callback
        self.hascallback = True

    def update_title(self, title):
        self.title_text.delete(1.0, tk.END)  
        self.title_text.insert(1.0, title)  
    
    def update_author(self, author):
        self.author_text.delete(1.0, tk.END)  
        self.author_text.insert(1.0, author)  
        
    def update_references(self, references):
        self.references_text.delete(1.0, tk.END)  
        result = '\n'.join([f'[{i+1}] {r}' for i, r in enumerate(references)])
        self.references_text.insert(1.0, result) 
        
# Debug
# def execute_program():
#     print("success!!")
#     gui.update_title("This is title!")

# if __name__ == "__main__":
#     gui = GUI()
#     gui.set_execute_callback(execute_program)
#     gui.start_gui()

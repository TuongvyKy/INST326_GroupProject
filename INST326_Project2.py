# imports
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import datetime # one module for working with dates and times

# The MainWindow class creates a custom GUI window based on the tkinter window (tk.Tk)
# It has an __init__() method, and three additional methods (new_note(), open_notebook(), and save_notebook())
# These methods correspond to new, open, and save buttons in the window.
# The new_note method calls the NoteForm class to create a new note form top level window.

class MainWindow(tk.Tk):
    def __init__(self):  #initialize the main window
        super().__init__() # initialize it as a tkinter window
        
        self.geometry("600x400") # set the default window size
        self.title('Notebook') #set the default window title
        self.notebook = [] # initialize an attribute named 'notebook' as an empty list
        self.notes = []
        
        # Buttons for creating new notes, opening notebook, and saving notebook
        self.new_note_button = tk.Button(self, text = "New Note", command = self.new_note)
        self.new_note_button.grid(padx = 10, pady = 10, row = 0, column = 0)

        self.open_notebook_button = tk.Button(self, text = "Open Notebook", command = self.open_notebook)
        self.open_notebook_button.grid(padx = 10, pady = 10, row = 0, column = 1)

        self.save_notebook_button = tk.Button(self, text = "Save Notebook", command = self.save_notebook)
        self.save_notebook_button.grid(padx = 10, pady = 10, row = 0, column = 2)

        # Frame to add previews of the notes onto main window
        self.note_preview_frame = tk.Frame(self)
        self.note_preview_frame.grid(row = 1, column = 0, columnspan = 3, padx = 10, pady = 10)

        
    def new_note(self): 
        note_window = NoteForm(self, self.notebook, self.notes)

    def open_notebook(self):
        filepath = filedialog.askopenfilename(filetypes=[("text files", "*.txt"), ("all files", "*.*")])
        if filepath:
            with open(filepath, "r") as file:
                lines = file.readlines()
                num_lines = len(lines)
                for i in range(0, len(lines), 6):  
                    title = lines[i].strip()
                    text = lines[i + 1].strip()
                    links = lines[i + 2].strip()
                    tags = lines[i + 3].strip()
                    date = lines[i + 4].strip()
                    zone = lines[i + 5].strip()
                
                    # Create MakeNote object with all details including date, time, and timezone
                    self.notes.append(MakeNote({"title": title, "text": text, "links": links, "tags": tags, "created_at": date, "timezone": zone}))
            self.update_note_preview()

    def save_notebook(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "w") as file:
                for note in self.notes:
                    file.write(f"Title: {note.title}\n{note.text}\nLinks: {note.links}\nTags: {note.tags}\nCreated At: {note.created_at}\n{note.zone}\n")
                    
    def update_note_preview(self): # Function to add notes and newly created ones to the main window
        for widget in self.note_preview_frame.winfo_children():
            widget.destroy()
            
        num_notes = len(self.notes)
        num_columns = 3 # Limit to 3 note previews to be shown on main window per row
        num_rows = (num_notes + num_columns - 1) // num_columns


        for i, note in enumerate(self.notes):
            preview_text = note.text[:30] + "..." if len(note.text) > 30 else note.text # Only show a preview of text and not full text unless text is less than 30 characters
            label_text = f"Title: {note.title}\nText: {preview_text}\n"
            button = tk.Button(self.note_preview_frame, text = label_text)
            row = i // num_columns
            column = i % num_columns
            button.grid(row = row, column = column, sticky = "w")
            button.bind("<Button-1>", lambda event, note = note: self.display_notes(note)) # When note preview is clicked, the full note is displayed on a new window on top of main window
            
    def display_notes(self,note): # Function to display notes when note preview is clicked on 
        display_window = tk.Toplevel(self)
        display_window.geometry("400x150")
        display_window.title(note.title)
        display_text = f'Title: {note.title}\n{note.text}\nlinks: {note.links}\ntags: {note.tags}\n{note.created_at}\n{note.zone}\n'
        text_label = tk.Label(display_window, text = display_text)
        text_label.grid(padx = 10, pady = 10, row = 2, column = 3)
        
            
# the NoteForm() class creates a Toplevel window that is a note form containing fields for
# data entry for title, text, link, and tags. It also calculates a meta field with date, time, and timezone
# the Noteform class has an __init__() method, and a submit() method that is called by a submit button
# the class may contain additional methods to perform tasks like calculating the metadata, for example
# the submit method calls the MakeNote class that transforms the the entered data into a new note object.

class NoteForm(tk.Toplevel):
    
    def __init__(self, master, notebook, notes): # initialize the new object
        super().__init__(master) # initialize it as a toplevel window
        self.master = master
        self.notebook = notebook
        self.notes = notes

        # Fields for note 
        self.note_title_label = tk.Label(self, text = "Title:")
        self.title_entry = tk.Entry(self, width = 80)
        
        self.text_label = tk.Label(self, text = "Text:")
        self.text_entry = tk.Text(self, height = 5, width = 60, wrap = tk.WORD)
        
        self.links_label = tk.Label(self, text = "Link:")
        self.links_entry = tk.Entry(self, width = 80)
        
        self.tags_label = tk.Label(self, text = "Tags:")
        self.tags_entry = tk.Entry(self, width = 80)
        
        # Button to submit the note
        self.submit_button = tk.Button(self, text = "Submit", command = self.submit)
        
        # Layout the widgets
        self.note_title_label.grid(row = 0, column = 0, sticky = "e")
        self.title_entry.grid(row = 0, column = 1, sticky = "we", padx = 5, pady = 5)

        self.text_label.grid(row = 1, column = 0, sticky = "e")
        self.text_entry.grid(row = 1, column = 1, columnspan = 2, padx = 5, pady = 5)

        self.links_label.grid(row = 2, column = 0, sticky = "e")
        self.links_entry.grid(row = 2, column = 1, sticky = "we", padx = 5, pady = 5)

        self.tags_label.grid(row = 3, column = 0, sticky = "e")
        self.tags_entry.grid(row = 3, column = 1, sticky = "we", padx = 5, pady = 5)

        self.submit_button.grid(row = 4, column = 1, sticky = "e", pady = 5)
        
    def submit(self):
        created = datetime.datetime.now()
        local_now = created.astimezone()
        local_tz = local_now.tzinfo 
        title = self.title_entry.get()
        text = self.text_entry.get("1.0", "end-1c")
        links = self.links_entry.get()
        tags = self.tags_entry.get()
        meta = f'created {created}, {local_tz}'

        note_dict = {"title": title,
                    "text": text,
                    "links": links,
                    "tags": tags}

        new_note = MakeNote(note_dict)
        self.notes.append(new_note)
        self.master.update_note_preview()
        self.destroy() # closes note making window when submit is clicked
        
# The MakeNote class takes a dictionary containing the data entered into the form window,
# and transforms it into a new note object.
# At present the note objects have attributes but no methods.

class MakeNote():
    def __init__(self, note_dict):
        self.note_dict = note_dict
        self.title = note_dict["title"]
        self.text = note_dict["text"]
        self.links = note_dict["links"]
        self.tags = note_dict["tags"]
        self.created_at = datetime.datetime.now().astimezone()
        self.zone = datetime.datetime.now().astimezone().tzinfo   
        
# main execution

if __name__ == '__main__':
    
    main_window = MainWindow() # this creates a notebook / main window called main_window. 

    main_window.mainloop()


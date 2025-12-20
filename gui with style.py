import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pysubparser import parser

class SubtitleReplacerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Subtitle Word Replacer")
        self.root.geometry("600x500")
        
        # Set window icon (replace with your own icon path if available)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # Configure styles
        self.configure_styles()
        
        # Create main container with padding
        main_container = tk.Frame(root, bg='#f0f0f0', padx=20, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_container,
            text="Subtitle Word Replacer",
            font=('Arial', 16, 'bold'),
            bg='#f0f0f0',
            fg='#333333'
        )
        title_label.pack(pady=(0, 20))
        
        # Input file section
        input_frame = self.create_section(main_container, "Input File")
        
        self.input_file_entry = self.create_file_entry(
            input_frame,
            "Browse Input File",
            self.browse_input_file
        )
        
        # Output file section
        output_frame = self.create_section(main_container, "Output File")
        
        self.output_file_entry = self.create_file_entry(
            output_frame,
            "Browse Output File",
            self.browse_output_file
        )
        
        # Replacements section
        replacements_frame = self.create_section(main_container, "Replacements")
        
        replacements_help = tk.Label(
            replacements_frame,
            text="Format: old:new,old:new",
            font=('Arial', 9),
            bg='#f0f0f0',
            fg='#666666'
        )
        replacements_help.pack(pady=(0, 5))
        
        self.replacements_entry = tk.Entry(
            replacements_frame,
            width=50,
            font=('Arial', 10),
            relief=tk.FLAT,
            bg='white',
            highlightthickness=1,
            highlightcolor='#4CAF50',
            highlightbackground='#cccccc'
        )
        self.replacements_entry.pack(pady=5, ipady=5)
        
        # Example text
        example_label = tk.Label(
            replacements_frame,
            text="Example: hello:hola,goodbye:adios",
            font=('Arial', 9, 'italic'),
            bg='#f0f0f0',
            fg='#888888'
        )
        example_label.pack(pady=(5, 0))
        
        # Replace button
        self.replace_button = tk.Button(
            main_container,
            text="Replace Words",
            command=self.replace_words,
            font=('Arial', 11, 'bold'),
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=30,
            pady=10
        )
        self.replace_button.pack(pady=20)
        
        # Status bar
        self.status_bar = tk.Label(
            root,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W,
            bg='#e0e0e0',
            fg='#333333',
            font=('Arial', 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Bind hover effects
        self.bind_hover_effects()

    def configure_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure button style
        style.configure(
            'Custom.TButton',
            background='#4CAF50',
            foreground='white',
            borderwidth=0,
            focusthickness=3,
            focuscolor='none',
            font=('Arial', 11, 'bold')
        )
        style.map(
            'Custom.TButton',
            background=[('active', '#45a049')],
            foreground=[('active', 'white')]
        )

    def create_section(self, parent, title):
        """Create a labeled section container"""
        frame = tk.Frame(parent, bg='#f0f0f0')
        frame.pack(fill=tk.X, pady=10)
        
        label = tk.Label(
            frame,
            text=title,
            font=('Arial', 12, 'bold'),
            bg='#f0f0f0',
            fg='#555555',
            anchor=tk.W
        )
        label.pack(fill=tk.X)
        
        return frame

    def create_file_entry(self, parent, button_text, command):
        """Create a file entry with browse button"""
        entry_frame = tk.Frame(parent, bg='#f0f0f0')
        entry_frame.pack(fill=tk.X, pady=5)
        
        entry = tk.Entry(
            entry_frame,
            width=50,
            font=('Arial', 10),
            relief=tk.FLAT,
            bg='white',
            highlightthickness=1,
            highlightcolor='#2196F3',
            highlightbackground='#cccccc'
        )
        entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=5)
        
        button = tk.Button(
            entry_frame,
            text=button_text,
            command=command,
            font=('Arial', 10),
            bg='#2196F3',
            fg='white',
            activebackground='#1976D2',
            activeforeground='white',
            relief=tk.FLAT,
            cursor='hand2',
            padx=15,
            pady=5
        )
        button.pack(side=tk.RIGHT)
        
        return entry

    def bind_hover_effects(self):
        """Bind hover effects to buttons"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.bind('<Enter>', lambda e, w=widget: w.configure(bg=w.cget('activebackground')))
                widget.bind('<Leave>', lambda e, w=widget: w.configure(bg='#4CAF50' if w == self.replace_button else '#2196F3'))

    def browse_input_file(self):
        filename = filedialog.askopenfilename(
            title="Select Input ASS File",
            filetypes=[("ASS Files", "*.ass"), ("All Files", "*.*")]
        )
        if filename:
            self.input_file_entry.delete(0, tk.END)
            self.input_file_entry.insert(0, filename)
            self.update_status(f"Input file selected: {filename.split('/')[-1]}")

    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output ASS File",
            defaultextension=".ass",
            filetypes=[("ASS Files", "*.ass"), ("All Files", "*.*")]
        )
        if filename:
            self.output_file_entry.delete(0, tk.END)
            self.output_file_entry.insert(0, filename)
            self.update_status(f"Output file set: {filename.split('/')[-1]}")

    def replace_words(self):
        input_file = self.input_file_entry.get()
        output_file = self.output_file_entry.get()
        replacements_input = self.replacements_entry.get()

        if not input_file or not output_file or not replacements_input:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Parse replacements
        replacements = {}
        try:
            for item in replacements_input.split(','):
                old_word, new_word = item.split(':')
                replacements[old_word.strip()] = new_word.strip()
        except ValueError:
            messagebox.showerror("Error", "Invalid replacements format. Use 'old:new,old:new'.")
            return

        # Update status and disable button during processing
        self.update_status("Processing...")
        self.replace_button.config(state=tk.DISABLED, bg='#cccccc')
        self.root.update()

        # Call the replacement function
        try:
            self.replace_words_in_ass(input_file, output_file, replacements)
        finally:
            # Re-enable button
            self.replace_button.config(state=tk.NORMAL, bg='#4CAF50')

    def replace_words_in_ass(self, input_file, output_file, replacements):
        try:
            # Read the entire input file to extract metadata
            with open(input_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Extract metadata (everything before the [Events] section)
            metadata = []
            events_header = None
            for line in lines:
                if line.strip().startswith("[Events]"):
                    events_header = line  # Save the [Events] header
                    break
                metadata.append(line)

            # Parse the subtitles using pysubparser
            subtitles = parser.parse(input_file)

            # Write the modified file
            with open(output_file, "w", encoding="utf-8") as f:
                # Write metadata
                f.writelines(metadata)

                # Write the [Events] header
                if events_header:
                    f.write(events_header)

                # Write the modified subtitles
                for subtitle in subtitles:
                    new_text = subtitle.text
                    for old_word, new_word in replacements.items():
                        new_text = new_text.replace(old_word, new_word)
                    # Ensure the timestamps are in the correct format
                    start_time = subtitle.start.strftime("%H:%M:%S.%f")[:-4]  # Trim to 2 decimal places
                    end_time = subtitle.end.strftime("%H:%M:%S.%f")[:-4]  # Trim to 2 decimal places

                    # Handle missing attributes with default values
                    layer = getattr(subtitle, 'layer', 0)  # Default layer is 0
                    style = getattr(subtitle, 'style', 'Default')  # Default style is 'Default'
                    name = getattr(subtitle, 'name', '')  # Default name is empty
                    margin_l = getattr(subtitle, 'margin_l', 0)  # Default margin_l is 0
                    margin_r = getattr(subtitle, 'margin_r', 0)  # Default margin_r is 0
                    margin_v = getattr(subtitle, 'margin_v', 0)  # Default margin_v is 0
                    effect = getattr(subtitle, 'effect', '')  # Default effect is empty

                    # Format the subtitle line according to ASS specifications
                    text_input = f"Dialogue: {layer},{start_time},{end_time},{style},{name},{margin_l},{margin_r},{margin_v},{effect},{new_text}\n"
                    f.write(text_input)

            self.update_status("Words replaced successfully!")
            messagebox.showinfo(
                "Success",
                f"Words replaced successfully!\n\n"
                f"Input: {input_file.split('/')[-1]}\n"
                f"Output: {output_file.split('/')[-1]}\n"
                f"Replacements made: {len(replacements)}"
            )
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror(
                "Error",
                f"An error occurred:\n\n{str(e)}\n\n"
                "Please check:\n"
                "1. The input file exists and is accessible\n"
                "2. The file is a valid ASS subtitle file\n"
                "3. You have write permissions for the output location"
            )

    def update_status(self, message):
        """Update the status bar with a message"""
        self.status_bar.config(text=f"Status: {message}")
        self.root.update()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    
    # Center the window on screen
    window_width = 600
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    app = SubtitleReplacerApp(root)
    root.mainloop()
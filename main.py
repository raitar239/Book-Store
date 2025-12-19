import tkinter as tk
from tkinter import ttk, messagebox, filedialog, PhotoImage


class BookStore:
    """Window book store"""

    #MAIN FUNCTIONS
    def __init__(self, root):
        """Init constants and window"""
        self.root = root
        self.root.iconbitmap('RGZ/assets/icon.ico') 

        self.books = []
        self.capacity = 50

        self.setup_window()
        self.create_widgets()

    def setup_window(self):
        """Parameters window"""
        self.root.title("Book store")
        self.root.geometry("1000x625")
        self.root.configure(bg="#f5e6d3")

    def create_widgets(self):
        """Create all widgets"""
        #Title with logo
        title_frame = tk.Frame(self.root, bg="#5d4037", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        self.logo_image = PhotoImage(file='RGZ/assets/logo.png')
        self.logo_image = self.logo_image.subsample(11, 11)  
        logo_label = tk.Label(title_frame, image=self.logo_image, bg="#5d4037")
        logo_label.pack(side=tk.LEFT, padx=15, pady=10)
        
        title_label = tk.Label(title_frame, text="BOOK STORE", font=("Georgia", 20, "bold"), bg="#5d4037", fg="#f5e6d3")
        title_label.pack(pady=15)

        #Main container and panels
        main_container = tk.Frame(self.root, bg="#f5e6d3")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        main_container.grid_columnconfigure(0, weight=0, minsize=250)
        main_container.grid_columnconfigure(1, weight=3)

        self.left_panel(main_container)
        self.right_panel(main_container)

    def left_panel(self, parent):
        "Create left panel with management"
        left_container = tk.Frame(parent, bg="#f5e6d3")
        left_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        #MANAGEMENT FRAME
        management_frame = tk.LabelFrame(left_container, text="Book management", font=("Georgia", 12, "bold"), bg="#f5e6d3", fg="#5d4037", padx=10, pady=10)
        management_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        management_frame.grid_columnconfigure(1, weight=1)

        #Title entry
        tk.Label(management_frame, text="Title:", bg="#f5e6d3", fg="#5d4037", font=("Georgia", 10)).grid(row=0, column=0, sticky=tk.W, pady=3, padx=(0, 5))
        
        self.title_entry = tk.Entry(management_frame, font=("Georgia", 10))
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=3)

        #Author entry
        tk.Label(management_frame, text="Author:", bg="#f5e6d3", fg="#5d4037", font=("Georgia", 10)).grid(row=1, column=0, sticky=tk.W, pady=3, padx=(0, 5))
        
        self.author_entry = tk.Entry(management_frame, font=("Georgia", 10))
        self.author_entry.grid(row=1, column=1, sticky="ew", pady=3)

        #Quantity entry
        tk.Label(management_frame, text="Quantity:", bg="#f5e6d3", fg="#5d4037", font=("Georgia", 10)).grid(row=2, column=0, sticky=tk.W, pady=3, padx=(0, 5))
        
        self.quantity_entry = tk.Entry(management_frame, font=("Georgia", 10))
        self.quantity_entry.grid(row=2, column=1, sticky="ew", pady=3)
        self.quantity_entry.insert(0, "1")

        #Management buttons 
        self.create_button(management_frame, "Add", "#5d4037", self.add_book, 3)
        self.create_button(management_frame, "Delete", "#5d4037", self.delete_book, 4)
        self.create_button(management_frame, "Sell", "#8d6e63", self.sell_book, 5)

        #SEARCH FRAME
        search_frame = tk.LabelFrame(left_container, text="Search", font=("Georgia", 12, "bold"), bg="#f5e6d3", fg="#5d4037", padx=10, pady=10)
        search_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.search_entry = tk.Entry(search_frame, font=("Georgia", 10))
        self.search_entry.pack(fill=tk.X, pady=3)

        #Search buttons
        self.create_button(search_frame, "By title", "#5d4037", self.search_by_title, pack=True)
        self.create_button(search_frame, "By author", "#5d4037", self.search_by_author, pack=True)
        self.create_button(search_frame, "Reset", "#8d6e63", self.reset_search, pack=True)

        #FILE FRAME
        file_frame = tk.LabelFrame(left_container, text="Файл", font=("Georgia", 12, "bold"), bg="#f5e6d3", fg="#5d4037", padx=10, pady=10)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.create_button(file_frame, "Load", "#5d4037", self.load_from_file, pack=True)
        self.create_button(file_frame, "Save", "#5d4037", self.save_to_file, pack=True)

    def create_button(self, parent, text, bg_color, command, row=None, pack=False):
        """Create buttons with given parameters"""
        button = tk.Button(parent, text=text, bg=bg_color, fg="#f5e6d3", font=("Georgia", 10, "bold"), cursor="hand2", relief=tk.RAISED, borderwidth=2, command=command)

        if pack: 
            button.pack(fill=tk.X, pady=3)
        else: 
            button.grid(row=row, columnspan=2, sticky="ew", pady=3, padx=5)

        return button

    def right_panel(self, parent):
        """Create right panel with bookshelf"""
        right_panel = tk.LabelFrame(parent, text="Bookshelf", font=("Georgia", 12, "bold"), bg="#f5e6d3", fg="#5d4037")
        right_panel.grid(row=0, column=1, sticky="nsew")
        
        #Counter books
        self.capacity_label = tk.Label(right_panel, text=f"Capacity: 0 / {self.capacity}", bg="#f5e6d3", fg="#5d4037", font=("Georgia", 10, "bold"))
        self.capacity_label.pack(pady=5)

        #Bookshelf table style
        style = ttk.Style()
        style.theme_use("default")
        style.map("Treeview", background=[("selected", "#8d6e63")], foreground=[("selected", "#f5e6d3")])
        style.configure("Treeview", background="#fff8f0", fieldbackground="#fff8f0", foreground="#5d4037", font=("Georgia", 10))
        style.configure("Treeview.Heading", background="#5d4037", foreground="#f5e6d3", font=("Georgia", 10, "bold"), relief=tk.FLAT)
        style.map("Treeview.Heading", background=[("active", "#5d4037"), ("pressed", "#5d4037")], relief=[("active", tk.FLAT), ("pressed", tk.FLAT)])
        
        #Create table
        self.tree = ttk.Treeview(right_panel, columns=("title", "author", "quantity"), show="headings", height=18)
        
        self.tree.heading("title", text="Title")
        self.tree.heading("author", text="Author")
        self.tree.heading("quantity", text="Quantity")
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.fill_from_selection)

    #AUXILIARY FUNCTIONS
    def total_quantity(self):
        '''Count of books on the shelf'''
        return sum(book["quantity"] for book in self.books)

    def validate_entry(self, title, author, qty):
        '''Check validate entry data'''
        if not title or not author or not qty:
            messagebox.showwarning("Error", "Please fill in all fields")
            return False

        if qty <= 0:
            messagebox.showerror("Error", "Please enter a positive integer number of books")
            return False

        if self.total_quantity() + qty > self.capacity:
            messagebox.showerror("Error", "Shelf capacity exceeded")
            return False

        return True

    def update_tree(self, filtered=None, select_item=None):
        '''Update contents of the book table'''
        #Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)

        #Fill table
        data = filtered if filtered is not None else self.books
        for book in data:
            self.tree.insert("", tk.END, values=(book["title"], book["author"], book["quantity"]))

        #Select item
        if select_item:
            for iid in self.tree.get_children():
                vals = self.tree.item(iid)['values']
                if (vals[0] == select_item['title'] and vals[1] == select_item['author']):
                    self.tree.selection_set(iid)
                    self.tree.see(iid)
                    break
        elif data:
            last_iid = self.tree.get_children()[-1]
            self.tree.selection_set(last_iid)
            self.tree.see(last_iid)

        #Update counter
        total = self.total_quantity()
        self.capacity_label.config(
            text=f"Capacity: {total} / {self.capacity}"
        )

    #MANAGEMENT FUNCTIONS
    def add_book(self):
        '''Add book or increases the amount'''
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        try:
            qty = int(self.quantity_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Quantity must be integer")
            return
        
        if not self.validate_entry(title, author, qty):
            return

        #Check availability  
        for book in self.books:
            if (book["title"].lower() == title.lower() and book["author"].lower() == author.lower()):
                book["quantity"] += qty
                self.update_tree(select_item=book)
                return

        #Add new book
        new_book = {"title": title, "author": author, "quantity": qty}
        self.books.append(new_book)
        self.update_tree(select_item=new_book)

    def delete_book(self):
        '''Delete book'''
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Choice a book")
            return

        title, author = self.tree.item(selected[0])['values'][:2]
        self.books = [b for b in self.books if not (b["title"] == title and b["author"] == author)]
        self.update_tree()

    def sell_book(self):
        '''Reduce count of books by 1'''
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "Choice a book")
            return

        title, author = self.tree.item(selected[0])['values'][:2]

        for book in self.books:
            if book["title"] == title and book["author"] == author:
                book["quantity"] -= 1
                if book["quantity"] <= 0:
                    self.books.remove(book)
                    self.update_tree()
                else:
                    self.update_tree(select_item=book)
                return
            
    #SEARCH FUNCTIONS
    def search_by_title(self):
        '''Search for books by title'''
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showwarning("Error", "Type title!")
            return

        filtered = [b for b in self.books if query in b["title"].lower()]
        self.update_tree(filtered)

    def search_by_author(self):
        '''Search for books by author'''
        query = self.search_entry.get().lower()
        if not query:
            messagebox.showwarning("Error", "Type author!")
            return

        filtered = [b for b in self.books if query in b["author"].lower()]
        self.update_tree(filtered)

    def reset_search(self):
        '''Reset search results and shows all books'''
        self.search_entry.delete(0, tk.END)
        self.update_tree()

    #FILE FUNCTIONS
    def save_to_file(self):
        '''Save list of books to text file '''
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")])
        if not file_path: 
            return

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                for book in self.books:
                    line = f"{book['title']};{book['author']};{book['quantity']}\n"
                    f.write(line)
            
            messagebox.showinfo("Success", "Data success save")
        except Exception as e:
            messagebox.showerror("Error", f"Error save data: {e}")

    def load_from_file(self):
        '''Load list of books from text file'''
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path: return
        try:
            temp_books = []
            total_qty = 0

            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    parts = line.strip().split(";")
                    if len(parts) == 3:
                        title, author, qty = parts
                        total_qty += int(qty) 
                        temp_books.append({"title": title, "author": author, "quantity": int(qty)})
            
            if total_qty > self.capacity:
                messagebox.showerror("Error", f"Cannot load: total books - {total_qty} exceeds capacity - {self.capacity}")
                return
            
            self.books.clear()
            self.books = temp_books
            self.update_tree()
            messagebox.showinfo("Success", f"Load success: {total_qty}/{self.capacity} books")
            
        except ValueError:
            messagebox.showerror("Error", "Invalid quantity format in file")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading: {e}")

    #FILL FUNCTION
    def fill_from_selection(self, event):
        '''Fill input fields data'''
        selected = self.tree.selection()
        if not selected: return

        title, author, _ = self.tree.item(selected[0])['values']
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, title)
        self.author_entry.delete(0, tk.END)
        self.author_entry.insert(0, author)
        self.quantity_entry.delete(0, tk.END)
        self.quantity_entry.insert(0, "1")


if __name__ == "__main__":
    root = tk.Tk()
    BookStore(root)
    root.mainloop()

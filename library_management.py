import tkinter as tk
from tkinter import messagebox
import sqlite3

class LibraryManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("500x600")
        self.master.config(bg='#708090')

        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        # Initialize the database
        self.initialize_db()

        # Login UI elements
        self.login_label = tk.Label(self.master, text="Library Management System", font=("Helvetica", 16), bg='#708090', fg='white')
        self.login_label.pack(pady=10)
        self.username_label = tk.Label(self.master, text="Username", font=("Helvetica", 12), bg='#708090', fg='white')
        self.username_label.pack()
        self.username_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.username_entry.pack()
        self.password_label = tk.Label(self.master, text="Password", font=("Helvetica", 12), bg='#708090', fg='white')
        self.password_label.pack()
        self.password_entry = tk.Entry(self.master, font=("Helvetica", 12), show="*")
        self.password_entry.pack()

        # Buttons
        self.login_button = tk.Button(self.master, text="Login", command=self.login, font=("Helvetica", 12))
        self.login_button.pack(pady=5)
        self.register_button = tk.Button(self.master, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_button.pack(pady=5)
        self.reset_button = tk.Button(self.master, text="Reset System", command=self.reset_system, font=("Helvetica", 12), bg='red', fg='white')
        self.reset_button.pack(pady=5)

    def initialize_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS librarians (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                author TEXT,
                isbn TEXT,
                year TEXT
            )
        """)
        self.conn.commit()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT * FROM librarians WHERE username = ? AND password = ?", (username, password))
        librarian = self.cursor.fetchone()
        if librarian:
            self.library_management_screen()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            self.cursor.execute("INSERT INTO librarians (username, password, role) VALUES (?, ?, ?)", (username, password, "user"))
            self.conn.commit()
            messagebox.showinfo("Success", "Registration successful")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    def reset_system(self):
        if messagebox.askyesno("Reset System", "Are you sure you want to reset the entire system? This action cannot be undone."):
            self.cursor.execute("DELETE FROM librarians")
            self.cursor.execute("DELETE FROM books")
            self.conn.commit()
            messagebox.showinfo("Success", "System reset successfully.")

    def library_management_screen(self):
        # Clear login screen
        for widget in self.master.winfo_children():
            widget.destroy()

        # Add book management UI
        self.book_title_label = tk.Label(self.master, text="Book Title", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_title_label.pack()
        self.book_title_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_title_entry.pack()

        self.book_author_label = tk.Label(self.master, text="Author", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_author_label.pack()
        self.book_author_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_author_entry.pack()

        self.book_isbn_label = tk.Label(self.master, text="ISBN", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_isbn_label.pack()
        self.book_isbn_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_isbn_entry.pack()

        self.book_year_label = tk.Label(self.master, text="Year", font=("Helvetica", 12), bg='#708090', fg='white')
        self.book_year_label.pack()
        self.book_year_entry = tk.Entry(self.master, font=("Helvetica", 12))
        self.book_year_entry.pack()

        self.add_book_button = tk.Button(self.master, text="Add Book", command=self.add_book, font=("Helvetica", 12))
        self.add_book_button.pack(pady=5)

        # Section to display book list
        self.books_display = tk.Text(self.master, width=50, height=10, font=("Helvetica", 12))
        self.books_display.pack(pady=10)

        self.view_books_button = tk.Button(self.master, text="View Book List", command=self.view_books, font=("Helvetica", 12))
        self.view_books_button.pack(pady=5)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()
        year = self.book_year_entry.get()
        self.cursor.execute("INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)", (title, author, isbn, year))
        self.conn.commit()
        messagebox.showinfo("Success", "Book added successfully")

    def view_books(self):
        self.books_display.delete(1.0, tk.END)
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if books:
            for book in books:
                book_details = f"Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Year: {book[4]}\n"
                self.books_display.insert(tk.END, book_details)
        else:
            self.books_display.insert(tk.END, "No books available.\n")

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagement(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox, PhotoImage
import sqlite3

class LibraryManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("600x600")
        self.master.config(bg='#f0f0f0')  # Light background for a cleaner look

        # Connect to SQLite database (or create it if it doesn't exist)
        self.conn = sqlite3.connect("library.db")
        self.cursor = self.conn.cursor()

        # Initialize the database
        self.initialize_db()

        # Frame for Login Section
        self.login_frame = tk.Frame(self.master, bg='#ffffff', padx=20, pady=20)
        self.login_frame.pack(pady=20)

        # Title Label
        self.login_label = tk.Label(self.login_frame, text="Library Management System", font=("Helvetica", 18, "bold"), bg='#ffffff', fg='#333333')
        self.login_label.pack(pady=10)

        # Username Entry
        self.username_label = tk.Label(self.login_frame, text="Username", font=("Helvetica", 12), bg='#ffffff', fg='#333333')
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame, font=("Helvetica", 12))
        self.username_entry.pack(pady=5)

        # Password Entry
        self.password_label = tk.Label(self.login_frame, text="Password", font=("Helvetica", 12), bg='#ffffff', fg='#333333')
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, font=("Helvetica", 12), show="*")
        self.password_entry.pack(pady=5)

        # Login Button
        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, font=("Helvetica", 12, "bold"), bg='#4CAF50', fg='white', padx=10, pady=5)
        self.login_button.pack(pady=10)

        # Register Button
        self.register_button = tk.Button(self.login_frame, text="Register", command=self.register, font=("Helvetica", 12, "bold"), bg='#2196F3', fg='white', padx=10, pady=5)
        self.register_button.pack(pady=5)

        # Reset System Button
        self.reset_button = tk.Button(self.master, text="Reset System", command=self.reset_system, font=("Helvetica", 12), bg='red', fg='white', padx=10, pady=5)
        self.reset_button.pack(pady=10)

    def initialize_db(self):
        # Create tables for librarians and books
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
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS issued_books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER,
                FOREIGN KEY(book_id) REFERENCES books(id)
            )
        """)
        self.conn.commit()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.cursor.execute("SELECT * FROM librarians WHERE username = ? AND password = ?", (username, password))
        librarian = self.cursor.fetchone()
        if librarian:
            self.clear_login_screen()
            self.create_sections()  # Show sections after login
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
            self.cursor.execute("DELETE FROM issued_books")
            self.conn.commit()
            messagebox.showinfo("Success", "System reset successfully.")

    def clear_login_screen(self):
        # Remove login screen elements
        self.login_label.pack_forget()
        self.username_label.pack_forget()
        self.username_entry.pack_forget()
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.login_button.pack_forget()
        self.register_button.pack_forget()
        self.reset_button.pack_forget()
        self.login_frame.pack_forget()

    def create_sections(self):
        # Frame for Book Management Section
        self.book_management_frame = tk.Frame(self.master, bg='#f0f0f0', padx=20, pady=20)
        self.book_management_frame.pack(side="left", fill="both", expand=True)

        # Book Management Section
        self.book_title_label = tk.Label(self.book_management_frame, text="Book Title", font=("Helvetica", 12), bg='#f0f0f0', fg='#333333')
        self.book_title_label.pack()
        self.book_title_entry = tk.Entry(self.book_management_frame, font=("Helvetica", 12))
        self.book_title_entry.pack()

        self.book_author_label = tk.Label(self.book_management_frame, text="Author", font=("Helvetica", 12), bg='#f0f0f0', fg='#333333')
        self.book_author_label.pack()
        self.book_author_entry = tk.Entry(self.book_management_frame, font=("Helvetica", 12))
        self.book_author_entry.pack()

        self.book_isbn_label = tk.Label(self.book_management_frame, text="ISBN", font=("Helvetica", 12), bg='#f0f0f0', fg='#333333')
        self.book_isbn_label.pack()
        self.book_isbn_entry = tk.Entry(self.book_management_frame, font=("Helvetica", 12))
        self.book_isbn_entry.pack()

        self.book_year_label = tk.Label(self.book_management_frame, text="Year", font=("Helvetica", 12), bg='#f0f0f0', fg='#333333')
        self.book_year_label.pack()
        self.book_year_entry = tk.Entry(self.book_management_frame, font=("Helvetica", 12))
        self.book_year_entry.pack()

        self.add_book_button = tk.Button(self.book_management_frame, text="Add Book", command=self.add_book, font=("Helvetica", 12, "bold"), bg='#4CAF50', fg='white', padx=10, pady=5)
        self.add_book_button.pack(pady=5)

        self.remove_book_label = tk.Label(self.book_management_frame, text="Remove Book by Title", font=("Helvetica", 12), bg='#f0f0f0', fg='#333333')
        self.remove_book_label.pack()
        self.remove_book_entry = tk.Entry(self.book_management_frame, font=("Helvetica", 12))
        self.remove_book_entry.pack()
        self.remove_book_button = tk.Button(self.book_management_frame, text="Remove Book", command=self.remove_book, font=("Helvetica", 12, "bold"), bg='red', fg='white', padx=10, pady=5)
        self.remove_book_button.pack(pady=5)

        # Frame for Book List Section
        self.book_list_frame = tk.Frame(self.master, bg='#f0f0f0', padx=20, pady=20)
        self.book_list_frame.pack(side="right", fill="both", expand=True)

        self.view_books_button = tk.Button(self.book_list_frame, text="View Book List", command=self.view_books, font=("Helvetica", 12, "bold"), bg='#2196F3', fg='white', padx=10, pady=5)
        self.view_books_button.pack(pady=10)

        self.books_display = tk.Text(self.book_list_frame, font=("Helvetica", 12), height=20, width=40)
        self.books_display.pack(pady=10)

    def add_book(self):
        title = self.book_title_entry.get()
        author = self.book_author_entry.get()
        isbn = self.book_isbn_entry.get()
        year = self.book_year_entry.get()

        self.cursor.execute("INSERT INTO books (title, author, isbn, year) VALUES (?, ?, ?, ?)", (title, author, isbn, year))
        self.conn.commit()
        messagebox.showinfo("Success", "Book added successfully")
        self.book_title_entry.delete(0, tk.END)
        self.book_author_entry.delete(0, tk.END)
        self.book_isbn_entry.delete(0, tk.END)
        self.book_year_entry.delete(0, tk.END)

    def remove_book(self):
        title = self.remove_book_entry.get()
        self.cursor.execute("DELETE FROM books WHERE title = ?", (title,))
        self.conn.commit()
        messagebox.showinfo("Success", "Book removed successfully")
        self.remove_book_entry.delete(0, tk.END)

    def view_books(self):
        self.books_display.delete(1.0, tk.END)  # Clear current display
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()
        if books:
            for book in books:
                book_details = f"Title: {book[1]}, Author: {book[2]}, ISBN: {book[3]}, Year: {book[4]}\n"
                self.books_display.insert(tk.END, book_details)
        else:
            self.books_display.insert(tk.END, "No books available.\n")

    def __del__(self):
        # Close the database connection when the program terminates
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagement(root)
    root.mainloop()

import sqlite3
from book import Book, Comic
from person import Person
import datetime

class Library:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)

    def initialize_database(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                is_available INTEGER DEFAULT 1,
                borrower_id INTEGER DEFAULT NULL,
                illustrator TEXT DEFAULT NULL -- NULL indicates it's not a comic
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persons (
                person_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowings (
            borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            person_id INTEGER NOT NULL,
            borrowed_date TEXT NOT NULL,
            returned_date TEXT DEFAULT NULL,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (person_id) REFERENCES persons(person_id)
        )
        """)
        self.conn.commit()

    def add_comic(self, title, author, illustrator):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, illustrator)
            VALUES (?, ?, ?)
        """, (title, author, illustrator))
        self.conn.commit()

    def add_book(self, title, author):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author)
            VALUES (?, ?)
        """, (title, author))
        self.conn.commit()

    def add_person(self, name, email):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO persons (name, email) VALUES (?, ?)", (name, email))
        self.conn.commit()

    def borrow_book(self, book_id, person_id):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM persons WHERE person_id = ?", (person_id,))
        person = cursor.fetchone()
        if not person:
            return f"Person with ID {person_id} does not exist."

        cursor.execute("SELECT is_available FROM books WHERE book_id = ?", (book_id,))
        result = cursor.fetchone()

        if result and result[0] == 1:
            borrowed_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                UPDATE books
                SET is_available = 0
                WHERE book_id = ?
            """, (book_id,))
            cursor.execute("""
                INSERT INTO borrowings (book_id, person_id, borrowed_date)
                VALUES (?, ?, ?)
            """, (book_id, person_id, borrowed_date))
            self.conn.commit()
            return "Book borrowed successfully."
        elif result:
            return "Book is already borrowed."
        return "Book not found."

    def return_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM borrowings WHERE book_id = ? AND returned_date IS NULL", (book_id,))
        borrowing = cursor.fetchone()
        if borrowing:
            returned_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
                UPDATE books
                SET is_available = 1
                WHERE book_id = ?
            """, (book_id,))
            cursor.execute("""
                UPDATE borrowings
                SET returned_date = ?
                WHERE borrowing_id = ?
            """, (returned_date, borrowing[0]))
            self.conn.commit()
            return "Book returned successfully."
        return "Book is not borrowed."
    

    def list_borrowings(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.borrowing_id, b.book_id, p.person_id, b.borrowed_date, b.returned_date
            FROM borrowings b
            JOIN persons p ON b.person_id = p.person_id
            ORDER BY b.borrowed_date DESC
        """)
        return cursor.fetchall()

    def list_books(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT book_id, title, author, is_available, borrower_id, illustrator
            FROM books
        """)
        rows = cursor.fetchall()
        books = []
        for row in rows:
            if row[5]: 
                book = Comic(row[1], row[2], row[0], row[5])
            else:
                book = Book(row[1], row[2], row[0])
            book._is_available = bool(row[3]) 
            books.append(book)
        return books


    def list_persons(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM persons")
        rows = cursor.fetchall()
        persons = [Person(row[1], row[0], row[2]) for row in rows]
        return persons

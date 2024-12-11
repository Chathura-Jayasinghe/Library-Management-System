from library_item import LibraryItem

class Book(LibraryItem):
    def __init__(self, title, author, book_id):
        self.title = title
        self.author = author
        self.book_id = book_id
        self._is_available = True
        self.borrower = None

    def get_item_info(self):
        return f"Title: {self.title}, Author: {self.author}, ID: {self.book_id}"

    def check_availability(self):
        return "Available" if self._is_available else "Not Available"


class Comic(Book):
    def __init__(self, title, author, book_id, illustrator):
        super().__init__(title, author, book_id)
        self.illustrator = illustrator 

    def get_item_info(self):
        basic_info = super().get_item_info()
        return f"{basic_info}, Illustrator: {self.illustrator}"
    
    def check_availability(self):
        return "Available" if self._is_available else "Not Available"

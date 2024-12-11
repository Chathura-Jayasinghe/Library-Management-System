from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library
from book import Book, Comic
from person import Person

app = FastAPI()
library = Library()
library.initialize_database()

class AddBook(BaseModel):
    title: str
    author: str
    illustrator: str = None 

class BorrowReturn(BaseModel):
    book_id: int
    person_id: int = None  

class AddPerson(BaseModel):
    name: str
    email: str

@app.post("/add_book/")
def add_book(item: AddBook):
    if item.illustrator:
        library.add_comic(item.title, item.author, item.illustrator)
        return {"message": f"Comic '{item.title}' added successfully."}
    else:
        library.add_book(item.title, item.author)
        return {"message": f"Book '{item.title}' added successfully."}

@app.post("/add_person/")
def add_person(item: AddPerson):
    library.add_person(item.name, item.email)
    return {"message": f"Person '{item.name}' added successfully."}

@app.post("/borrow_book/")
def borrow_book(data: BorrowReturn):
    message = library.borrow_book(data.book_id, data.person_id)
    if "not found" in message.lower():
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}

@app.post("/return_book/")
def return_book(data: BorrowReturn):
    message = library.return_book(data.book_id)
    if "not borrowed" in message.lower():
        raise HTTPException(status_code=404, detail=message)
    return {"message": message}

@app.get("/list_books/")
def list_books():
    books = library.list_books()
    return [
        {
            "id": book.book_id,
            "title": book.title,
            "author": book.author,
            "availability": book.check_availability(),
            "illustrator": getattr(book, "illustrator", None),
        }
        for book in books
    ]

@app.get("/list_persons/")
def list_persons():
    persons = library.list_persons()
    return [
        {"id": person.person_id, "name": person.name, "email": person.email}
        for person in persons
    ]

import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Library Management System")

tabs = st.tabs(["Add Book/Comic", "Borrow Book", "Return Book", "View Books", "Manage Members"])

with tabs[0]:
    st.header("Add Book/Comic")
    title = st.text_input("Title")
    author = st.text_input("Author")
    is_comic = st.checkbox("Is this a Comic?")
    illustrator = st.text_input("Illustrator (Only for Comics)") if is_comic else None

    if st.button("Add Book/Comic"):
        data = {"title": title, "author": author}
        if is_comic and illustrator:  
            data["illustrator"] = illustrator
        
        response = requests.post(f"{BASE_URL}/add_book/", json=data)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(f"Error: {response.status_code}, Response: {response.text}")


# Borrow Book
with tabs[1]:
    st.header("Borrow Book")
    book_id = st.number_input("Book ID", min_value=1, step=1)
    person_id = st.number_input("Person ID", min_value=1, step=1)
    if st.button("Borrow Book"):
        data = {"book_id": book_id, "person_id": person_id}
        response = requests.post(f"{BASE_URL}/borrow_book/", json=data)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

# Return Book
with tabs[2]:
    st.header("Return Book")
    book_id = st.number_input("Book ID to Return", min_value=1, step=1)
    if st.button("Return Book"):
        data = {"book_id": book_id}
        response = requests.post(f"{BASE_URL}/return_book/", json=data)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

# View Books
with tabs[3]:
    st.header("Available Books and Comics")
    response = requests.get(f"{BASE_URL}/list_books/")
    if response.status_code == 200:
        books = response.json()
        for book in books:
            book_info = f"ID: {book['id']}, Title: {book['title']}, Author: {book['author']}, {book['availability']}"
            if book.get("illustrator"):
                book_info += f", Illustrator: {book['illustrator']}"
            st.write(book_info)
    else:
        st.error("Error retrieving books.")

# Manage Members
with tabs[4]:
    st.header("Add Member")
    name = st.text_input("Name")
    email = st.text_input("Email")
    if st.button("Add Member"):
        data = {"name": name, "email": email}
        response = requests.post(f"{BASE_URL}/add_person/", json=data)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

    st.header("View Members")
    response = requests.get(f"{BASE_URL}/list_persons/")
    if response.status_code == 200:
        persons = response.json()
        for person in persons:
            st.write(f"ID: {person['id']}, Name: {person['name']}, Email: {person['email']}")
    else:
        st.error("Error retrieving members.")


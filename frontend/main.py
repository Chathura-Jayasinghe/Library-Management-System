import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.title("Library Management System")

tabs = st.tabs(["Add Book", "Borrow Book", "Return Book", "View Books", "Manage Members", "Borrowings"])

# Add book
with tabs[0]:
    st.header("Add Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    is_comic = st.checkbox("Is this a Comic?")
    illustrator = st.text_input("Illustrator (Only for Comics)") if is_comic else None

    if st.button("Add Book"):
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
        
        if books:
            table_data = []
            for book in books:
                row = {
                    "ID": book["id"],
                    "Title": book["title"],
                    "Author": book["author"],
                    "Availability": book["availability"],
                    "Illustrator": book.get("illustrator", "N/A") 
                }
                table_data.append(row)
            
            st.table(table_data) 
        else:
            st.write("No books or comics available.")
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
        
        if persons:
            table_data = []
            for person in persons:
                row = {
                    "ID": person["id"],
                    "Name": person["name"],
                    "Email": person["email"]
                }
                table_data.append(row)
            
            st.table(table_data) 
        else:
            st.write("No members available.")
    else:
        st.error("Error retrieving members.")

# View Borrowings
with tabs[5]:
    st.header("Borrowings")

    response = requests.get(f"{BASE_URL}/list_borrowings/")
    if response.status_code == 200:
        borrowings = response.json()
        
        if borrowings:
            table_data = []
            for borrowing in borrowings:
                row = {
                    "Borrowing ID": borrowing["borrowing_id"],
                    "Book ID": borrowing["book_id"],
                    "Person ID": borrowing["person_id"],
                    "Borrowed Date": borrowing.get("borrowed_date", "N/A"),
                    "Returned Date": borrowing.get("returned_date", "N/A")
                }
                table_data.append(row)
            
            st.table(table_data)
        else:
            st.write("No borrowings available.")
    else:
        st.error("Error retrieving borrowings.")

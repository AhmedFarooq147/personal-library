import streamlit as st  # type: ignore
import json

st.set_page_config(page_title="Personal Library", page_icon=":books:", layout="wide")

st.title("Personal Library")
st.markdown("""
            <style>
            div.stButton > button{
                background-color: #ff6347;
                color: white;
                font-size: 18px;
                border-radius: 8px;
                padding: 12px 24px;
                transition: 0.3s;
            }
            div.stButton > button:hover{
                background-color: #ff4500;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True)

def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_library(library):
    with open("library.json", "w") as file:
        json.dump(library, file)

library = load_library()

choice = st.sidebar.radio("Choose an option:", ["Add Book", "Remove Book", "Display Books","Search Books","Display statistics","Exit"])

def add_book():
    title = st.text_input("Enter the title of the book:")
    author = st.text_input("Enter the author of the book:")
    publication_year = st.number_input("Enter the publication year of the book:", min_value=1000, max_value=2025, value=2024)
    genre = st.text_input("Enter the genre of the book:")
    read_status = st.selectbox("Enter the read status of the book:", ["Not Read", "Read"])
    if st.button("Add Book" ):
        if title and author and publication_year and genre and read_status:
            item = {
                "title": title,
                "author": author,
                "publication year": publication_year,
                "genre": genre,
                "read status": read_status
            }
            library.append(item)
            save_library(library)
            st.success(f"Book {title} added successfully!")
            time.sleep(2)
            st.rerun()
            
        else:
            st.error("Please fill all the fields")
        


if choice == "Add Book":
    add_book()
   
elif choice == "Remove Book":
    st.subheader("Remove a book from your library")
    book_titles = [book["title"] for book in library]
    if book_titles:
        selected_title = st.selectbox("Select a book to remove:", book_titles)
        if st.button("Remove Book"):
            library = [book for book in library if book["title"] != selected_title]
            save_library(library)
            st.success(f"Book {selected_title} removed successfully!")
            time.sleep(2)
            st.rerun()
    else:
        st.warning("No books in the library!")
        
elif choice == "Search Books":
    st.subheader("Search for a book in your library")
    search = st.text_input("Enter the title/author of the book:")
    if st.button("Search"):
        results = [book for book in library if search in book["title"] or search in book["author"]]
        if results:
            st.table(results)
        else:
            st.warning("No books found!")
    
elif choice == "Display Books":
    st.subheader("Display all books in your library")
    if library:
        st.table(library)
    else:
        st.warning("No books in the library!")
elif choice == "Display statistics":
    st.subheader("Display statistics of your library")
    if library:
        total_books = len(library)
        read_books = sum(1 for book in library if book["read status"] == "Read")
        not_read_books = total_books - read_books
        st.success(f"Total books: {total_books}")
        st.success(f"Read books: {read_books}")
        st.success(f"Not read books: {not_read_books}")
    else:
        st.warning("No books in the library!")

elif choice == "Exit":
    st.subheader("Exit the library")
    if st.button("Exit"):
        st.success("Thank you for using the library!")
        st.stop()
        

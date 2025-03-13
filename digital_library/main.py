import streamlit as st
import pymongo
from datetime import date, timedelta
import sys
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(
    page_title="Library Management System",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📚"
)

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def connect_to_database():
    connection_string = st.secrets["MONGO_URI"]
    # connection_string = "mongodb+srv://<username>:<password>@digitallibrary.a6oks.mongodb.net/?retryWrites=true&w=majority&appName=DigitalLibrary"
    try:
        client = pymongo.MongoClient(connection_string)
        db = client["LibraryDB"]
        return client, db
    except pymongo.errors.ConnectionError:
        st.error("Error: Could not connect to database")
        sys.exit(1)

def home_page(db):
    st.title("📚 Library Management System")
    
    col1, col2, col3= st.columns(3,)
    
    total_books = db.books.count_documents({})
    available_books = db.books.count_documents({"availability": "Available"})
    issued_books = db.issuedBooks.count_documents({})
    
    with col1:
        st.metric("Total Books", total_books)
    with col2:
        st.metric("Available Books", available_books)
    with col3:
        st.metric("Issued Books", issued_books)

    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📖 Recently Added Books")
        recent_books = list(db.books.find().sort("_id", -1).limit(5))
        if recent_books:
            for book in recent_books:
                with st.expander(f"{book['bookName']}"):
                    st.write(f"🖊️ Author: {book['authorName']}")
                    st.write(f"📑 ISBN: {book['isbn']}")
                    status_color = "green" if book['availability'] == "Available" else "red"
                    st.markdown(f"Status: <span style='color:{status_color}'>{book['availability']}</span>", 
                              unsafe_allow_html=True)
        else:
            st.info("No books added recently")

    with col2:
        st.markdown("### 📋 Recently Issued Books")
        recent_issues = list(db.issuedBooks.find().sort("_id", -1).limit(5))
        if recent_issues:
            for book in recent_issues:
                with st.expander(f"{book['bookName']}"):
                    st.write(f"👤 Borrowed by: {book['name']}")
                    st.write(f"📞 Contact: {book['phone']}")
                    st.write(f"📅 Due Date: {book['dateDue']}")
        else:
            st.info("No recent book issues")

def add_book(db):
    st.header("Add New Book")
    with st.form("add_book_form"):
        bookName = st.text_input("Book Name")
        authorName = st.text_input("Author Name")
        isbn = st.text_input("ISBN")
        cover_image = st.file_uploader("Upload Book Cover", type=['jpg', 'jpeg', 'png'])
        
        submitted = st.form_submit_button("Add Book")
        
        if submitted:
            if not bookName or not authorName or not isbn:
                st.error("Please fill all fields")
            elif not isbn.isdigit():
                st.error("Error: ISBN must be numeric")
            elif db.books.find_one({"isbn": isbn}):
                st.error("Error: Book with this ISBN already exists")
            else:
                image_data = None
                if cover_image is not None:
                    # Open the image using PIL
                    img = Image.open(cover_image)
                    
                    # Resize image to a reasonable size (e.g., max 800px width)
                    max_width = 800
                    if img.size[0] > max_width:
                        ratio = max_width / img.size[0]
                        new_size = (max_width, int(img.size[1] * ratio))
                        img = img.resize(new_size)
                    
                    # Convert image to base64
                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    image_data = base64.b64encode(buffered.getvalue()).decode()

                book_doc = {
                    "bookName": bookName,
                    "authorName": authorName,
                    "isbn": isbn,
                    "availability": "Available",
                    "cover_image": image_data,
                    "dateAdded": date.today().isoformat()
                }
                
                db.books.insert_one(book_doc)
                st.success("Book added successfully!")

def view_books(db):
    st.header("Books in Library")
    

    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search by book name or author")
    with col2:
        status_filter = st.selectbox("Filter by status", ["All", "Available", "Issued"])
    
    query = {}
    if search:
        query["$or"] = [
            {"bookName": {"$regex": search, "$options": "i"}},
            {"authorName": {"$regex": search, "$options": "i"}}
        ]
    if status_filter != "All":
        query["availability"] = status_filter
    
    books = list(db.books.find(query))
    if not books:
        st.info("No books found matching your criteria")
    else:
        cols = st.columns(3)
        for idx, book in enumerate(books):
            with cols[idx % 3]:
                with st.expander(f"{book['bookName']}",expanded=True):
                    if book.get('cover_image'):
                        st.image(
                            f"data:image/jpeg;base64,{book['cover_image']}", 
                            caption=book['bookName'],
                            use_container_width=True
                        )
                    else:
                        st.info("📸 - Image not found!")
                    
                    st.write(f"Author: {book['authorName']}")
                    st.write(f"ISBN: {book['isbn']}")
                    status_color = "green" if book['availability'] == "Available" else "red"
                    st.markdown(
                        f"Status: <span style='color:{status_color}'>{book['availability']}</span>", 
                        unsafe_allow_html=True
                    )


def issue_book(db):
    st.header("Issue Book")
    
    available_books = list(db.books.find({"availability": "Available"}))
    
    if not available_books:
        st.warning("No books are currently available for issuing.")
        return
    
    book_options = [f"{book['bookName']} - {book['authorName']} (ISBN: {book['isbn']})" for book in available_books]
    
    book_options.insert(0, "Select a book")
    selected_book = st.selectbox("Select Book to Issue", book_options)

    if selected_book != "Select a book":
        # Extract ISBN from the selected option
        isbn = selected_book.split("ISBN: ")[-1][:-1]  # Remove the closing parenthesis
        
        book = db.books.find_one({"isbn": isbn})
        
        col1, col2 = st.columns(2)
        with col1:
            if book.get('cover_image'):
                st.image(
                    f"data:image/jpeg;base64,{book['cover_image']}", 
                    caption=book['bookName'],
                )
        with col2:
            st.write(f"**Author:** {book['authorName']}")
            st.write(f"**ISBN:** {book['isbn']}")
        
        with st.form("issue_book_form"):
            st.markdown("### Borrower Details")
            name = st.text_input("Borrower's Name")
            email = st.text_input("Borrower's Email")
            phone = st.text_input("Borrower's Phone")
            for_days = st.slider("Number of days to issue", 1, 30, 7)
            
            submitted = st.form_submit_button("Issue Book")
            
            if submitted:
                if not all([name, email, phone]):
                    st.error("Please fill all borrower details")
                else:
                    book = db.books.find_one({"isbn": isbn})
                    if not book:
                        st.error("Book not found")
                    elif book.get("availability") != "Available":
                        st.error("Book is no longer available")
                    else:
                        dateIssued = date.today()
                        dateDue = dateIssued + timedelta(days=for_days)
                        
                        db.issuedBooks.insert_one({
                            "bookName": book["bookName"],
                            "authorName": book["authorName"],
                            "isbn": isbn,
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "dateIssued": dateIssued.strftime("%d/%m/%Y"),
                            "dateDue": dateDue.strftime("%d/%m/%Y")
                        })
                        
                        db.books.update_one(
                            {"isbn": isbn},
                            {"$set": {"availability": "Issued"}}
                        )
                        
                        st.success("Book issued successfully!")
                        
                        st.markdown("### Issue Details")
                        st.write(f"Book: {book['bookName']}")
                        st.write(f"Issued to: {name}")
                        st.write(f"Issue Date: {dateIssued.strftime('%d/%m/%Y')}")
                        st.write(f"Due Date: {dateDue.strftime('%d/%m/%Y')}")


def return_book(db):
    st.header("Return Book")
    isbn = st.text_input("Enter ISBN of book to return")
    if isbn:
        issued_book = db.issuedBooks.find_one({"isbn": isbn})
        if issued_book:
            st.write("Book Details:")
            st.write(f"Book Name: {issued_book['bookName']}")
            st.write(f"Borrowed by: {issued_book['name']}")
            st.write(f"Due Date: {issued_book['dateDue']}")
            
            if st.button("Confirm Return"):
                db.issuedBooks.delete_one({"isbn": isbn})
                db.books.update_one(
                    {"isbn": isbn},
                    {"$set": {"availability": "Available"}}
                )
                st.success("Book returned successfully!")
        else:
            st.error("This book is not issued")

def view_issued_books(db):
    st.header("Issued Books")
    if db.issuedBooks.count_documents({}) == 0:
        st.info("No books are currently issued")
    else:
        search = st.text_input("🔍 Search by borrower name or book name")
        query = {}
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"bookName": {"$regex": search, "$options": "i"}}
            ]
            
        for book in db.issuedBooks.find(query):
            with st.expander(f"{book['bookName']} - {book['isbn']}"):
                st.write(f"Author: {book['authorName']}")
                st.write(f"ISBN: {book['isbn']}")
                st.write(f"Borrowed by: {book['name']}")
                st.write(f"Contact: {book['phone']}")
                st.write(f"Issue Date: {book['dateIssued']}")
                st.write(f"Due Date: {book['dateDue']}")

def delete_book(db):
    st.header("Delete Book")
    isbn = st.text_input("Enter ISBN of book to delete")
    if isbn:
        book = db.books.find_one({"isbn": isbn})
        if book:
            st.write("Book Details:")
            st.write(f"Book Name: {book['bookName']}")
            st.write(f"Author: {book['authorName']}")
            
            if book.get("availability") == "Issued":
                st.error("Cannot delete: Book is currently issued")
            elif st.button("Confirm Delete"):
                db.books.delete_one({"isbn": isbn})
                st.success("Book deleted successfully!")
        else:
            st.error("Book not found")

def main():
    _ , db = connect_to_database()
    
    st.sidebar.title("Navigation")
    
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    if st.sidebar.button("Home"):
        st.session_state.page = 'home'
    if st.sidebar.button("➕ Add Book"):
        st.session_state.page = 'add_book'
    if st.sidebar.button("📚 View Books"):
        st.session_state.page = 'view_books'
    if st.sidebar.button("📖 Issue Book"):
        st.session_state.page = 'issue_book'
    if st.sidebar.button("↩️ Return Book"):
        st.session_state.page = 'return_book'
    if st.sidebar.button("📋 View Issued Books"):
        st.session_state.page = 'view_issued'
    if st.sidebar.button("🗑️ Delete Book"):
        st.session_state.page = 'delete_book'
    
    if st.session_state.page == 'home':
        home_page(db)
    elif st.session_state.page == 'add_book':
        add_book(db)
    elif st.session_state.page == 'view_books':
        view_books(db)
    elif st.session_state.page == 'issue_book':
        issue_book(db)
    elif st.session_state.page == 'return_book':
        return_book(db)
    elif st.session_state.page == 'view_issued':
        view_issued_books(db)
    elif st.session_state.page == 'delete_book':
        delete_book(db)
    
    st.sidebar.markdown("---")
    st.sidebar.info("Developed with ❤️ by Anas Ahmed")

if __name__ == "__main__":
    main()

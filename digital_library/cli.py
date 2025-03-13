import pymongo
from datetime import date, timedelta
import sys
from dotenv import load_dotenv
import os

# Database connection
def connect_to_database():
    load_dotenv()
    connection_string = os.getenv("MONGO_URI")
    try:
        client = pymongo.MongoClient(connection_string)
        db = client["LibraryDB"]
        return client, db
    except pymongo.errors.ConnectionError:
        print("Error: Could not connect to database")
        sys.exit(1)

def add_book(db):
    print("\n=== Add New Book ===")
    try:
        bookName = input("Enter book name: ")
        authorName = input("Enter author name: ")
        isbn = input("Enter ISBN: ")
        
        if not isbn.isdigit():
            print("Error: ISBN must be numeric")
            return
            
        if db.books.find_one({"isbn": isbn}):
            print("Error: Book with this ISBN already exists")
            return
        
        db.books.insert_one({
            "bookName": bookName,
            "authorName": authorName,
            "isbn": isbn,
            "availability": "Available"
        })
        print("Book added successfully!")
    except Exception as e:
        print(f"Error adding book: {str(e)}")

def view_books(db):
    print("\n=== Books in Library ===")
    if db.books.count_documents({}) == 0:
        print("No books in library")
        return
        
    for book in db.books.find():
        print(f"\nBook Name: {book.get('bookName')}")
        print(f"Author: {book.get('authorName')}")
        print(f"ISBN: {book.get('isbn')}")
        print(f"Status: {book.get('availability')}")
        print("-" * 30)

def search_book(db):
    print("\n=== Search Book ===")
    search_term = input("Enter book name or ISBN: ")
    
    query = {
        "$or": [
            {"isbn": search_term},
            {"bookName": {"$regex": search_term, "$options": "i"}}
        ]
    }
    
    if db.books.count_documents(query) == 0:
        print("No matching books found")
        return
    
    for book in db.books.find(query):
        print(f"\nBook Name: {book.get('bookName')}")
        print(f"Author: {book.get('authorName')}")
        print(f"ISBN: {book.get('isbn')}")
        print(f"Status: {book.get('availability')}")
        print("-" * 30)

def issue_book(db):
    print("\n=== Issue Book ===")
    isbn = input("Enter ISBN of book to issue: ")
    
    book = db.books.find_one({"isbn": isbn})
    if not book:
        print("Book not found")
        return
        
    if book.get("availability") != "Available":
        print("Book is already issued")
        return
        
    name = input("Enter borrower's name: ")
    email = input("Enter borrower's email: ")
    phone = input("Enter borrower's phone: ")
    
    while True:
        try:
            for_days = int(input("Enter number of days to issue (1-30): "))
            if 1 <= for_days <= 30:
                break
            print("Please enter a number between 1 and 30")
        except ValueError:
            print("Please enter a valid number")
    
    dateIssued = date.today()
    dateDue = dateIssued + timedelta(days=for_days)
    
    try:
        db.issuedBooks.insert_one({
            "bookName": book.get("bookName"),
            "authorName": book.get("authorName"),
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
        print("Book issued successfully!")
    except Exception as e:
        print(f"Error issuing book: {str(e)}")

def return_book(db):
    print("\n=== Return Book ===")
    isbn = input("Enter ISBN of book to return: ")
    
    issued_book = db.issuedBooks.find_one({"isbn": isbn})
    if not issued_book:
        print("This book is not issued")
        return
        
    try:
        db.issuedBooks.delete_one({"isbn": isbn})
        db.books.update_one(
            {"isbn": isbn},
            {"$set": {"availability": "Available"}}
        )
        print("Book returned successfully!")
    except Exception as e:
        print(f"Error returning book: {str(e)}")

def view_issued_books(db):
    print("\n=== Issued Books ===")
    if db.issuedBooks.count_documents({}) == 0:
        print("No books are currently issued")
        return
        
    for book in db.issuedBooks.find():
        print(f"\nBook Name: {book.get('bookName')}")
        print(f"Author: {book.get('authorName')}")
        print(f"ISBN: {book.get('isbn')}")
        print(f"Borrowed by: {book.get('name')}")
        print(f"Contact: {book.get('phone')}")
        print(f"Issue Date: {book.get('dateIssued')}")
        print(f"Due Date: {book.get('dateDue')}")
        print("-" * 30)

def delete_book(db):
    print("\n=== Delete Book ===")
    isbn = input("Enter ISBN of book to delete: ")
    
    book = db.books.find_one({"isbn": isbn})
    if not book:
        print("Book not found")
        return
        
    if book.get("availability") == "Issued":
        print("Cannot delete: Book is currently issued")
        return
        
    try:
        db.books.delete_one({"isbn": isbn})
        print("Book deleted successfully!")
    except Exception as e:
        print(f"Error deleting book: {str(e)}")

def display_menu():
    print("\n=== Library Management System ===")
    print("1. Add Book")
    print("2. View All Books")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. View Issued Books")
    print("7. Delete Book")
    print("8. Exit")
    return input("Enter your choice (1-8): ")

def main():
    try:
        client, db = connect_to_database()
        
        while True:
            choice = display_menu()
            
            if choice == "1":
                add_book(db)
            elif choice == "2":
                view_books(db)
            elif choice == "3":
                search_book(db)
            elif choice == "4":
                issue_book(db)
            elif choice == "5":
                return_book(db)
            elif choice == "6":
                view_issued_books(db)
            elif choice == "7":
                delete_book(db)
            elif choice == "8":
                print("\nThank you for using the Library Management System!")
                break
            else:
                print("\nInvalid choice. Please try again.")
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    main()
# 📚 Library Management System

A modern, web-based library management system built with Streamlit and MongoDB. This application provides an intuitive interface for managing books, issuing/returning books, and tracking library inventory.

## Live Demo

🌐 Check out the live application: [Digital Library](https://digital-library.streamlit.app)

## Features

- 📊 Dashboard with key metrics
- 📚 Book management (add, view, delete)
- 📖 Book issuing and return system
- 🔍 Search functionality
- 📱 Responsive design
- 🖼️ Book cover image support
- 📋 Issued book tracking system

## Technologies Used

- Python
- Streamlit
- MongoDB
- PIL (Python Imaging Library)
- PyMongo

## Installation

1. Clone the repository:
```bash
git clone https://github.com/anasahmed07/python-projects.git
cd digital-library
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB:
   - Create a MongoDB Atlas account or use a local MongoDB instance
   - Create a `.streamlit/secrets.toml` file with your MongoDB connection string:
```toml
MONGO_URI = "your_mongodb_connection_string"
```

4. Run the application:
```bash
streamlit run main.py
```

## Usage

### Navigation
- **Home**: View dashboard with key metrics and recent activities
- **Add Book**: Add new books to the library with cover images
- **View Books**: Browse and search the book collection
- **Issue Book**: Issue books to borrowers
- **Return Book**: Process book returns
- **View Issued Books**: Track currently issued books
- **Delete Book**: Remove books from the system

### Book Management
- Add books with details like name, author, ISBN, and cover image
- Search books by name or author
- Filter books by availability status
- View book details including cover images

### Borrowing System
- Issue books with borrower details
- Set custom borrowing duration
- Track due dates
- Process returns

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

Developed with ❤️ by Anas Ahmed

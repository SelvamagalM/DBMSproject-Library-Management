# Public Library Management System - Web Application

A modern, responsive web application for managing public library operations built with Python Flask and SQLite.

## Features

### 🏠 Dashboard
- Real-time statistics showing:
  - Total books in library
  - Active members
  - Active borrowings
  - Overdue book count
  - Available books
  - Outstanding fines
  - Pending reservations
- Quick action buttons for common tasks

### 📚 Books Management
- Add new books with ISBN, title, author, publisher, year, and quantity
- Search books by title, author, or ISBN
- View all books with availability status
- Track total and available quantities

### 👥 Members Management
- Register new members with name, email, phone, and address
- View all active members
- View individual member profiles
- Access member borrowing history
- Track fines for each member

### 📖 Borrowing & Returns
- Issue books to members with customizable borrowing period
- Return books with automatic fine calculation
- Fine: **Rs. 2 per day** for overdue books
- View all active borrowings
- Highlight overdue books
- Visual indicators for due date status

### 🔔 Reservations
- Reserve unavailable books
- View reservation queues for each book
- Cancel reservations
- Queue position tracking

### 📊 Reports & Statistics
- **Overdue Books Report**: Lists all overdue books with fines
- **Member Fines Report**: Show members with outstanding fines
- **Borrowing Statistics**: Comprehensive library statistics
- **Top Books Report**: Most borrowed books ranking
- **Quick Stats Cards**: Key metrics at a glance

## Technology Stack

- **Backend**: Python Flask (lightweight web framework)
- **Database**: SQLite (embedded, no external server required)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JS for interactivity
- **Icons**: Font Awesome 6
- **Styling**: Custom CSS with gradients and animations

## Project Structure

```
library_web/
├── app.py                 # Main Flask application
├── db.py                  # Database setup and utilities
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navbar
│   ├── index.html        # Dashboard
│   ├── books.html        # Books management
│   ├── members.html      # Members management
│   ├── member_detail.html # Member details & history
│   ├── borrowing.html    # Borrowing & returns
│   ├── reservations.html # Reservations
│   ├── reports.html      # Reports & statistics
│   ├── 404.html          # 404 error page
│   └── 500.html          # 500 error page
├── static/
│   ├── css/
│   │   └── style.css     # Custom styling
│   └── js/
│       └── main.js       # JavaScript utilities
└── library.db           # SQLite database (created on first run)
```

## Installation

### Prerequisites
- Python 3.7+ installed
- Windows, Mac, or Linux

### Setup Instructions

1. **Navigate to the project directory:**
   ```bash
   cd c:\Users\cmala\.antigravity\library_web
   ```

2. **Create a Python virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open in browser:**
   - Navigate to `http://localhost:5000`
   - The database will be automatically created on first run

## Usage Guide

### 1. Adding Books
1. Go to **Books** page
2. Click "Add New Book" button
3. Fill in book details (title, author, ISBN required)
4. Click "Add Book"

### 2. Registering Members
1. Go to **Members** page
2. Click "Register Member" button
3. Enter member details
4. Click "Register"

### 3. Issuing Books
1. Go to **Borrowing** page
2. Select member and book
3. Set borrowing period (default 14 days)
4. Click "Issue Book"

### 4. Returning Books
1. Go to **Borrowing** page
2. Find the book in active borrowings list
3. Click "Return" button
4. Fine is calculated automatically if overdue

### 5. Reserving Books
1. Go to **Reservations** page
2. Select member and book
3. Click "Reserve Book"
4. View queue position

### 6. Viewing Reports
1. Go to **Reports** page
2. View statistics and reports
3. Check overdue books, member fines, and top borrowed books

## Database Schema

### Tables

#### `books`
- `book_id`: Unique identifier
- `title`, `author`, `isbn` (unique), `publisher`, `publication_year`
- `quantity`, `available_quantity`

#### `members`
- `member_id`: Unique identifier
- `name`, `email` (unique), `phone`, `address`
- `membership_date`, `is_active`

#### `borrowing`
- `borrowing_id`: Unique identifier
- `member_id`, `book_id` (foreign keys)
- `borrowed_date`, `due_date`, `return_date`
- `fine_amount`, `is_returned`

#### `reservations`
- `reservation_id`: Unique identifier
- `member_id`, `book_id` (foreign keys)
- `reservation_date`, `is_fulfilled`

## API Endpoints

### Books
- `GET /books` - View all books page
- `GET /api/books/search?q=<term>` - Search books (JSON)
- `POST /api/books/add` - Add new book (JSON)

### Members
- `GET /members` - View all members
- `GET /members/<id>` - View member details
- `POST /api/members/register` - Register member (JSON)

### Borrowing
- `GET /borrowing` - Borrowing page
- `POST /api/borrowing/issue` - Issue book (JSON)
- `POST /api/borrowing/return` - Return book (JSON)

### Reservations
- `GET /reservations` - Reservations page
- `GET /api/reservations/book/<id>` - Get queue for book (JSON)
- `POST /api/reservations/add` - Add reservation (JSON)
- `POST /api/reservations/cancel/<id>` - Cancel reservation (JSON)

### Reports
- `GET /reports` - View reports page

## Features Highlight

### ✨ Beautiful UI
- Modern gradient design
- Responsive Bootstrap layout
- Smooth animations and transitions
- Card-based dashboard
- Professional color scheme

### 🔒 Data Integrity
- SQLite foreign key constraints enabled
- Unique ISBN and email validation
- Transaction support
- Automatic database creation

### 📱 Responsive Design
- Mobile-friendly interface
- Tablet optimized
- Desktop enhanced
- Touch-friendly buttons and controls

### ⚡ Performance
- Client-side search for books
- Efficient database queries
- Cached static assets
- Minimal page reload

### 🎨 User Experience
- Intuitive navigation
- Clear visual hierarchy
- Error handling with helpful messages
- Success notifications
- Modal forms for data entry

## Configuration

### Default Settings
- **Fine Rate**: Rs. 2 per day (configurable in `app.py`)
- **Default Borrowing Period**: 14 days (configurable in `app.py`)
- **Debug Mode**: True (change to False in production)

### Customization
To customize fine rate or borrowing period:
```python
# In app.py
FINE_PER_DAY = 2      # Rs.2 per day
BORROW_DAYS = 14      # Default 14 days
```

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```python
# In app.py, change:
app.run(debug=True, port=5001)
```

### Database Issues
To reset the database:
1. Delete `library.db`
2. Restart the application
3. Database will be recreated automatically

### Import Errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

## Future Enhancements

- User authentication and admin panel
- Member dashboard
- Email notifications for due dates
- Payment integration for fines
- Book search with filters
- PDF report export
- Multi-language support
- Dark mode
- Mobile app
- Book covers and images
- Advanced analytics

## License

Open Source - Feel free to use and modify

## Support

For issues or questions, check the error messages in the browser console and Flask debug output.

---

**Built with ❤️ using Flask & SQLite**
**Version**: 1.0.0 | **Date**: April 2026

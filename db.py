import sqlite3
import os
from datetime import datetime

DB_PATH = "library.db"

def is_vercel():
    """Check if running on Vercel serverless environment."""
    return os.getenv('VERCEL') == '1'

def create_database():
    """Create the library database with all required tables."""
    # Skip database creation on Vercel (serverless) - use a cloud database instead
    if is_vercel():
        return
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Enable foreign key support
        cursor.execute("PRAGMA foreign_keys = ON")
        
        # Books table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE NOT NULL,
                publisher TEXT,
                publication_year INTEGER,
                genre TEXT,
                quantity INTEGER DEFAULT 1,
                available_quantity INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                membership_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                address TEXT,
                member_type TEXT DEFAULT 'Student',
                is_active INTEGER DEFAULT 1
            )
        """)
        
        # Borrowing table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowing (
                borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrowed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                due_date TIMESTAMP NOT NULL,
                return_date TIMESTAMP,
                fine_amount REAL DEFAULT 0,
                is_returned INTEGER DEFAULT 0,
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)
        
        # Reservations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                reservation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_fulfilled INTEGER DEFAULT 0,
                fulfilled_date TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)
        
        conn.commit()
        conn.close()
    except Exception as e:
        # Database creation failed - likely on serverless environment
        print(f"Database creation failed: {e}")

def get_connection():
    """Get a database connection."""
    if not os.path.exists(DB_PATH):
        create_database()
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def dict_from_row(row):
    """Convert sqlite3.Row to dict."""
    if row is None:
        return None
    return dict(row)

def dict_list_from_rows(rows):
    """Convert list of sqlite3.Row to list of dicts."""
    return [dict(row) for row in rows]

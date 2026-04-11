#!/usr/bin/env python3
"""
Seed data for Library Management System
Inserts sample books, members, borrowing records, and reservations into library.db
"""

import sqlite3
from datetime import datetime, timedelta
import os

DB_PATH = "library.db"

def delete_and_recreate_tables():
    """Delete existing data and recreate tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    # Drop existing tables
    cursor.execute("DROP TABLE IF EXISTS reservations")
    cursor.execute("DROP TABLE IF EXISTS borrowing")
    cursor.execute("DROP TABLE IF EXISTS members")
    cursor.execute("DROP TABLE IF EXISTS books")

    # Recreate tables
    cursor.execute("""
        CREATE TABLE books (
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

    cursor.execute("""
        CREATE TABLE members (
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

    cursor.execute("""
        CREATE TABLE borrowing (
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

    cursor.execute("""
        CREATE TABLE reservations (
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
    print("[OK] Tables recreated successfully")

def insert_books():
    """Insert sample books."""
    books = [
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'isbn': '978-0-06-112008-4',
            'publisher': 'J.B. Lippincott',
            'publication_year': 1960,
            'genre': 'Fiction',
            'quantity': 3,
            'available_quantity': 2
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'isbn': '978-0-452-26423-5',
            'publisher': 'Signet Classics',
            'publication_year': 1949,
            'genre': 'Dystopian Fiction',
            'quantity': 2,
            'available_quantity': 1
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'isbn': '978-0-14-143951-8',
            'publisher': 'Penguin Classics',
            'publication_year': 1813,
            'genre': 'Romance',
            'quantity': 4,
            'available_quantity': 3
        },
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'isbn': '978-0-7432-7356-5',
            'publisher': 'Scribner',
            'publication_year': 1925,
            'genre': 'Fiction',
            'quantity': 3,
            'available_quantity': 2
        },
        {
            'title': 'Sapiens',
            'author': 'Yuval Noah Harari',
            'isbn': '978-0-06-231609-7',
            'publisher': 'Harper',
            'publication_year': 2014,
            'genre': 'Non-fiction',
            'quantity': 2,
            'available_quantity': 1
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'isbn': '978-0-316-76948-0',
            'publisher': 'Little, Brown',
            'publication_year': 1951,
            'genre': 'Fiction',
            'quantity': 3,
            'available_quantity': 3
        },
        {
            'title': 'Python Programming',
            'author': 'Mark Lutz',
            'isbn': '978-1-449-35573-9',
            'publisher': "O'Reilly Media",
            'publication_year': 2013,
            'genre': 'Technology',
            'quantity': 4,
            'available_quantity': 2
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'isbn': '978-0-547-92822-8',
            'publisher': 'Houghton Mifflin Harcourt',
            'publication_year': 1937,
            'genre': 'Fantasy',
            'quantity': 3,
            'available_quantity': 1
        },
        {
            'title': 'Atomic Habits',
            'author': 'James Clear',
            'isbn': '978-0-735-21159-4',
            'publisher': 'Avery',
            'publication_year': 2018,
            'genre': 'Self-help',
            'quantity': 2,
            'available_quantity': 2
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'isbn': '978-0-544-00159-5',
            'publisher': 'Houghton Mifflin Harcourt',
            'publication_year': 1954,
            'genre': 'Fantasy',
            'quantity': 2,
            'available_quantity': 0
        },
        {
            'title': 'Educated',
            'author': 'Tara Westover',
            'isbn': '978-0-399-59065-7',
            'publisher': 'Random House',
            'publication_year': 2018,
            'genre': 'Biography',
            'quantity': 3,
            'available_quantity': 2
        },
        {
            'title': 'Clean Code',
            'author': 'Robert C. Martin',
            'isbn': '978-0-13-235088-4',
            'publisher': 'Prentice Hall',
            'publication_year': 2008,
            'genre': 'Technology',
            'quantity': 2,
            'available_quantity': 1
        }
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for book in books:
        cursor.execute("""
            INSERT INTO books (title, author, isbn, publisher, publication_year, genre, quantity, available_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (book['title'], book['author'], book['isbn'], book['publisher'],
              book['publication_year'], book['genre'], book['quantity'], book['available_quantity']))

    conn.commit()
    conn.close()
    print(f"[OK] Inserted {len(books)} books")

def insert_members():
    """Insert sample members."""
    members = [
        {
            'name': 'Rajesh Kumar',
            'email': 'rajesh.kumar@university.edu',
            'phone': '9876543210',
            'address': '123 Main Street, City A',
            'member_type': 'Student'
        },
        {
            'name': 'Priya Sharma',
            'email': 'priya.sharma@university.edu',
            'phone': '9876543211',
            'address': '456 Oak Avenue, City B',
            'member_type': 'Faculty'
        },
        {
            'name': 'Amit Patel',
            'email': 'amit.patel@university.edu',
            'phone': '9876543212',
            'address': '789 Elm Road, City C',
            'member_type': 'Student'
        },
        {
            'name': 'Neha Singh',
            'email': 'neha.singh@university.edu',
            'phone': '9876543213',
            'address': '321 Pine Lane, City D',
            'member_type': 'Staff'
        },
        {
            'name': 'Vikram Desai',
            'email': 'vikram.desai@university.edu',
            'phone': '9876543214',
            'address': '654 Maple Drive, City E',
            'member_type': 'Faculty'
        },
        {
            'name': 'Anjali Gupta',
            'email': 'anjali.gupta@university.edu',
            'phone': '9876543215',
            'address': '987 Cedar Court, City F',
            'member_type': 'Student'
        }
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for member in members:
        cursor.execute("""
            INSERT INTO members (name, email, phone, address, member_type, membership_date)
            VALUES (?, ?, ?, ?, ?, datetime('2025-06-01'))
        """, (member['name'], member['email'], member['phone'], member['address'], member['member_type']))

    conn.commit()
    conn.close()
    print(f"[OK] Inserted {len(members)} members")

def insert_borrowing_records():
    """Insert sample borrowing records with various statuses."""
    now = datetime.now()

    borrowing_records = [
        # Record 1: Returned on time (no fine)
        {
            'member_id': 1,
            'book_id': 1,
            'borrowed_date': (now - timedelta(days=20)).isoformat(),
            'due_date': (now - timedelta(days=8)).isoformat(),
            'return_date': (now - timedelta(days=7)).isoformat(),
            'fine_amount': 0,
            'is_returned': 1
        },
        # Record 2: Returned late with fine (3 days overdue = Rs.6)
        {
            'member_id': 2,
            'book_id': 2,
            'borrowed_date': (now - timedelta(days=18)).isoformat(),
            'due_date': (now - timedelta(days=5)).isoformat(),
            'return_date': (now - timedelta(days=2)).isoformat(),
            'fine_amount': 6,
            'is_returned': 1
        },
        # Record 3: Currently borrowed, due soon (no fine yet, still active)
        {
            'member_id': 3,
            'book_id': 3,
            'borrowed_date': (now - timedelta(days=10)).isoformat(),
            'due_date': (now + timedelta(days=3)).isoformat(),
            'return_date': None,
            'fine_amount': 0,
            'is_returned': 0
        },
        # Record 4: Currently borrowed and OVERDUE (5 days = Rs.10)
        {
            'member_id': 4,
            'book_id': 4,
            'borrowed_date': (now - timedelta(days=25)).isoformat(),
            'due_date': (now - timedelta(days=5)).isoformat(),
            'return_date': None,
            'fine_amount': 10,
            'is_returned': 0
        },
        # Record 5: Returned on time (no fine)
        {
            'member_id': 5,
            'book_id': 5,
            'borrowed_date': (now - timedelta(days=15)).isoformat(),
            'due_date': (now - timedelta(days=2)).isoformat(),
            'return_date': (now - timedelta(days=2)).isoformat(),
            'fine_amount': 0,
            'is_returned': 1
        },
        # Record 6: Returned with fine (2 days overdue = Rs.4)
        {
            'member_id': 1,
            'book_id': 6,
            'borrowed_date': (now - timedelta(days=17)).isoformat(),
            'due_date': (now - timedelta(days=4)).isoformat(),
            'return_date': (now - timedelta(days=2)).isoformat(),
            'fine_amount': 4,
            'is_returned': 1
        },
        # Record 7: Currently borrowed, active
        {
            'member_id': 2,
            'book_id': 7,
            'borrowed_date': (now - timedelta(days=5)).isoformat(),
            'due_date': (now + timedelta(days=9)).isoformat(),
            'return_date': None,
            'fine_amount': 0,
            'is_returned': 0
        },
        # Record 8: Currently borrowed and OVERDUE (10 days = Rs.20)
        {
            'member_id': 6,
            'book_id': 8,
            'borrowed_date': (now - timedelta(days=28)).isoformat(),
            'due_date': (now - timedelta(days=10)).isoformat(),
            'return_date': None,
            'fine_amount': 20,
            'is_returned': 0
        }
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    for record in borrowing_records:
        cursor.execute("""
            INSERT INTO borrowing (member_id, book_id, borrowed_date, due_date, return_date, fine_amount, is_returned)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (record['member_id'], record['book_id'], record['borrowed_date'], record['due_date'],
              record['return_date'], record['fine_amount'], record['is_returned']))

    conn.commit()
    conn.close()
    print(f"[OK] Inserted {len(borrowing_records)} borrowing records")
    print("  - 2 Returned on time (no fine)")
    print("  - 2 Returned with fines")
    print("  - 2 Currently active (not overdue)")
    print("  - 2 Currently overdue (with fines)")

def insert_reservations():
    """Insert sample reservations."""
    reservations = [
        # Reservation for "The Lord of the Rings" (book_id=10, available_quantity=0)
        {
            'member_id': 3,
            'book_id': 10,
            'reservation_date': (datetime.now() - timedelta(days=3)).isoformat(),
            'is_fulfilled': 0
        },
        # Another reservation for same book
        {
            'member_id': 4,
            'book_id': 10,
            'reservation_date': (datetime.now() - timedelta(days=1)).isoformat(),
            'is_fulfilled': 0
        }
    ]

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    for res in reservations:
        cursor.execute("""
            INSERT INTO reservations (member_id, book_id, reservation_date, is_fulfilled)
            VALUES (?, ?, ?, ?)
        """, (res['member_id'], res['book_id'], res['reservation_date'], res['is_fulfilled']))

    conn.commit()
    conn.close()
    print(f"[OK] Inserted {len(reservations)} reservations")

def main():
    """Main function to seed all data."""
    print("\n" + "="*50)
    print("Library Management System - Data Seeding")
    print("="*50 + "\n")

    try:
        delete_and_recreate_tables()
        insert_books()
        insert_members()
        insert_borrowing_records()
        insert_reservations()

        print("\n" + "="*50)
        print("[OK] Data seeding completed successfully!")
        print("="*50)
        print("\nSummary:")
        print("- 12 Books inserted")
        print("- 6 Members inserted")
        print("- 8 Borrowing records inserted")
        print("  * 2 Returned on time with no fine")
        print("  * 2 Returned late with fine")
        print("  * 2 Currently borrowed (not overdue)")
        print("  * 2 Currently overdue with pending fine")
        print("- 2 Reservations inserted")
        print("\nDatabase is ready for testing!\n")

    except Exception as e:
        print(f"\n[ERROR] Error during seeding: {e}")
        raise

if __name__ == '__main__':
    main()

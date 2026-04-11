import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Sample books data
books = [
    ('The Great Gatsby', 'F. Scott Fitzgerald', '978-0743273565', 'Scribner', 1925, 'Fiction', 5),
    ('To Kill a Mockingbird', 'Harper Lee', '978-0061120084', 'J.B. Lippincott', 1960, 'Fiction', 6),
    ('1984', 'George Orwell', '978-0451524935', 'Signet', 1949, 'Science Fiction', 4),
    ('Pride and Prejudice', 'Jane Austen', '978-0141199078', 'Penguin Classics', 1813, 'Romance', 7),
    ('The Catcher in the Rye', 'J.D. Salinger', '978-0316769082', 'Little, Brown', 1951, 'Fiction', 3),
    ('The Hobbit', 'J.R.R. Tolkien', '978-0547928227', 'Houghton Mifflin', 1937, 'Fantasy', 5),
    ('Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', '978-0747532699', 'Bloomsbury', 1997, 'Fantasy', 8),
    ('The Lord of the Rings', 'J.R.R. Tolkien', '978-0544003415', 'Mariner Books', 1954, 'Fantasy', 4),
    ('Atomic Habits', 'James Clear', '978-0735211292', 'Avery', 2018, 'Self-Help', 6),
    ('Sapiens', 'Yuval Noah Harari', '978-0062316097', 'Harper', 2011, 'Non-Fiction', 5),
    ('The Lean Startup', 'Eric Ries', '978-0307887894', 'Crown Business', 2011, 'Business', 4),
    ('A Brief History of Time', 'Stephen Hawking', '978-0553380163', 'Bantam', 1988, 'Science', 3),
]

# Insert books
for title, author, isbn, publisher, year, genre, quantity in books:
    cursor.execute('''
        INSERT INTO books (title, author, isbn, publisher, publication_year, genre, quantity, available_quantity)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title, author, isbn, publisher, year, genre, quantity, quantity))
    print(f"✓ Added book: {title}")

conn.commit()
conn.close()

print(f"\n✓ {len(books)} sample books added successfully!")

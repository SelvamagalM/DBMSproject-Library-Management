import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Add some sample borrowings
borrowings = [
    (1, 1, datetime.now().isoformat(), (datetime.now() + timedelta(days=14)).isoformat()),
    (2, 3, datetime.now().isoformat(), (datetime.now() + timedelta(days=10)).isoformat()),
    (3, 2, (datetime.now() - timedelta(days=5)).isoformat(), (datetime.now() - timedelta(days=2)).isoformat()),
]

for member_id, book_id, borrowed_date, due_date in borrowings:
    cursor.execute('''
        INSERT INTO borrowing (member_id, book_id, borrowed_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (member_id, book_id, borrowed_date, due_date))
    print(f"✓ Added borrowing: Member {member_id} → Book {book_id}")

conn.commit()
conn.close()

print(f"\n✓ Sample borrowing records added successfully!")

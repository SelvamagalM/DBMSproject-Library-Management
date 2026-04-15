import sqlite3
from datetime import datetime, timedelta

# Connect to database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Clear existing borrowing and reservation records
cursor.execute('DELETE FROM borrowing')
cursor.execute('DELETE FROM reservations')

# Member IDs: 8=Selvamagal, 9=Sandhiya, 10=Janikaa Sri
# Get actual book IDs from database
cursor.execute('SELECT book_id FROM books ORDER BY book_id LIMIT 12')
book_ids = [row[0] for row in cursor.fetchall()]

if len(book_ids) < 12:
    print(f"Error: Need at least 12 books, found {len(book_ids)}")
    conn.close()
    exit(1)

# Active Borrowings (is_returned=0, no return_date)
active_borrowings = [
    # Member 8 (Selvamagal) - 3 active borrowings
    (8, book_ids[0], (datetime.now() - timedelta(days=5)).isoformat(), (datetime.now() + timedelta(days=9)).isoformat(), None, 0, 0),
    (8, book_ids[1], (datetime.now() - timedelta(days=2)).isoformat(), (datetime.now() + timedelta(days=12)).isoformat(), None, 0, 0),
    (8, book_ids[2], (datetime.now() - timedelta(days=1)).isoformat(), (datetime.now() + timedelta(days=13)).isoformat(), None, 0, 0),
    
    # Member 9 (Sandhiya) - 2 active borrowings
    (9, book_ids[3], (datetime.now() - timedelta(days=3)).isoformat(), (datetime.now() + timedelta(days=11)).isoformat(), None, 0, 0),
    (9, book_ids[4], (datetime.now() - timedelta(days=1)).isoformat(), (datetime.now() + timedelta(days=13)).isoformat(), None, 0, 0),
    
    # Member 10 (Janikaa Sri) - 2 active borrowings
    (10, book_ids[5], (datetime.now() - timedelta(days=4)).isoformat(), (datetime.now() + timedelta(days=10)).isoformat(), None, 0, 0),
    (10, book_ids[6], (datetime.now() - timedelta(days=2)).isoformat(), (datetime.now() + timedelta(days=12)).isoformat(), None, 0, 0),
]

# Completed Borrowings (is_returned=1, with return_date)
completed_borrowings = [
    # Member 8 - 2 completed
    (8, book_ids[7], (datetime.now() - timedelta(days=30)).isoformat(), (datetime.now() - timedelta(days=16)).isoformat(), (datetime.now() - timedelta(days=16)).isoformat(), 0, 1),
    (8, book_ids[8], (datetime.now() - timedelta(days=25)).isoformat(), (datetime.now() - timedelta(days=11)).isoformat(), (datetime.now() - timedelta(days=11)).isoformat(), 0, 1),
    
    # Member 9 - 1 completed
    (9, book_ids[9], (datetime.now() - timedelta(days=20)).isoformat(), (datetime.now() - timedelta(days=6)).isoformat(), (datetime.now() - timedelta(days=6)).isoformat(), 0, 1),
    
    # Member 10 - 1 completed
    (10, book_ids[10], (datetime.now() - timedelta(days=28)).isoformat(), (datetime.now() - timedelta(days=14)).isoformat(), (datetime.now() - timedelta(days=14)).isoformat(), 0, 1),
]

# Insert all borrowings
print("Adding Active Borrowings:")
for member_id, book_id, borrowed_date, due_date, return_date, fine, is_returned in active_borrowings:
    cursor.execute('''
        INSERT INTO borrowing (member_id, book_id, borrowed_date, due_date, return_date, fine_amount, is_returned)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (member_id, book_id, borrowed_date, due_date, return_date, fine, is_returned))
    print(f"✓ Active: Member {member_id} → Book {book_id}")

print("\nAdding Completed Borrowings (History):")
for member_id, book_id, borrowed_date, due_date, return_date, fine, is_returned in completed_borrowings:
    cursor.execute('''
        INSERT INTO borrowing (member_id, book_id, borrowed_date, due_date, return_date, fine_amount, is_returned)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (member_id, book_id, borrowed_date, due_date, return_date, fine, is_returned))
    print(f"✓ Completed: Member {member_id} → Book {book_id}")

# Add Reservations (is_fulfilled=0)
print("\nAdding Reservations:")
reservations = [
    (8, book_ids[11], (datetime.now() - timedelta(days=2)).isoformat(), 0, None),
    (9, book_ids[0], (datetime.now() - timedelta(days=1)).isoformat(), 0, None),
    (10, book_ids[3], (datetime.now() - timedelta(days=3)).isoformat(), 0, None),
]

for member_id, book_id, reservation_date, is_fulfilled, fulfilled_date in reservations:
    cursor.execute('''
        INSERT INTO reservations (member_id, book_id, reservation_date, is_fulfilled, fulfilled_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (member_id, book_id, reservation_date, is_fulfilled, fulfilled_date))
    print(f"✓ Reservation: Member {member_id} → Book {book_id}")

conn.commit()
conn.close()

print("\n✓ All borrowing and reservation records added successfully!")
print("\nDemo Login Credentials:")
print("- Selvamagal: selvamagal@library.edu (password: member123)")
print("- Sandhiya: sandhiya@library.edu (password: member123)")
print("- Janikaa Sri: janikaa.sri@library.edu (password: member123)")

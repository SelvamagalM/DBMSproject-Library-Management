import sqlite3
from datetime import datetime

# Connect to database
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Member details
members = [
    ('Selvamagal', 'selvamagal@library.edu', '9876543210', 'Student', '123 Main St'),
    ('Sandhiya', 'sandhiya@library.edu', '9876543211', 'Student', '456 Oak Ave'),
    ('Janikaa Sri', 'janikaa.sri@library.edu', '9876543212', 'Faculty', '789 Pine Rd')
]

# Insert members
for name, email, phone, member_type, address in members:
    cursor.execute('''
        INSERT INTO members (name, email, phone, member_type, address, membership_date)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, email, phone, member_type, address, datetime.now().isoformat()))
    print(f"✓ Added member: {name} ({member_type})")

conn.commit()
conn.close()

print("\n✓ All members added successfully!")

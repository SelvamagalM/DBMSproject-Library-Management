import sqlite3
from datetime import datetime

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Add faculty members
faculty_members = [
    ('RAJARAM.P', 'rajaram@library.edu', '9876543210', 'Main Campus', 'Faculty'),
    ('SENTHIL.K', 'senthil@library.edu', '9876543211', 'Main Campus', 'Faculty')
]

for name, email, phone, address, member_type in faculty_members:
    try:
        cursor.execute("""
            INSERT INTO members (name, email, phone, address, member_type, membership_date, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, email, phone, address, member_type, datetime.now().isoformat(), 1))
        print(f"✓ Added {name} as {member_type}")
    except sqlite3.IntegrityError:
        print(f"✗ {name} already exists")

conn.commit()
conn.close()

print("\n✓ Faculty members added successfully!")

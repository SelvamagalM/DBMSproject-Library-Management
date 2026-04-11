import sqlite3

conn = sqlite3.connect('library.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=" * 60)
print("ALL MEMBERS IN DATABASE:")
print("=" * 60)

cursor.execute("SELECT * FROM members ORDER BY member_id")
members = cursor.fetchall()

for member in members:
    print(f"ID: {member['member_id']}, Name: {member['name']:20} | Type: {member['member_type']:10} | Email: {member['email']}")

print("\n" + "=" * 60)
print(f"Total Members: {len(members)}")
print("=" * 60)

conn.close()

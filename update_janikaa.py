import sqlite3

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Update Janikaa Sri to Faculty
cursor.execute("""
    UPDATE members 
    SET member_type = 'Faculty' 
    WHERE name = 'Janikaa Sri'
""")

conn.commit()

# Verify
cursor.execute("SELECT member_id, name, member_type, email FROM members WHERE name = 'Janikaa Sri'")
result = cursor.fetchone()

if result:
    print(f"✓ Updated: {result[1]} → {result[2]}")
else:
    print("✗ Member not found")

# Show all members
print("\n" + "="*60)
print("ALL MEMBERS:")
print("="*60)

conn.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute("SELECT member_id, name, member_type FROM members ORDER BY member_id")
for member in cursor.fetchall():
    print(f"ID: {member['member_id']} | {member['name']:20} | Type: {member['member_type']}")

conn.close()

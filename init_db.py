import os

# Delete old database to start fresh
if os.path.exists('library.db'):
    os.remove('library.db')
    print("✓ Deleted old database")

# Import and initialize with new schema
from db import create_database
create_database()
print("✓ Database recreated with new schema")

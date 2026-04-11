================================================================================
LIBRARY MANAGEMENT SYSTEM - SAMPLE DATA SEEDING
================================================================================

CREATED: seed_data.py
PURPOSE: Automatically populate library.db with realistic test data

================================================================================
WHAT WAS CREATED:
================================================================================

1. BOOKS (12 entries)
   ✓ 12 different books with unique ISBNs
   ✓ Various genres: Fiction, Technology, Fantasy, Biography, etc.
   ✓ Different authors and publishers
   ✓ Quantities ranging from 2-4 copies
   ✓ Most have available copies (some zero - for reservations testing)

2. MEMBERS (6 entries)
   ✓ 6 library members
   ✓ Different types: Student (3), Faculty (2), Staff (1)
   ✓ Unique emails and phone numbers
   ✓ Realistic names and addresses

3. BORROWING RECORDS (8 entries)
   ✓ 2 Returned on time (Zero fine)
   ✓ 2 Returned late with fines (Rs.6 and Rs.4)
   ✓ 2 Currently active, not overdue
   ✓ 2 Currently overdue (with pending fines of Rs.10 and Rs.20)
   
   TOTAL OUTSTANDING FINES: Rs.40

4. RESERVATIONS (2 entries)
   ✓ 2 members waiting for "The Lord of the Rings"
   ✓ Shows reservation queue system
   ✓ Tests pending reservation functionality

================================================================================
HOW TO RUN:
================================================================================

1. Open Terminal/Command Prompt
2. Navigate to library_web directory:
   cd c:/Users/cmala/.antigravity/library_web

3. Run the seed script:
   python seed_data.py

4. You'll see:
   [OK] Tables recreated successfully
   [OK] Inserted 12 books
   [OK] Inserted 6 members
   [OK] Inserted 8 borrowing records
   [OK] Inserted 2 reservations
   [OK] Data seeding completed successfully!

================================================================================
WHAT YOU CAN TEST:
================================================================================

DASHBOARD (http://localhost:5000)
- View statistics with fresh data
- See outstanding fines card (Rs.40, 4 entries)
- Check quick overview of library status

REPORTS PAGE (http://localhost:5000/reports)
- Overdue Books Report (2 overdue items highlighted in red)
- Members with Outstanding Fines (4 entries with Rs.40 total)
- Outstanding Fines Details table with:
  • Complete borrowing information
  • Days overdue calculation
  • Red highlighting for overdue items
  • "Mark as Paid" button functionality

TESTING SCENARIOS:
1. Click "Mark as Paid" on any fine to test:
   - Fine removal
   - Real-time total updates
   - Success notifications

2. View borrowing details:
   - Active vs. returned status
   - Fine calculations (Rs.2 per day)
   - Member information

3. Check reservations:
   - See 2 members in queue for "The Lord of the Rings"
   - Understand reservation system

================================================================================
DATABASE STRUCTURE:
================================================================================

BOOKS TABLE
- 12 books with ISBNs, titles, authors, genres
- Quantities: 2-4 copies each
- Available quantities reflect current borrowings

MEMBERS TABLE
- 6 members: Students, Faculty, Staff
- Contact information: email, phone, address
- Membership dates from June 2025

BORROWING TABLE
- 8 records showing various scenarios
- Return dates for completed borrowings
- Fine amounts calculated (Rs.0 to Rs.20)
- Days overdue properly calculated

RESERVATIONS TABLE
- 2 pending reservations
- Both for same book (testing queue)
- Shows reservation workflow

================================================================================
FILE INFORMATION:
================================================================================

seed_data.py
- Standalone Python script
- Deletes existing data and recreates fresh
- Inserts realistic sample data
- Calculates proper dates and times
- Handles Windows console encoding

Uses:
- sqlite3 (included with Python)
- datetime (included with Python)
- No external dependencies

================================================================================
RESET/RESEED:
================================================================================

To clear the database and reseed with fresh data:
1. Simply run: python seed_data.py again
2. All existing data will be deleted
3. Fresh sample data will be inserted
4. Database is ready for continued testing

================================================================================
NOTES:
================================================================================

✓ All dates are calculated relative to current date
✓ Overdue items automatically have fines calculated
✓ Reserved book has 0 available quantity
✓ Members have realistic email addresses
✓ Fine calculation: Rs.2 per day overdue
✓ Sample data is diverse and comprehensive
✓ Ready for immediate application testing

================================================================================
QUICK START:
================================================================================

1. python seed_data.py              # Seed the database
2. python app.py                    # Start the Flask app
3. Visit http://localhost:5000      # View dashboard
4. Go to Reports page               # See outstanding fines

That's it! Everything is ready to use.

================================================================================

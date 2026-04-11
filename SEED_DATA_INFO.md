# Library Management System - Sample Data

## Overview
The `seed_data.py` script populates the library.db database with realistic sample data for testing and demonstration purposes.

## Running the Seed Script

```bash
cd library_web
python seed_data.py
```

## Data Inserted

### 1. Books (12 entries)
| Title | Author | ISBN | Genre | Qty | Available |
|-------|--------|------|-------|-----|-----------|
| To Kill a Mockingbird | Harper Lee | 978-0-06-112008-4 | Fiction | 3 | 2 |
| 1984 | George Orwell | 978-0-452-26423-5 | Dystopian Fiction | 2 | 1 |
| Pride and Prejudice | Jane Austen | 978-0-14-143951-8 | Romance | 4 | 3 |
| The Great Gatsby | F. Scott Fitzgerald | 978-0-7432-7356-5 | Fiction | 3 | 2 |
| Sapiens | Yuval Noah Harari | 978-0-06-231609-7 | Non-fiction | 2 | 1 |
| The Catcher in the Rye | J.D. Salinger | 978-0-316-76948-0 | Fiction | 3 | 3 |
| Python Programming | Mark Lutz | 978-1-449-35573-9 | Technology | 4 | 2 |
| The Hobbit | J.R.R. Tolkien | 978-0-547-92822-8 | Fantasy | 3 | 1 |
| Atomic Habits | James Clear | 978-0-735-21159-4 | Self-help | 2 | 2 |
| **The Lord of the Rings** | J.R.R. Tolkien | 978-0-544-00159-5 | Fantasy | 2 | **0** (reserved) |
| Educated | Tara Westover | 978-0-399-59065-7 | Biography | 3 | 2 |
| Clean Code | Robert C. Martin | 978-0-13-235088-4 | Technology | 2 | 1 |

### 2. Members (6 entries)
| ID | Name | Email | Phone | Type |
|----|------|-------|-------|------|
| 1 | Rajesh Kumar | rajesh.kumar@university.edu | 9876543210 | Student |
| 2 | Priya Sharma | priya.sharma@university.edu | 9876543211 | Faculty |
| 3 | Amit Patel | amit.patel@university.edu | 9876543212 | Student |
| 4 | Neha Singh | neha.singh@university.edu | 9876543213 | Staff |
| 5 | Vikram Desai | vikram.desai@university.edu | 9876543214 | Faculty |
| 6 | Anjali Gupta | anjali.gupta@university.edu | 9876543215 | Student |

### 3. Borrowing Records (8 entries)

#### Returned On Time (No Fine)
- **Rajesh Kumar** borrowed "To Kill a Mockingbird" - Returned 7 days early
- **Vikram Desai** borrowed "Sapiens" - Returned on due date

#### Returned with Fines
- **Priya Sharma** borrowed "1984" - Returned 3 days late → **Fine: Rs.6**
- **Rajesh Kumar** borrowed "The Catcher in the Rye" - Returned 2 days late → **Fine: Rs.4**

#### Currently Active (Not Overdue)
- **Amit Patel** has "Pride and Prejudice" - Due in 3 days (Rs.0 fine)
- **Vikram Desai** has "Python Programming" - Due in 9 days (Rs.0 fine)

#### Currently Overdue (Pending Fines)
- **Neha Singh** has "The Great Gatsby" - **5 days overdue → Fine: Rs.10**
- **Anjali Gupta** has "The Hobbit" - **10 days overdue → Fine: Rs.20**

**Total Outstanding Fines: Rs.40**

### 4. Reservations (2 entries)
| Member | Book | Status |
|--------|------|--------|
| Amit Patel (ID: 3) | **The Lord of the Rings** | Pending (Position: 1) |
| Neha Singh (ID: 4) | **The Lord of the Rings** | Pending (Position: 2) |

## Fine Calculation
- Fine Rate: **Rs.2 per day**
- Formula: `days_overdue × 2 = fine_amount`
- Example: 5 days overdue = 5 × 2 = Rs.10

## Features Demonstrated

### Outstanding Fines Section
✓ Shows members with pending fines (Rs.40 total)
✓ Highlights overdue entries in red
✓ Displays days overdue calculation
✓ "Mark as Paid" button to clear fines
✓ Real-time total updates

### Dashboard
✓ Total Books: 12
✓ Active Members: 6
✓ Active Borrowings: 4 (2 on time, 2 overdue)
✓ Overdue Books: 2
✓ Outstanding Fines: Rs.40 across 4 entries

### Reports Page
✓ Overdue Books Report (2 entries)
✓ Members with Fines Summary
✓ Outstanding Fines Details with Mark as Paid functionality
✓ Borrowing Statistics

## Testing Scenarios

### 1. View Outstanding Fines
- Go to Reports page
- See detailed outstanding fines table
- Note red highlighting for overdue entries
- Click "Mark as Paid" to clear fines

### 2. Dashboard Overview
- See quick stats cards
- View outstanding fines card showing:
  - Total: Rs.40
  - Pending Entries: 4

### 3. Manage Fines
- Mark fines as paid
- See totals update in real-time
- Test with overdue and returned items

### 4. Reservation Queue
- View 2 members waiting for "The Lord of the Rings"
- Understand reservation system

## Reset Data
To reset and reseed the database, simply run:
```bash
python seed_data.py
```

This will delete all existing data and insert fresh sample data.

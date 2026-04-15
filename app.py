from flask import Flask, render_template, request, redirect, url_for, jsonify, flash, session
from functools import wraps
import sqlite3
from datetime import datetime, timedelta
from db import get_connection, create_database, dict_from_row, dict_list_from_rows

app = Flask(__name__)
app.secret_key = 'library_management_secret_key_2026'

# Default credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'
MEMBER_DEMO_USERNAME = 'member'
MEMBER_DEMO_PASSWORD = 'member123'

FINE_PER_DAY = 2  # Rs.2 per day
BORROW_DAYS = 14  # Default borrowing period

# Initialize database
create_database()

# ==================== AUTHENTICATION ====================

def login_required(f):
    """Decorator to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            flash('Admin access required!', 'error')
            return redirect(url_for('member_dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def member_required(f):
    """Decorator to require member role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Please login first!', 'error')
            return redirect(url_for('login'))
        if session.get('role') != 'member':
            flash('Member access required!', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== LOGIN/LOGOUT ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for admin and members."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        role = request.form.get('role', 'admin')
        
        # Check credentials
        if role == 'admin':
            if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
                session['user'] = username
                session['role'] = 'admin'
                flash('Welcome Admin!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid admin credentials!', 'error')
        elif role == 'member':
            # Check if member exists in database
            conn = get_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT member_id, name FROM members WHERE email = ? AND is_active = 1", (username,))
                member_row = cursor.fetchone()
                member = dict_from_row(member_row) if member_row else None
                
                if member and password == MEMBER_DEMO_PASSWORD:
                    session['user'] = username
                    session['role'] = 'member'
                    session['member_id'] = member['member_id']
                    session['member_name'] = member['name']
                    flash(f"Welcome {member['name']}!", 'success')
                    return redirect(url_for('member_dashboard'))
                elif not member:
                    flash('Member not found! Please use your registered email.', 'error')
                else:
                    flash('Invalid password!', 'error')
            except Exception as e:
                flash(f'Login error: {str(e)}', 'error')
            finally:
                conn.close()
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user."""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

def get_dashboard_stats():
    """Get statistics for dashboard."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Total books
        cursor.execute("SELECT COUNT(*) as count FROM books")
        total_books = cursor.fetchone()['count']

        # Total active members
        cursor.execute("SELECT COUNT(*) as count FROM members WHERE is_active = 1")
        total_members = cursor.fetchone()['count']

        # Active borrowings
        cursor.execute("SELECT COUNT(*) as count FROM borrowing WHERE is_returned = 0")
        active_borrowings = cursor.fetchone()['count']

        # Overdue books
        cursor.execute("""
            SELECT COUNT(*) as count FROM borrowing
            WHERE is_returned = 0 AND datetime(due_date) < datetime('now')
        """)
        overdue_count = cursor.fetchone()['count']

        # Available books
        cursor.execute("SELECT SUM(available_quantity) as total FROM books")
        available_books = cursor.fetchone()['total'] or 0

        # Outstanding fines - total amount
        cursor.execute("SELECT SUM(fine_amount) as total FROM borrowing WHERE fine_amount > 0")
        outstanding_fines = cursor.fetchone()['total'] or 0

        # Outstanding fines - count
        cursor.execute("SELECT COUNT(*) as count FROM borrowing WHERE fine_amount > 0")
        outstanding_fines_count = cursor.fetchone()['count']

        return {
            'total_books': total_books,
            'total_members': total_members,
            'active_borrowings': active_borrowings,
            'overdue_count': overdue_count,
            'available_books': available_books,
            'outstanding_fines': outstanding_fines,
            'outstanding_fines_count': outstanding_fines_count
        }
    finally:
        conn.close()

# ==================== HOME & DASHBOARD ====================

@app.route('/')
@admin_required
def index():
    """Home page with dashboard (Admin only)."""
    stats = get_dashboard_stats()
    return render_template('index.html', stats=stats)

@app.route('/member-dashboard')
@member_required
def member_dashboard():
    """Member dashboard showing their borrowings."""
    member_id = session.get('member_id')
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get member info
        cursor.execute("SELECT name, email, phone, member_type, membership_date FROM members WHERE member_id = ?", (member_id,))
        member = dict_from_row(cursor.fetchone())
        
        # Get active borrowings
        cursor.execute("""
            SELECT b.borrowing_id, bk.isbn, bk.title, bk.author, b.borrowed_date, b.due_date, b.is_returned
            FROM borrowing b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.member_id = ? AND b.is_returned = 0
            ORDER BY b.due_date
        """, (member_id,))
        active_borrowings_raw = dict_list_from_rows(cursor.fetchall())
        
        # Add is_overdue flag to each borrowing
        now = datetime.now()
        active_borrowings = []
        for borrow in active_borrowings_raw:
            try:
                # Handle both ISO format and regular datetime format
                due_date_str = borrow['due_date']
                if 'T' in due_date_str:
                    due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                else:
                    due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
            except:
                # Fallback: just use current time if parsing fails
                due_date = now
            
            borrow['is_overdue'] = now > due_date
            active_borrowings.append(borrow)
        
        # Get completed borrowings
        cursor.execute("""
            SELECT b.borrowing_id, bk.isbn, bk.title, bk.author, b.borrowed_date, b.due_date, 
                   b.return_date, b.fine_amount, b.is_returned
            FROM borrowing b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.member_id = ? AND b.is_returned = 1
            ORDER BY b.return_date DESC
            LIMIT 10
        """, (member_id,))
        completed_borrowings = dict_list_from_rows(cursor.fetchall())
        
        # Get member's reservations
        cursor.execute("""
            SELECT r.reservation_id, bk.isbn, bk.title, bk.author, r.reservation_date,
                   COUNT(*) OVER (PARTITION BY r.book_id ORDER BY r.reservation_date) as position_in_queue
            FROM reservations r
            JOIN books bk ON r.book_id = bk.book_id
            WHERE r.member_id = ? AND r.is_fulfilled = 0
            ORDER BY r.reservation_date
        """, (member_id,))
        reservations = dict_list_from_rows(cursor.fetchall())
        
        # Get fines for this member
        cursor.execute("""
            SELECT b.borrowing_id, bk.title, b.fine_amount, b.return_date
            FROM borrowing b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.member_id = ? AND b.fine_amount > 0
            ORDER BY b.return_date DESC
        """, (member_id,))
        fines = dict_list_from_rows(cursor.fetchall())
        total_fines = sum(f.get('fine_amount', 0) for f in fines)
        
        return render_template('member_dashboard.html',
                             member=member,
                             active_borrowings=active_borrowings,
                             completed_borrowings=completed_borrowings,
                             reservations=reservations,
                             fines=fines,
                             total_fines=total_fines)
    finally:
        conn.close()

# ==================== BOOKS ROUTES ====================

@app.route('/books')
@admin_required
def books_page():
    """Books management page."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT book_id, title, author, isbn, publisher, publication_year, genre, quantity, available_quantity
            FROM books
            ORDER BY title
        """)
        books_list = dict_list_from_rows(cursor.fetchall())
    finally:
        conn.close()
    
    return render_template('books.html', books=books_list)

@app.route('/api/books/search', methods=['GET'])
@admin_required
def search_books():
    """Search books by ISBN or title."""
    search_term = request.args.get('q', '').strip()
    
    if not search_term:
        return jsonify([])
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT book_id, title, author, isbn, publisher, publication_year, genre, quantity, available_quantity
            FROM books
            WHERE title LIKE ? OR isbn LIKE ? OR author LIKE ?
            ORDER BY title
        """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        
        books_list = dict_list_from_rows(cursor.fetchall())
        return jsonify(books_list)
    finally:
        conn.close()

@app.route('/api/books/add', methods=['POST'])
def add_book():
    """Add a new book."""
    data = request.get_json()
    
    title = data.get('title', '').strip()
    author = data.get('author', '').strip()
    isbn = data.get('isbn', '').strip()
    publisher = data.get('publisher', '').strip() or None
    publication_year = data.get('publication_year')
    genre = data.get('genre', '').strip() or None
    quantity = int(data.get('quantity', 1))
    
    if not title or not author or not isbn or quantity <= 0:
        return jsonify({'success': False, 'error': 'Invalid input. All fields required, quantity > 0.'}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO books (title, author, isbn, publisher, publication_year, genre, quantity, available_quantity)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, author, isbn, publisher, publication_year, genre, quantity, quantity))
        conn.commit()
        return jsonify({'success': True, 'message': f"Book '{title}' added successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'ISBN already exists!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

# ==================== MEMBERS ROUTES ====================

@app.route('/members')
@admin_required
def members_page():
    """Members management page."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT member_id, name, email, phone, membership_date, member_type, is_active
            FROM members
            WHERE is_active = 1
            ORDER BY name
        """)
        members_list = dict_list_from_rows(cursor.fetchall())
    finally:
        conn.close()
    
    return render_template('members.html', members=members_list)

@app.route('/members/<int:member_id>')
@admin_required
def member_detail(member_id):
    """View member details and borrowing history."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT member_id, name, email, phone, address, membership_date, member_type
            FROM members
            WHERE member_id = ?
        """, (member_id,))
        member = dict_from_row(cursor.fetchone())
        
        if not member:
            return redirect(url_for('members_page'))
        
        cursor.execute("""
            SELECT b.borrowing_id, bk.isbn, bk.title, bk.author, b.borrowed_date, b.due_date, 
                   b.return_date, b.fine_amount, b.is_returned
            FROM borrowing b
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.member_id = ?
            ORDER BY b.borrowed_date DESC
        """, (member_id,))
        history = dict_list_from_rows(cursor.fetchall())
        
        return render_template('member_detail.html', member=member, history=history)
    finally:
        conn.close()

@app.route('/api/members/register', methods=['POST'])
def register_member():
    """Register a new member."""
    data = request.get_json()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip() or None
    address = data.get('address', '').strip() or None
    member_type = data.get('member_type', 'Student').strip()
    
    if not name or not email:
        return jsonify({'success': False, 'error': 'Name and email are required!'}), 400
    
    if member_type not in ['Student', 'Faculty', 'Staff']:
        member_type = 'Student'
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO members (name, email, phone, address, member_type)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, phone, address, member_type))
        conn.commit()
        return jsonify({'success': True, 'message': f"Member '{name}' registered successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Email already registered!'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

# ==================== BORROWING ROUTES ====================

@app.route('/borrowing')
@admin_required
def borrowing_page():
    """Borrowing and returns page."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get active borrowings
        cursor.execute("""
            SELECT b.borrowing_id, m.member_id, m.name, m.member_type, bk.book_id, bk.isbn, bk.title, bk.author, b.due_date, b.is_returned
            FROM borrowing b
            JOIN members m ON b.member_id = m.member_id
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.is_returned = 0
            ORDER BY b.due_date
        """)
        active_borrowings = dict_list_from_rows(cursor.fetchall())
        
        # Get list of members and books for forms
        cursor.execute("SELECT member_id, name, member_type FROM members WHERE is_active = 1 ORDER BY name")
        members_list = dict_list_from_rows(cursor.fetchall())
        
        cursor.execute("SELECT book_id, isbn, title, author, available_quantity FROM books WHERE available_quantity > 0 ORDER BY title")
        books_list = dict_list_from_rows(cursor.fetchall())
        
        return render_template('borrowing.html', 
                             active_borrowings=active_borrowings,
                             members=members_list,
                             books=books_list,
                             now=datetime.now())
    finally:
        conn.close()

@app.route('/api/borrowing/issue', methods=['POST'])
def issue_book():
    """Issue a book to a member."""
    data = request.get_json()
    
    member_id = int(data.get('member_id', 0))
    book_id = int(data.get('book_id', 0))
    borrow_days = int(data.get('borrow_days', BORROW_DAYS))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check member
        cursor.execute("SELECT name FROM members WHERE member_id = ? AND is_active = 1", (member_id,))
        member = cursor.fetchone()
        if not member:
            return jsonify({'success': False, 'error': 'Member not found or inactive!'}), 400
        
        # Check book
        cursor.execute("SELECT title, available_quantity FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({'success': False, 'error': 'Book not found!'}), 400
        
        if book['available_quantity'] <= 0:
            return jsonify({'success': False, 'error': 'Book not available!'}), 400
        
        # Issue book
        borrowed_date = datetime.now()
        due_date = borrowed_date + timedelta(days=borrow_days)
        
        cursor.execute("""
            INSERT INTO borrowing (member_id, book_id, due_date)
            VALUES (?, ?, ?)
        """, (member_id, book_id, due_date.strftime("%Y-%m-%d %H:%M:%S")))
        
        # Update available quantity
        cursor.execute("""
            UPDATE books SET available_quantity = available_quantity - 1 WHERE book_id = ?
        """, (book_id,))
        
        conn.commit()
        return jsonify({'success': True, 'message': f"Book issued successfully! Due date: {due_date.strftime('%d-%m-%Y')}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/borrowing/return', methods=['POST'])
def return_book():
    """Return a book."""
    data = request.get_json()
    borrowing_id = int(data.get('borrowing_id', 0))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get borrowing details
        cursor.execute("""
            SELECT b.member_id, b.book_id, b.due_date, b.is_returned, bk.title, m.name
            FROM borrowing b
            JOIN members m ON b.member_id = m.member_id
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.borrowing_id = ?
        """, (borrowing_id,))
        
        record = cursor.fetchone()
        if not record:
            return jsonify({'success': False, 'error': 'Borrowing record not found!'}), 400
        
        if record['is_returned']:
            return jsonify({'success': False, 'error': 'This book has already been returned!'}), 400
        
        # Calculate fine
        return_date = datetime.now()
        
        # Handle both ISO format and regular datetime format
        due_date_str = record['due_date']
        try:
            if 'T' in due_date_str:
                due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
            else:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M:%S")
        except:
            due_date = return_date
        
        fine_amount = 0
        
        if return_date > due_date:
            days_overdue = (return_date - due_date).days
            fine_amount = days_overdue * FINE_PER_DAY
        
        # Update borrowing
        cursor.execute("""
            UPDATE borrowing
            SET return_date = ?, fine_amount = ?, is_returned = 1
            WHERE borrowing_id = ?
        """, (return_date.strftime("%Y-%m-%d %H:%M:%S"), fine_amount, borrowing_id))
        
        # Update available quantity
        cursor.execute("""
            UPDATE books SET available_quantity = available_quantity + 1 WHERE book_id = ?
        """, (record['book_id'],))
        
        conn.commit()
        
        message = f"Book returned successfully! "
        if fine_amount > 0:
            message += f"Fine: Rs.{fine_amount} ({(return_date - due_date).days} days overdue)"
        else:
            message += "No fine charged - returned on time!"
        
        return jsonify({'success': True, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

# ==================== RESERVATIONS ROUTES ====================

@app.route('/reservations')
@admin_required
def reservations_page():
    """Reservations page."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get books with reservations
        cursor.execute("""
            SELECT b.book_id, b.isbn, b.title, b.author, COUNT(r.reservation_id) as queue_count
            FROM books b
            LEFT JOIN reservations r ON b.book_id = r.book_id AND r.is_fulfilled = 0
            WHERE EXISTS (SELECT 1 FROM reservations WHERE book_id = b.book_id AND is_fulfilled = 0)
            GROUP BY b.book_id
            ORDER BY COUNT(r.reservation_id) DESC
        """)
        books_with_reservations = dict_list_from_rows(cursor.fetchall())
        
        # Get list of active members and books for form
        cursor.execute("SELECT member_id, name, member_type FROM members WHERE is_active = 1 ORDER BY name")
        members_list = dict_list_from_rows(cursor.fetchall())
        
        cursor.execute("SELECT book_id, isbn, title, author FROM books ORDER BY title")
        books_list = dict_list_from_rows(cursor.fetchall())
        
        return render_template('reservations.html',
                             books_with_reservations=books_with_reservations,
                             members=members_list,
                             books=books_list)
    finally:
        conn.close()

@app.route('/api/reservations/book/<int:book_id>')
def get_reservation_queue(book_id):
    """Get reservation queue for a book."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT r.reservation_id, r.member_id, m.name, m.member_type, m.email, r.reservation_date,
                   CASE WHEN r.is_fulfilled = 1 THEN 'Fulfilled' ELSE 'Pending' END as status
            FROM reservations r
            JOIN members m ON r.member_id = m.member_id
            WHERE r.book_id = ? AND r.is_fulfilled = 0
            ORDER BY r.reservation_date
        """, (book_id,))
        
        queue = dict_list_from_rows(cursor.fetchall())
        return jsonify(queue)
    finally:
        conn.close()

@app.route('/api/reservations/add', methods=['POST'])
def add_reservation():
    """Add a book reservation."""
    data = request.get_json()
    
    member_id = int(data.get('member_id', 0))
    book_id = int(data.get('book_id', 0))
    
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Check member
        cursor.execute("SELECT name FROM members WHERE member_id = ? AND is_active = 1", (member_id,))
        if not cursor.fetchone():
            return jsonify({'success': False, 'error': 'Member not found or inactive!'}), 400
        
        # Check book
        cursor.execute("SELECT title FROM books WHERE book_id = ?", (book_id,))
        book = cursor.fetchone()
        if not book:
            return jsonify({'success': False, 'error': 'Book not found!'}), 400
        
        # Check existing reservation
        cursor.execute("""
            SELECT reservation_id FROM reservations
            WHERE member_id = ? AND book_id = ? AND is_fulfilled = 0
        """, (member_id, book_id))
        
        if cursor.fetchone():
            return jsonify({'success': False, 'error': 'Member has already reserved this book!'}), 400
        
        # Add reservation
        cursor.execute("""
            INSERT INTO reservations (member_id, book_id)
            VALUES (?, ?)
        """, (member_id, book_id))
        
        # Get position
        cursor.execute("""
            SELECT COUNT(*) as position FROM reservations
            WHERE book_id = ? AND is_fulfilled = 0 AND reservation_date <= CURRENT_TIMESTAMP
        """, (book_id,))
        
        position = cursor.fetchone()['position']
        conn.commit()
        
        return jsonify({'success': True, 'message': f"Book reserved! Position in queue: {position}"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/reservations/cancel/<int:reservation_id>', methods=['POST'])
def cancel_reservation(reservation_id):
    """Cancel a reservation."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT is_fulfilled FROM reservations WHERE reservation_id = ?", (reservation_id,))
        result = cursor.fetchone()
        
        if not result:
            return jsonify({'success': False, 'error': 'Reservation not found!'}), 400
        
        if result['is_fulfilled']:
            return jsonify({'success': False, 'error': 'This reservation is already fulfilled!'}), 400
        
        cursor.execute("DELETE FROM reservations WHERE reservation_id = ?", (reservation_id,))
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Reservation cancelled successfully!'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/outstanding-fines')
def get_outstanding_fines():
    """Get all members with outstanding (unpaid) fines."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT b.borrowing_id, m.member_id, m.name, bk.isbn, bk.title,
                   b.borrowed_date, b.due_date, b.return_date, b.fine_amount,
                   CASE
                       WHEN b.return_date IS NOT NULL THEN
                           CAST((julianday(b.return_date) - julianday(b.due_date)) AS INTEGER)
                       ELSE
                           CAST((julianday('now') - julianday(b.due_date)) AS INTEGER)
                   END as days_overdue
            FROM borrowing b
            JOIN members m ON b.member_id = m.member_id
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.fine_amount > 0
            ORDER BY b.fine_amount DESC
        """)
        fines = dict_list_from_rows(cursor.fetchall())

        # Calculate total
        total_fines = sum(fine.get('fine_amount', 0) for fine in fines)

        return jsonify({
            'fines': fines,
            'total_amount': total_fines,
            'count': len(fines)
        })
    finally:
        conn.close()

@app.route('/api/fines/mark-paid/<int:borrowing_id>', methods=['POST'])
def mark_fine_paid(borrowing_id):
    """Mark a fine as paid."""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT fine_amount FROM borrowing WHERE borrowing_id = ? AND fine_amount > 0", (borrowing_id,))
        record = cursor.fetchone()

        if not record:
            return jsonify({'success': False, 'error': 'No fine found for this borrowing!'}), 400

        # Set fine_amount to 0 (mark as paid)
        cursor.execute("""
            UPDATE borrowing
            SET fine_amount = 0
            WHERE borrowing_id = ?
        """, (borrowing_id,))

        conn.commit()
        return jsonify({'success': True, 'message': f"Fine of Rs.{record['fine_amount']} marked as paid!"})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        conn.close()

# ==================== REPORTS ROUTES ====================

@app.route('/reports')
@admin_required
def reports_page():
    """Reports page."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Overdue books
        cursor.execute("""
            SELECT b.borrowing_id, m.name, m.member_id, m.email, m.phone, bk.isbn, bk.title, bk.author, b.due_date,
                   CAST((julianday('now') - julianday(b.due_date)) AS INTEGER) as days_overdue,
                   CAST((julianday('now') - julianday(b.due_date)) * 2 AS INTEGER) as estimated_fine
            FROM borrowing b
            JOIN members m ON b.member_id = m.member_id
            JOIN books bk ON b.book_id = bk.book_id
            WHERE b.is_returned = 0 AND datetime(b.due_date) < datetime('now')
            ORDER BY b.due_date
        """)
        overdue_books = dict_list_from_rows(cursor.fetchall())
        
        # Members with fines
        cursor.execute("""
            SELECT m.member_id, m.name, m.email, m.phone, m.member_type, SUM(b.fine_amount) as total_fine
            FROM members m
            JOIN borrowing b ON m.member_id = b.member_id
            WHERE b.is_returned = 1 AND b.fine_amount > 0
            GROUP BY m.member_id
            ORDER BY total_fine DESC
        """)
        members_with_fines = dict_list_from_rows(cursor.fetchall())
        
        # Top borrowed books
        cursor.execute("""
            SELECT bk.isbn, bk.title, bk.author, COUNT(b.borrowing_id) as borrow_count
            FROM borrowing b
            JOIN books bk ON b.book_id = bk.book_id
            GROUP BY b.book_id
            ORDER BY borrow_count DESC
            LIMIT 10
        """)
        top_books = dict_list_from_rows(cursor.fetchall())
        
        # Member-wise borrowing history
        cursor.execute("""
            SELECT m.member_id, m.name, m.email, m.member_type, COUNT(b.borrowing_id) as total_borrowed,
                   SUM(CASE WHEN b.is_returned = 0 THEN 1 ELSE 0 END) as active_borrowings
            FROM members m
            LEFT JOIN borrowing b ON m.member_id = b.member_id
            WHERE m.is_active = 1
            GROUP BY m.member_id
            ORDER BY total_borrowed DESC
        """)
        member_stats = dict_list_from_rows(cursor.fetchall())
        
        # Statistics
        cursor.execute("SELECT COUNT(*) as count FROM books")
        total_books = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM members WHERE is_active = 1")
        total_members = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM borrowing WHERE is_returned = 0")
        active_borrowings = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM borrowing")
        total_issued = cursor.fetchone()['count']
        
        cursor.execute("SELECT SUM(available_quantity) as total FROM books")
        available = cursor.fetchone()['total'] or 0
        
        cursor.execute("SELECT SUM(fine_amount) as total FROM borrowing WHERE is_returned = 1 AND fine_amount > 0")
        total_fines = cursor.fetchone()['total'] or 0
        
        cursor.execute("SELECT COUNT(*) as count FROM reservations WHERE is_fulfilled = 0")
        pending_reservations = cursor.fetchone()['count']
        
        stats = {
            'total_books': total_books,
            'total_members': total_members,
            'active_borrowings': active_borrowings,
            'total_issued': total_issued,
            'available': available,
            'total_fines': total_fines,
            'pending_reservations': pending_reservations,
            'overdue_count': len(overdue_books)
        }
        
        return render_template('reports.html',
                             stats=stats,
                             overdue_books=overdue_books,
                             members_with_fines=members_with_fines,
                             top_books=top_books,
                             member_stats=member_stats)
    finally:
        conn.close()

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

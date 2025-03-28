import mysql.connector 
from credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
import bcrypt
from datetime import datetime, timedelta

# Creating and returning DB connection 
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Database initialization - creates tables if they don't exist
def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()
    
    # Create books table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        author VARCHAR(255) NOT NULL,
        genre VARCHAR(100) NOT NULL,
        status VARCHAR(50) DEFAULT 'available'
    )
    ''')
    
    # Create customers table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        firstname VARCHAR(100) NOT NULL,
        lastname VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        passwordhash BINARY(60) NOT NULL
    )
    ''')
    
    # Create borrowingrecords table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS borrowingrecords (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bookid INT NOT NULL,
        customerid INT NOT NULL,
        borrowdate DATE NOT NULL,
        returndate DATE,
        late_fee DECIMAL(10, 2) DEFAULT 0.00,
        FOREIGN KEY (bookid) REFERENCES books(id),
        FOREIGN KEY (customerid) REFERENCES customers(id)
    )
    ''')
    
    connection.commit()
    cursor.close()
    connection.close()
    
# Adds a new book to system 
def create_book(title, author, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO books (title, author, genre, status) VALUES (%s, %s, %s, 'available')"
    cursor.execute(query, (title, author, genre))
    connection.commit()
    cursor.close()
    connection.close()
    
# Gets all books
def get_books(): 
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    connection.close()
    return books 

# Get a single book by ID
def get_book(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (id,))
    book = cursor.fetchone()
    cursor.close()
    connection.close()
    return book

# Update the details of the book 
def update_book(id, title, author, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE books SET title = %s, author = %s, genre = %s WHERE id = %s"
    cursor.execute(query, (title, author, genre, id))
    connection.commit()
    cursor.close()
    connection.close()
    
# Delete book by book id 
def delete_book(id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM books WHERE id = %s"
    cursor.execute(query, (id,))  # Note the comma to make it a tuple
    connection.commit()
    cursor.close()
    connection.close()
    
# Update book status (available/unavailable)
def update_book_status(id, status):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE books SET status = %s WHERE id = %s"
    cursor.execute(query, (status, id))
    connection.commit()
    cursor.close()
    connection.close()

# Add new customer
def add_customer(firstname, lastname, email, password):
    salt = bcrypt.gensalt()
    passwordhash = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO customers (firstname, lastname, email, passwordhash) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (firstname, lastname, email, passwordhash))
    connection.commit()
    cursor.close()
    connection.close()
    
# Retrieve all customers
def get_customers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, firstname, lastname, email FROM customers")  # Exclude passwordhash from result
    customers = cursor.fetchall()
    cursor.close()
    connection.close()
    return customers

# Get a single customer by ID
def get_customer(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id, firstname, lastname, email FROM customers WHERE id = %s", (id,))
    customer = cursor.fetchone()
    cursor.close()
    connection.close()
    return customer

# Update customer details
def update_customer(id, firstname, lastname, email):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE customers SET firstname = %s, lastname = %s, email = %s WHERE id = %s"
    cursor.execute(query, (firstname, lastname, email, id))
    connection.commit()
    cursor.close()
    connection.close()

# Update customer password
def update_customer_password(id, new_password):
    salt = bcrypt.gensalt()
    passwordhash = bcrypt.hashpw(new_password.encode('utf-8'), salt)
    
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE customers SET passwordhash = %s WHERE id = %s"
    cursor.execute(query, (passwordhash, id))
    connection.commit()
    cursor.close()
    connection.close()

# Delete customer
def delete_customer(id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM customers WHERE id = %s"
    cursor.execute(query, (id,))
    connection.commit()
    cursor.close()
    connection.close()

# Check if customer has active borrowings
def customer_has_active_borrowing(customer_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "SELECT COUNT(*) FROM borrowingrecords WHERE customerid = %s AND returndate IS NULL"
    cursor.execute(query, (customer_id,))
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count > 0

# Create a new loan/borrowing
def create_loan(book_id, customer_id, borrow_date):
    # Format date if it's a string
    if isinstance(borrow_date, str):
        borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').date()
    
    connection = get_connection()
    cursor = connection.cursor()
    
    # Check if book is available
    cursor.execute("SELECT status FROM books WHERE id = %s", (book_id,))
    book_status = cursor.fetchone()
    if not book_status or book_status[0] != 'available':
        cursor.close()
        connection.close()
        return False, "Book is not available for borrowing"
    
    # Check if customer already has a book borrowed
    if customer_has_active_borrowing(customer_id):
        cursor.close()
        connection.close()
        return False, "Customer already has an active borrowing"
    
    # Create borrowing record
    query = "INSERT INTO borrowingrecords (bookid, customerid, borrowdate) VALUES (%s, %s, %s)"
    cursor.execute(query, (book_id, customer_id, borrow_date))
    
    # Update book status to unavailable
    update_query = "UPDATE books SET status = 'unavailable' WHERE id = %s"
    cursor.execute(update_query, (book_id,))
    
    connection.commit()
    cursor.close()
    connection.close()
    return True, "Borrowing record created successfully"

# Get all active loans
def get_active_loans():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT borrowingrecords.id, borrowingrecords.bookid, borrowingrecords.customerid, borrowingrecords.borrowdate, 
           books.title as book_title, 
           CONCAT(customers.firstname, ' ', customers.lastname) as customer_name
    FROM borrowingrecords
    JOIN books ON borrowingrecords.bookid = books.id
    JOIN customers ON borrowingrecords.customerid = customers.id
    WHERE borrowingrecords.returndate IS NULL
    """
    cursor.execute(query)
    loans = cursor.fetchall()
    cursor.close()
    connection.close()
    return loans

# Get all loans (including returned)
def get_loans():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT borrowingrecords.id, borrowingrecords.bookid, borrowingrecords.customerid, borrowingrecords.borrowdate, borrowingrecords.returndate, borrowingrecords.late_fee,
           books.title as book_title, 
           CONCAT(customers.firstname, ' ', customers.lastname) as customer_name
    FROM borrowingrecords
    JOIN books ON borrowingrecords.bookid = books.id
    JOIN customers ON borrowingrecords.customerid = customers.id
    """
    cursor.execute(query)
    loans = cursor.fetchall()
    cursor.close()
    connection.close()
    return loans

# Get a single loan by ID
def get_loan(id):
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT borrowingrecords.id, borrowingrecords.bookid, borrowingrecords.customerid, borrowingrecords.borrowdate, borrowingrecords.returndate, borrowingrecords.late_fee,
           books.title as book_title, 
           CONCAT(customers.firstname, ' ', customers.lastname) as customer_name
    FROM borrowingrecords
    JOIN books ON borrowingrecords.bookid = books.id
    JOIN customers ON borrowingrecords.customerid = customers.id
    WHERE borrowingrecords.id = %s
    """
    cursor.execute(query, (id,))
    loan = cursor.fetchone()
    cursor.close()
    connection.close()
    return loan

# Process book return
def return_book(loan_id, return_date):
    # Format date if it's a string
    if isinstance(return_date, str):
        return_date = datetime.strptime(return_date, '%Y-%m-%d').date()
    
    connection = get_connection()
    cursor = connection.cursor()
    
    # Get the loan details
    cursor.execute("SELECT bookid, borrowdate FROM borrowingrecords WHERE id = %s", (loan_id,))
    loan = cursor.fetchone()
    
    if not loan:
        cursor.close()
        connection.close()
        return False, "Loan record not found"
    
    book_id, borrow_date = loan
    
    # Calculate late fee if applicable (more than 10 days)
    borrow_date = borrow_date if isinstance(borrow_date, datetime.date) else borrow_date.date()
    due_date = borrow_date + timedelta(days=10)
    
    late_fee = 0.0
    if return_date > due_date:
        days_late = (return_date - due_date).days
        late_fee = days_late * 1.0  # $1 per day late
    
    # Update the loan record with return date and late fee
    update_query = "UPDATE borrowingrecords SET returndate = %s, late_fee = %s WHERE id = %s"
    cursor.execute(update_query, (return_date, late_fee, loan_id))
    
    # Set the book status back to available
    book_update_query = "UPDATE books SET status = 'available' WHERE id = %s"
    cursor.execute(book_update_query, (book_id,))
    
    connection.commit()
    cursor.close()
    connection.close()
    return True, "Book returned successfully"

# Get available books (for borrowing)
def get_available_books():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE status = 'available'")
    books = cursor.fetchall()
    cursor.close()
    connection.close()
    return books

# Get customers without active borrowings
def get_available_customers():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT customers.id, customers.firstname, customers.lastname, customers.email
    FROM customers
    WHERE customers.id NOT IN (
        SELECT DISTINCT customerid 
        FROM borrowingrecords 
        WHERE returndate IS NULL
    )
    """
    cursor.execute(query)
    customers = cursor.fetchall()
    cursor.close()
    connection.close()
    return customers
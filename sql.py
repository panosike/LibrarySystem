import mysql.connector 
from credentials import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

#Creating and returning DB connection 
def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
#Adds a new book to system 
def create_book(title, author, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO books (title, author, genre) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (title, author, genre))
    connection.commit()
    cursor.close()
    connection.close()
    
#Gets all books
def get_books(): 
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    return books 

#Update the details of the book 
def update_book(book_id, title, author, genre):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE books SET title = %s, author =%s, genre = %s WHERE book_id = %s"
    cursor.execute(query, (title, author, genre, book_id))
    connection.commit()
    cursor.close()
    connection.close()
    
#Delete book by book id 
def delete_book(book_id):
    connection = get_connection()
    cursor = connection.cursor()
    query = "DELETE FROM books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    connection.commit()
    cursor.close()
    connection.close()
    
#Add new user
def add_user(username, email):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO users (username, email) VALUES (%s, %s)"
    cursor.execute(query, (username, email))
    connection.commit()
    cursor.close()
    connection.close()
    
#Retrieve all users
def get_users():
    connection=get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    cursor.close()
    connection.close()
    return users

#Borrowing system and entry 
def create_loan(book_id, user_id, loan_date, return_date):
    connection = get_connection()
    cursor = connection.cursor()
    query = """INSERT INTO loans (book_id, user_id, loan_date, return_date) VALUES (%s, %s, %s, %s) """
    cursor.execute(query, (book_id, user_id, loan_date, return_date))
    connection.commit()
    cursor.close()
    connection.close()
    
#Getting loans details 
def get_loans():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("""
        SELECT loans.loan_id, books.title, users.username, loans.loan_date, loans.return_date
        FROM loans
        JOIN books ON loans.book_id = books.book_id
        JOIN users ON loans.user_id = users.user_id 
    """)
    loans = cursor.fetchall()
    cursor.close()
    connection.close()
    return loans 

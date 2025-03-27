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
def create_book(title, author, year):
    connection = get_connection()
    cursor = connection.cursor()
    query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
    cursor.execute(query, (title, author, year))
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
def update_book(book_id, title, author, year):
    connection = get_connection()
    cursor = connection.cursor()
    query = "UPDATE books SET title = %s, author =%s, year = %s WHERE book_id = %s"
    cursor.execute(query, (title, author, year, book_id))
    connection.commit()
    cursor.close()
    connection.close()
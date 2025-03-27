from flask import Flask, jsonify, request
from sql import create_book, get_books, update_book, delete_book, add_user, get_users, create_loan, get_loans
import credentials

app = Flask(__name__)

#Routes for the books 
@app.route('/books', methods=['GET'])
def fetch_books():
    books = get_books()
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    create_book(data['title'], data['author'], data['year'])
    return jsonify({"message": "Book successfully added"}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def modify_book(book_id):
    data = request.json
    update_book(book_id, data['title'], data['author'], data['year'])
    return jsonify({"message": "Book successfully updated"})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def remove_book(book_id):
    delete_book(book_id)
    return jsonify({"message": "Book successfully deleted"})

#Routes for users 
@app.route('/users', methods=['GET'])
def fetch_users():
    user = get_users()
    return jsonify(user)

@app.route('/users', methods=['POST'])
def add_new_user():
    data = request.json
    add_user(data['username'], data['email'])
    return jsonify({"message": "User successfully added"}), 201

#Routes for borrowing/loans
@app.route('/loans', methods=['GET'])
def fetch_loans():
    loans = get_loans()
    return jsonify(loans)

@app.route('/loans', methods=['POST'])
def add_loan():
    data = request.json
    create_loan(data['book_id'], data['user_id'], data['loan_date'], data['return_date'])
    return jsonify({"message": "Loan successfully created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
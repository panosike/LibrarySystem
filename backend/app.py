from flask import Flask, jsonify, request, render_template
import sql
from datetime import datetime

app = Flask(__name__)

# Initialize database when app starts
@app.before_request
def init_db():
    sql.initialize_database()

# Routes for the books 
@app.route('/books', methods=['GET'])
def fetch_books():
    books = sql.get_books()
    return jsonify(books)

@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    sql.create_book(data['title'], data['author'], data['genre'])
    return jsonify({"message": "Book successfully added"}), 201

@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    book = sql.get_book(id)
    if book:
        return jsonify(book)
    return jsonify({"message": "Book not found"}), 404

@app.route('/books/<int:id>', methods=['PUT'])
def modify_book(id):
    data = request.json
    sql.update_book(id, data['title'], data['author'], data['genre'])
    return jsonify({"message": "Book successfully updated"})

@app.route('/books/<int:id>', methods=['DELETE'])
def remove_book(id):
    sql.delete_book(id)
    return jsonify({"message": "Book successfully deleted"})

@app.route('/books/available', methods=['GET'])
def get_available_books():
    books = sql.get_available_books()
    return jsonify(books)

# Routes for customers 
@app.route('/customers', methods=['GET'])
def fetch_customers():
    customers = sql.get_customers()
    return jsonify(customers)

@app.route('/customers', methods=['POST'])
def add_new_customer():
    data = request.json
    sql.add_customer(data['firstname'], data['lastname'], data['email'], data['password'])
    return jsonify({"message": "Customer successfully added"}), 201

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = sql.get_customer(id)
    if customer:
        return jsonify(customer)
    return jsonify({"message": "Customer not found"}), 404

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    data = request.json
    sql.update_customer(id, data['firstname'], data['lastname'], data['email'])
    
    # Update password if provided
    if 'password' in data and data['password']:
        sql.update_customer_password(id, data['password'])
        
    return jsonify({"message": "Customer successfully updated"})

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    # Check if customer has active loans before deleting
    if sql.customer_has_active_borrowing(id):
        return jsonify({"message": "Cannot delete customer with active borrowings"}), 400
        
    sql.delete_customer(id)
    return jsonify({"message": "Customer successfully deleted"})

@app.route('/customers/available', methods=['GET'])
def get_available_customers():
    customers = sql.get_available_customers()
    return jsonify(customers)

# Routes for borrowing/loans
@app.route('/loans', methods=['GET'])
def get_all_loans():
    loans = sql.get_loans()
    return jsonify(loans)

@app.route('/loans/active', methods=['GET'])
def get_active_loans():
    active_loans = sql.get_active_loans()
    return jsonify(active_loans)

@app.route('/loans/<int:id>', methods=['GET'])
def get_loan(id):
    loan = sql.get_loan(id)
    if loan:
        return jsonify(loan)
    return jsonify({"message": "Loan not found"}), 404

@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    book_id = data['book_id']
    customer_id = data['customer_id']
    
    # Use current date if borrow_date not provided
    borrow_date = data.get('borrow_date', datetime.now().strftime('%Y-%m-%d'))
    
    success, message = sql.create_loan(book_id, customer_id, borrow_date)
    
    if success:
        return jsonify({"message": message}), 201
    else:
        return jsonify({"message": message}), 400

@app.route('/loans/<int:id>/return', methods=['POST'])
def return_book(id):
    data = request.json
    return_date = data.get('return_date', datetime.now().strftime('%Y-%m-%d'))
    
    success, message = sql.return_book(id, return_date)
    
    if success:
        return jsonify({"message": message})
    else:
        return jsonify({"message": message}), 400


if __name__ == '__main__':
    app.run(debug=True)
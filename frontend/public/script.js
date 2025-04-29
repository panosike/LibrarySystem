document.addEventListener('DOMContentLoaded', function () {
    // API base URL
    const API_BASE_URL = '/api'; // Changed to use our frontend server API routes

    // DOM elements
    const booksTableBody = document.getElementById('books-table-body');
    const customersTableBody = document.getElementById('customers-table-body');
    const activeLoansTableBody = document.getElementById('active-loans-table-body');
    const loansHistoryTableBody = document.getElementById('loans-history-table-body');

    // Modal elements for books
    const addBookForm = document.getElementById('add-book-form');
    const saveBookBtn = document.getElementById('save-book-btn');
    const editBookForm = document.getElementById('edit-book-form');
    const updateBookBtn = document.getElementById('update-book-btn');

    // Modal elements for customers
    const addCustomerForm = document.getElementById('add-customer-form');
    const saveCustomerBtn = document.getElementById('save-customer-btn');
    const editCustomerForm = document.getElementById('edit-customer-form');
    const updateCustomerBtn = document.getElementById('update-customer-btn');

    // Modal elements for loans
    const createLoanForm = document.getElementById('create-loan-form');
    const saveLoanBtn = document.getElementById('save-loan-btn');
    const returnBookForm = document.getElementById('return-book-form');
    const confirmReturnBtn = document.getElementById('confirm-return-btn');

    // Dropdown elements for loans
    const loanBookSelect = document.getElementById('loan-book');
    const loanCustomerSelect = document.getElementById('loan-customer');

    // Load data when tabs are clicked
    document.getElementById('books-tab').addEventListener('click', loadBooks);
    document.getElementById('customers-tab').addEventListener('click', loadCustomers);
    document.getElementById('borrowing-tab').addEventListener('click', () => {
        loadActiveLoans();
        loadLoanHistory();
    });

    // Load books when page loads
    loadBooks();

    // Create loan modal opened
    const createLoanModal = document.getElementById('createLoanModal');
    createLoanModal.addEventListener('show.bs.modal', loadCreateLoanData);

    // Load all books
    function loadBooks() {
        fetch(`${API_BASE_URL}/books`)
            .then(response => response.json())
            .then(books => {
                booksTableBody.innerHTML = '';
                books.forEach(book => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td>${book.id}</td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td>${book.genre}</td>
                    <td>${book.status}</td>
                    <td class="action-buttons">
                        <button class="btn btn-sm btn-primary edit-book" data-id="${book.id}">Edit</button>
                        <button class="btn btn-sm btn-danger delete-book" data-id="${book.id}">Delete</button>
                    </td>
                `;
                    booksTableBody.appendChild(row);
                });

                // Add event listeners to edit and delete buttons
                document.querySelectorAll('.edit-book').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const id = e.target.getAttribute('data-id');
                        loadBookForEdit(id);
                    });
                });

                document.querySelectorAll('.delete-book').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const id = e.target.getAttribute('data-id');
                        if (confirm('Are you sure you want to delete this book?')) {
                            deleteBook(id);
                        }
                    });
                });
            })
            .catch(error => console.error('Error loading books:', error));
    }

    // Add new book
    saveBookBtn.addEventListener('click', () => {
        const title = document.getElementById('book-title').value;
        const author = document.getElementById('book-author').value;
        const genre = document.getElementById('book-genre').value;

        fetch(`${API_BASE_URL}/books`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, author, genre }),
        })
            .then(response => response.json())
            .then(data => {
                // Close modal and reload books
                const modal = bootstrap.Modal.getInstance(document.getElementById('addBookModal'));
                modal.hide();
                loadBooks();
                // Reset form
                addBookForm.reset();
            })
            .catch(error => console.error('Error adding book:', error));
    });

    // Load book for editing
    function loadBookForEdit(id) {
        fetch(`${API_BASE_URL}/books/${id}`)
            .then(response => response.json())
            .then(book => {
                document.getElementById('edit-book-id').value = book.id;
                document.getElementById('edit-book-title').value = book.title;
                document.getElementById('edit-book-author').value = book.author;
                document.getElementById('edit-book-genre').value = book.genre;

                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('editBookModal'));
                modal.show();
            })
            .catch(error => console.error('Error loading book for edit:', error));
    }

    // Update book
    updateBookBtn.addEventListener('click', () => {
        const id = document.getElementById('edit-book-id').value;
        const title = document.getElementById('edit-book-title').value;
        const author = document.getElementById('edit-book-author').value;
        const genre = document.getElementById('edit-book-genre').value;

        fetch(`${API_BASE_URL}/books/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ title, author, genre }),
        })
            .then(response => response.json())
            .then(data => {
                // Close modal and reload books
                const modal = bootstrap.Modal.getInstance(document.getElementById('editBookModal'));
                modal.hide();
                loadBooks();
            })
            .catch(error => console.error('Error updating book:', error));
    });

    // Delete book
    function deleteBook(id) {
        fetch(`${API_BASE_URL}/books/${id}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                loadBooks();
            })
            .catch(error => console.error('Error deleting book:', error));
    }

    // Load all customers
    function loadCustomers() {
        fetch(`${API_BASE_URL}/customers`)
            .then(response => response.json())
            .then(customers => {
                customersTableBody.innerHTML = '';
                customers.forEach(customer => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                    <td>${customer.id}</td>
                    <td>${customer.firstname}</td>
                    <td>${customer.lastname}</td>
                    <td>${customer.email}</td>
                    <td class="action-buttons">
                        <button class="btn btn-sm btn-primary edit-customer" data-id="${customer.id}">Edit</button>
                        <button class="btn btn-sm btn-danger delete-customer" data-id="${customer.id}">Delete</button>
                    </td>
                `;
                    customersTableBody.appendChild(row);
                });

                // Add event listeners to edit and delete buttons
                document.querySelectorAll('.edit-customer').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const id = e.target.getAttribute('data-id');
                        loadCustomerForEdit(id);
                    });
                });

                document.querySelectorAll('.delete-customer').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const id = e.target.getAttribute('data-id');
                        if (confirm('Are you sure you want to delete this customer?')) {
                            deleteCustomer(id);
                        }
                    });
                });
            })
            .catch(error => console.error('Error loading customers:', error));
    }

    // Add new customer
    saveCustomerBtn.addEventListener('click', () => {
        const firstname = document.getElementById('customer-firstname').value;
        const lastname = document.getElementById('customer-lastname').value;
        const email = document.getElementById('customer-email').value;
        const password = document.getElementById('customer-password').value;

        fetch(`${API_BASE_URL}/customers`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ firstname, lastname, email, password }),
        })
            .then(response => response.json())
            .then(data => {
                // Close modal and reload customers
                const modal = bootstrap.Modal.getInstance(document.getElementById('addCustomerModal'));
                modal.hide();
                loadCustomers();
                // Reset form
                addCustomerForm.reset();
            })
            .catch(error => console.error('Error adding customer:', error));
    });

    // Load customer for editing
    function loadCustomerForEdit(id) {
        fetch(`${API_BASE_URL}/customers/${id}`)
            .then(response => response.json())
            .then(customer => {
                document.getElementById('edit-customer-id').value = customer.id;
                document.getElementById('edit-customer-firstname').value = customer.firstname;
                document.getElementById('edit-customer-lastname').value = customer.lastname;
                document.getElementById('edit-customer-email').value = customer.email;

                // Show modal
                const modal = new bootstrap.Modal(document.getElementById('editCustomerModal'));
                modal.show();
            })
            .catch(error => console.error('Error loading customer for edit:', error));
    }

    // Update customer
    updateCustomerBtn.addEventListener('click', () => {
        const id = document.getElementById('edit-customer-id').value;
        const firstname = document.getElementById('edit-customer-firstname').value;
        const lastname = document.getElementById('edit-customer-lastname').value;
        const email = document.getElementById('edit-customer-email').value;
        const password = document.getElementById('edit-customer-password').value;

        fetch(`${API_BASE_URL}/customers/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ firstname, lastname, email, password }),
        })
            .then(response => response.json())
            .then(data => {
                // Close modal and reload customers
                const modal = bootstrap.Modal.getInstance(document.getElementById('editCustomerModal'));
                modal.hide();
                loadCustomers();
            })
            .catch(error => console.error('Error updating customer:', error));
    });

    // Delete customer
    function deleteCustomer(id) {
        fetch(`${API_BASE_URL}/customers/${id}`, {
            method: 'DELETE',
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then(data => {
                loadCustomers();
            })
            .catch(error => {
                alert(error.message || 'Error deleting customer');
                console.error('Error deleting customer:', error);
            });
    }

    // Load active loans
    function loadActiveLoans() {
        fetch(`${API_BASE_URL}/loans/active`)
            .then(response => response.json())
            .then(loans => {
                activeLoansTableBody.innerHTML = '';
                loans.forEach(loan => {
                    const row = document.createElement('tr');
                    const borrowDate = new Date(loan.borrowdate).toLocaleDateString();

                    row.innerHTML = `
                    <td>${loan.id}</td>
                    <td>${loan.book_title}</td>
                    <td>${loan.customer_name}</td>
                    <td>${borrowDate}</td>
                    <td class="action-buttons">
                        <button class="btn btn-sm btn-success return-book" data-id="${loan.id}">Return</button>
                    </td>
                `;
                    activeLoansTableBody.appendChild(row);
                });

                // Add event listeners to return buttons
                document.querySelectorAll('.return-book').forEach(button => {
                    button.addEventListener('click', (e) => {
                        const id = e.target.getAttribute('data-id');
                        prepareBookReturn(id);
                    });
                });
            })
            .catch(error => console.error('Error loading active loans:', error));
    }

    // Load loan history
    function loadLoanHistory() {
        fetch(`${API_BASE_URL}/loans`)
            .then(response => response.json())
            .then(loans => {
                loansHistoryTableBody.innerHTML = '';
                // Filter completed loans (those with returndate)
                const completedLoans = loans.filter(loan => loan.returndate);

                completedLoans.forEach(loan => {
                    const row = document.createElement('tr');
                    const borrowDate = new Date(loan.borrowdate).toLocaleDateString();
                    const returnDate = loan.returndate ? new Date(loan.returndate).toLocaleDateString() : '-';

                    row.innerHTML = `
                    <td>${loan.id}</td>
                    <td>${loan.book_title}</td>
                    <td>${loan.customer_name}</td>
                    <td>${borrowDate}</td>
                    <td>${returnDate}</td>
                    <td>${loan.late_fee || '0.00'}</td>
                `;
                    loansHistoryTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error loading loan history:', error));
    }

    // Load data for create loan modal
    function loadCreateLoanData() {
        // Load available books
        fetch(`${API_BASE_URL}/books/available`)
            .then(response => response.json())
            .then(books => {
                loanBookSelect.innerHTML = '<option value="">Select a book</option>';
                books.forEach(book => {
                    const option = document.createElement('option');
                    option.value = book.id;
                    option.textContent = `${book.title} (${book.author})`;
                    loanBookSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error loading books for loan:', error));

        // Load available customers
        fetch(`${API_BASE_URL}/customers/available`)
            .then(response => response.json())
            .then(customers => {
                loanCustomerSelect.innerHTML = '<option value="">Select a customer</option>';
                customers.forEach(customer => {
                    const option = document.createElement('option');
                    option.value = customer.id;
                    option.textContent = `${customer.firstname} ${customer.lastname}`;
                    loanCustomerSelect.appendChild(option);
                });
            })
            .catch(error => console.error('Error loading customers for loan:', error));

        // Set today's date as default for borrow date
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('loan-borrow-date').value = today;
    }

    // Prepare book return
    function prepareBookReturn(id) {
        document.getElementById('return-loan-id').value = id;

        // Set today's date as default for return date
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('loan-return-date').value = today;

        // Show modal
        const modal = new bootstrap.Modal(document.getElementById('returnBookModal'));
        modal.show();
    }

    // Create new loan
    saveLoanBtn.addEventListener('click', () => {
        const book_id = loanBookSelect.value;
        const customer_id = loanCustomerSelect.value;
        const borrow_date = document.getElementById('loan-borrow-date').value;

        if (!book_id || !customer_id) {
            alert('Please select both a book and a customer');
            return;
        }

        fetch(`${API_BASE_URL}/loans`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ book_id, customer_id, borrow_date }),
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then(data => {
                // Close modal and reload loans
                const modal = bootstrap.Modal.getInstance(document.getElementById('createLoanModal'));
                modal.hide();
                loadActiveLoans();
                // Reset form
                createLoanForm.reset();
            })
            .catch(error => {
                alert(error.message || 'Error creating loan');
                console.error('Error creating loan:', error);
            });
    });

    // Confirm return book
    confirmReturnBtn.addEventListener('click', () => {
        const id = document.getElementById('return-loan-id').value;
        const return_date = document.getElementById('loan-return-date').value;

        fetch(`${API_BASE_URL}/loans/${id}/return`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ return_date }),
        })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(data => {
                        throw new Error(data.message);
                    });
                }
                return response.json();
            })
            .then(data => {
                // Close modal and reload loans
                const modal = bootstrap.Modal.getInstance(document.getElementById('returnBookModal'));
                modal.hide();
                loadActiveLoans();
                loadLoanHistory();
            })
            .catch(error => {
                alert(error.message || 'Error returning book');
                console.error('Error returning book:', error);
            });
    });
});
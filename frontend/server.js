const express = require('express');
const app = express();
const axios = require('axios');
const bodyParser = require('body-parser');

// Configure middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());
app.use(express.static('public'));

// Set EJS as the view engine
app.set('view engine', 'ejs');

// API base URL
const API_BASE_URL = 'https://librarysystem-mbi9.onrender.com';

// Home route - render the main page
app.get('/', (req, res) => {
    res.render('index');
});

// Books API routes
app.get('/api/books', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/books`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching books:', error);
        res.status(500).json({ message: 'Error fetching books' });
    }
});

app.get('/api/books/available', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/books/available`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching available books:', error);
        res.status(500).json({ message: 'Error fetching available books' });
    }
});

app.post('/api/books', async (req, res) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/books`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error adding book:', error);
        res.status(500).json({ message: 'Error adding book' });
    }
});

app.put('/api/books/:id', async (req, res) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/books/${req.params.id}`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error updating book:', error);
        res.status(500).json({ message: 'Error updating book' });
    }
});

app.delete('/api/books/:id', async (req, res) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/books/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        console.error('Error deleting book:', error);
        res.status(500).json({ message: 'Error deleting book' });
    }
});

// Customers API routes
app.get('/api/customers', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/customers`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching customers:', error);
        res.status(500).json({ message: 'Error fetching customers' });
    }
});

app.get('/api/customers/available', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/customers/available`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching available customers:', error);
        res.status(500).json({ message: 'Error fetching available customers' });
    }
});

app.post('/api/customers', async (req, res) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/customers`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error adding customer:', error);
        res.status(500).json({ message: 'Error adding customer' });
    }
});

app.put('/api/customers/:id', async (req, res) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/customers/${req.params.id}`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error updating customer:', error);
        res.status(500).json({ message: 'Error updating customer' });
    }
});

app.delete('/api/customers/:id', async (req, res) => {
    try {
        const response = await axios.delete(`${API_BASE_URL}/customers/${req.params.id}`);
        res.json(response.data);
    } catch (error) {
        console.error('Error deleting customer:', error);
        res.status(500).json({ message: 'Error deleting customer' });
    }
});

// Loans API routes
app.get('/api/loans', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/loans`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching loans:', error);
        res.status(500).json({ message: 'Error fetching loans' });
    }
});

app.get('/api/loans/active', async (req, res) => {
    try {
        const response = await axios.get(`${API_BASE_URL}/loans/active`);
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching active loans:', error);
        res.status(500).json({ message: 'Error fetching active loans' });
    }
});

app.post('/api/loans', async (req, res) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/loans`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error creating loan:', error);
        res.status(500).json({ message: 'Error creating loan' });
    }
});

app.post('/api/loans/:id/return', async (req, res) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/loans/${req.params.id}/return`, req.body);
        res.json(response.data);
    } catch (error) {
        console.error('Error returning book:', error);
        res.status(500).json({ message: 'Error returning book' });
    }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Frontend server running on http://localhost:${PORT}`);
});
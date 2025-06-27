import express from 'express';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import jwt from 'jsonwebtoken';

const app = express();
app.use(cors());
app.use(express.json());

const SECRET_KEY = 'mysecretkey';
const ALGORITHM = 'HS256';

// Database setup (async)
let userDb, customerDb, addressDb;
(async () => {
  userDb = await open({ filename: '../todo.db', driver: sqlite3.Database });
  customerDb = await open({ filename: '../customer.db', driver: sqlite3.Database });
  addressDb = await open({ filename: '../address.db', driver: sqlite3.Database });
})();

function createJwtToken(username) {
  return jwt.sign({ sub: username }, SECRET_KEY, { expiresIn: '1d' });
}

// Register
app.post('/register', async (req, res) => {
  const { name, email, phone, username, password, profile_picture } = req.body;
  try {
    await userDb.run(`INSERT INTO users (name, email, phone, username, password, profile_picture) VALUES (?, ?, ?, ?, ?, ?)`,
      name, email, phone, username, password, profile_picture);
    res.json({ message: 'User registered successfully' });
  } catch (e) {
    res.status(400).json({ error: e.message });
  }
});

// Login
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  const user = await userDb.get('SELECT * FROM users WHERE username = ?', username);
  if (!user || user.password !== password) {
    return res.status(400).json({ detail: 'Invalid credentials' });
  }
  const token = createJwtToken(user.username);
  res.json({ access_token: token, token_type: 'bearer' });
});

// Create customer
app.post('/customer', async (req, res) => {
  const c = req.body;
  if (c.username) {
    const existing = await customerDb.get('SELECT * FROM customers WHERE username = ?', c.username);
    if (existing) return res.status(400).json({ detail: 'Username already exists' });
  }
  const stmt = `INSERT INTO customers (facebook_id, email, license_key, name, phone, username, password, payment, transaction_id, date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`;
  const result = await customerDb.run(stmt, c.facebook_id, c.email, c.license_key, c.name, c.phone, c.username, c.password, c.payment, c.transaction_id, c.date);
  res.json({ id: result.lastID });
});

// Get all customers
app.get('/customers', async (req, res) => {
  const customers = await customerDb.all('SELECT * FROM customers');
  res.json(customers);
});

// Get customer by id
app.get('/customer/:customer_id', async (req, res) => {
  const c = await customerDb.get('SELECT * FROM customers WHERE id = ?', req.params.customer_id);
  if (!c) return res.status(404).json({ detail: 'Customer not found' });
  res.json(c);
});

// Update customer
app.put('/customer/:customer_id', async (req, res) => {
  const c = req.body;
  const id = req.params.customer_id;
  const existing = await customerDb.get('SELECT * FROM customers WHERE id = ?', id);
  if (!existing) return res.status(404).json({ detail: 'Customer not found' });
  const update = `UPDATE customers SET facebook_id=?, email=?, license_key=?, name=?, phone=?, username=?, password=?, payment=?, transaction_id=?, date=? WHERE id=?`;
  await customerDb.run(update, c.facebook_id, c.email, c.license_key, c.name, c.phone, c.username, c.password, c.payment, c.transaction_id, c.date, id);
  res.json({ message: 'Customer updated successfully' });
});

// Delete customer
app.delete('/customer/:customer_id', async (req, res) => {
  const id = req.params.customer_id;
  const existing = await customerDb.get('SELECT * FROM customers WHERE id = ?', id);
  if (!existing) return res.status(404).json({ detail: 'Customer not found' });
  await customerDb.run('DELETE FROM customers WHERE id = ?', id);
  res.json({ message: 'Customer deleted successfully' });
});

// Get address by index
app.get('/address/by-index/:index', async (req, res) => {
  const addresses = await addressDb.all('SELECT * FROM addresses ORDER BY id');
  const idx = parseInt(req.params.index, 10);
  if (!addresses || idx < 0 || idx >= addresses.length) {
    return res.status(404).json({ detail: 'Address index out of range' });
  }
  const address = addresses[idx];
  res.json({
    id: address.id,
    street: address.street,
    city: address.city,
    province: address.province,
    zip: address.zip
  });
});

// Message endpoint
app.get('/message', (req, res) => {
  setTimeout(() => {
    res.json({ message: 'Hello there!' });
  }, 2000);
});

// Profile endpoints
app.get('/profile/:username', async (req, res) => {
  const user = await userDb.get('SELECT * FROM users WHERE username = ?', req.params.username);
  if (!user) return res.status(404).json({ detail: 'User not found' });
  res.json({ username: user.username, password: user.password });
});

app.put('/profile/:username', async (req, res) => {
  const { username, password } = req.body;
  const user = await userDb.get('SELECT * FROM users WHERE username = ?', req.params.username);
  if (!user) return res.status(404).json({ detail: 'User not found' });
  if (username) {
    const existing = await userDb.get('SELECT * FROM users WHERE username = ?', username);
    if (existing && existing.id !== user.id) {
      return res.status(400).json({ detail: 'Username already exists' });
    }
    await userDb.run('UPDATE users SET username = ? WHERE id = ?', username, user.id);
  }
  if (password) {
    await userDb.run('UPDATE users SET password = ? WHERE id = ?', password, user.id);
  }
  res.json({ message: 'Profile updated successfully' });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});

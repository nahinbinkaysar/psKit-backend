# JS Backend for Customer Management (Express + SQLite)

## Endpoints
- POST   `/register`           — Register a user
- POST   `/login`              — Login and get JWT
- POST   `/customer`           — Create customer
- GET    `/customers`          — List all customers
- GET    `/customer/:id`       — Get customer by id
- PUT    `/customer/:id`       — Update customer
- DELETE `/customer/:id`       — Delete customer
- GET    `/address/by-index/:index` — Get address by index
- GET    `/message`            — Demo message endpoint
- GET    `/profile/:username`  — Get user profile
- PUT    `/profile/:username`  — Update user profile

## Setup
1. `cd backend`
2. `npm install`
3. Place your `todo.db`, `customer.db`, and `address.db` in the backend directory or update the DB paths in `index.js`.
4. `npm start` (for local dev)

## Deploy to Vercel
- Import this directory as a project in Vercel.
- Vercel will use `index.js` as the serverless entry point.

---
**Note:** This backend is a direct port of your FastAPI logic to Express/Node.js. Adjust DB paths as needed for your deployment.

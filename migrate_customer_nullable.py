import sqlite3

# Path to your customer.db
DB_PATH = "customer.db"

# Connect to the database
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# 1. Create a new table with correct nullable columns
c.execute('''
CREATE TABLE IF NOT EXISTS customers_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    facebook_id TEXT NULL,
    email TEXT NULL,
    license_key TEXT NULL,
    name TEXT NULL,
    phone TEXT NULL,
    username TEXT NULL,
    password TEXT NULL,
    payment TEXT NULL,
    transaction_id TEXT NULL,
    date TEXT NULL
)
''')

# 2. Copy data from old table to new table
c.execute('''
INSERT INTO customers_new (id, facebook_id, email, license_key, name, phone, username, password, payment, transaction_id, date)
SELECT id, facebook_id, email, license_key, name, phone, username, password, payment, transaction_id, date FROM customers
''')

# 3. Drop old table
c.execute('DROP TABLE customers')

# 4. Rename new table to original name
c.execute('ALTER TABLE customers_new RENAME TO customers')

conn.commit()
conn.close()

print("Migration complete: 'customers' table now allows NULLs for all fields.")

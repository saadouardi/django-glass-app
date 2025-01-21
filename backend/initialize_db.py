import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("image_data.db")
cursor = conn.cursor()

# Fetch all users
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

# Print users
print("📌 Users in Database:")
for user in users:
    print(user)

# Close connection
conn.close()

# Connect to the database (creates if not exists)
conn = sqlite3.connect("image_data.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

conn.commit()
conn.close()

print("✅ Users table created successfully!")

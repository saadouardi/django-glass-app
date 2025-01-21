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

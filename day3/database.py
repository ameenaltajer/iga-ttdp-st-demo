import sqlite3




# Write the python code (function) to write and read from the database. The function should be able to add a user and return all users in the database.



def init_db():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

# Function to add a user to the database
def add_user(name):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()


# Delete the user with id 1 from the database
def delete_user(number):
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (number,))
    conn.commit()
    conn.close()


# Function to get all users from the database and put them in a list
def get_all_users():
    conn = sqlite3.connect("example.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users
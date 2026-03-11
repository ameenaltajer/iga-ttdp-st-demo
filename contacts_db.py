import sqlite3
 
DB_NAME = "contacts.db"
 
 
def get_connection():
    return sqlite3.connect(DB_NAME)
 
 
def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
 
 
def get_all_contacts():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
 
 
def add_contact(name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contacts (name, email, phone) VALUES (?, ?, ?)",
        (name, email, phone)
    )
    conn.commit()
    contact_id = cursor.lastrowid
    conn.close()
    return contact_id
 
 
def get_contact_by_id(contact_id):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
 
 
def update_contact(contact_id, name, email, phone):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contacts SET name = ?, email = ?, phone = ? WHERE id = ?",
        (name, email, phone, contact_id)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0
 
 
def delete_contact(contact_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    return deleted > 0
 
 
def search_contacts(query):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    like_query = f"%{query}%"
    cursor.execute(
        """
        SELECT * FROM contacts
        WHERE name LIKE ? OR email LIKE ?
        """,
        (like_query, like_query)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
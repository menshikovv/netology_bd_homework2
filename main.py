import sqlite3

def create_database():
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS phones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            phone TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')

    conn.commit()
    conn.close()

def add_client(first_name, last_name, email):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO clients (first_name, last_name, email)
        VALUES (?, ?, ?)
    ''', (first_name, last_name, email))

    conn.commit()
    conn.close()

def add_phone(client_id, phone):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO phones (client_id, phone)
        VALUES (?, ?)
    ''', (client_id, phone))

    conn.commit()
    conn.close()

def update_client(client_id, first_name, last_name, email):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE clients
        SET first_name = ?, last_name = ?, email = ?
        WHERE id = ?
    ''', (first_name, last_name, email, client_id))

    conn.commit()
    conn.close()

def delete_phone(client_id):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM phones
        WHERE client_id = ?
    ''', (client_id,))

    conn.commit()
    conn.close()

def delete_client(client_id):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM clients
        WHERE id = ?
    ''', (client_id,))

    conn.commit()
    conn.close()

def find_client(query):
    conn = sqlite3.connect('clients.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT clients.*, GROUP_CONCAT(phones.phone, ', ') AS phone_numbers
        FROM clients
        LEFT JOIN phones ON clients.id = phones.client_id
        WHERE first_name LIKE ? OR last_name LIKE ? OR email LIKE ?
        GROUP BY clients.id
    ''', (f'%{query}%', f'%{query}%', f'%{query}%'))

    clients = cursor.fetchall()
    conn.close()
    return clients

if __name__ == "__main__":
    create_database()

    add_client('John', 'Doe', 'john@gmail.com')
    add_client('Jane', 'Smith', 'jane@gmail.com')
    add_client('Bob', 'Johnson', 'bob@gmail.com')

    add_phone(1, '123-456-7890')
    add_phone(3, '987-654-3210')

    update_client(2, 'Jane', 'Brown', 'jane.brown@gmail.com')

    delete_phone(1)

    delete_client(3)

    result = find_client('Jane')
    for row in result:
        print(f"ID: {row[0]}, First Name: {row[1]}, Last Name: {row[2]}, Email: {row[3]}, Phone Numbers: {row[4]}")

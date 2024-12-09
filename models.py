import sqlite3

def create_tables():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        is_seasonal BOOLEAN
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        stock INTEGER
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS suggestions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_name TEXT NOT NULL,
        allergen_name TEXT
    )''')
    conn.commit()
    conn.close()

def get_all_flavors():
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flavors")
    flavors = cursor.fetchall()
    conn.close()
    return flavors

def get_flavor_by_id(flavor_id):
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flavors WHERE id=?", (flavor_id,))
    flavor = cursor.fetchone()
    conn.close()
    return flavor
    conn.commit()
    conn.close()

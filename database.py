import sqlite3

# Database file path
DB_PATH = 'ice_cream_parlor.db'

def get_connection():
    """Establish a database connection and return the connection object."""
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_db():
    """Initialize the database (create tables if they don't exist)."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flavors (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        seasonal BOOLEAN
    );
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    ''')
    
    conn.commit()
    conn.close()

def add_flavor(name, description, seasonal=False):
    """Add a new flavor to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO flavors (name, description, seasonal) 
    VALUES (?, ?, ?)
    ''', (name, description, seasonal))
    
    conn.commit()
    conn.close()

def search_flavors(term):
    """Search for flavors that match the search term."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM flavors WHERE name LIKE ?", (f'%{term}%',))
    flavors = cursor.fetchall()
    
    conn.close()
    return flavors

def add_allergen(name):
    """Add a new allergen to the allergens table."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO allergens (name) VALUES (?)", (name,))
    
    conn.commit()
    conn.close()

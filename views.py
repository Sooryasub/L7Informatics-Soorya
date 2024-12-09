import sqlite3
from models import get_all_flavors, get_flavor_by_id

def search_flavors(search_term, is_seasonal=None):
    """Searches for flavors based on name and optional seasonality filter."""
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    query = "SELECT * FROM flavors WHERE name LIKE ?"
    params = [f'%{search_term}%']
    if is_seasonal is not None:
        query += " AND is_seasonal = ?"
        params.append(is_seasonal)
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def add_allergen(name):
    """Adds a new allergen to the database."""
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO allergens (name) VALUES (?)', (name,))
        conn.commit()
    except sqlite3.IntegrityError:
        print("Allergen already exists!")
    conn.close()

def get_cart_total(cart):
    """Calculates the total price of items in the cart."""
    total = 0
    for flavor_id, quantity in cart.items():
        flavor = get_flavor_by_id(flavor_id)
        if flavor:
            total += flavor['price'] * quantity 
    return total

def get_all_flavors():
    """Retrieves all flavors from the database."""
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flavors")
    flavors = cursor.fetchall()
    conn.close()
    return flavors

def get_flavor_by_id(flavor_id):
    """Retrieves a flavor by its ID."""
    conn = sqlite3.connect('ice_cream_parlor.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flavors WHERE id=?", (flavor_id,))
    flavor = cursor.fetchone()
    conn.close()
    return flavor 
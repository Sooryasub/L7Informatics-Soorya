import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management
DB_NAME = 'db/database.db'

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Drop tables if they exist (optional but helpful in resetting schema)
    c.execute('''DROP TABLE IF EXISTS flavors''')
    c.execute('''DROP TABLE IF EXISTS ingredients''')
    c.execute('''DROP TABLE IF EXISTS cart''')
    c.execute('''DROP TABLE IF EXISTS allergens''')
    c.execute('''DROP TABLE IF EXISTS flavor_allergens''')  # Drop junction table

    # Create the flavors table
    c.execute('''CREATE TABLE IF NOT EXISTS flavors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        seasonal INTEGER NOT NULL
    )''')

    # Create the ingredient table with quantity column
    c.execute('''CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        quantity INTEGER NOT NULL
    )''')

    # Create the cart table with quantity column
    c.execute('''CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flavor_id INTEGER,
        user_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY(flavor_id) REFERENCES flavors(id)
    )''')

    # Create the allergens table
    c.execute('''CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )''')

    # Create the flavor_allergens junction table
    c.execute('''CREATE TABLE IF NOT EXISTS flavor_allergens (
        flavor_id INTEGER,
        allergen_id INTEGER,
        PRIMARY KEY (flavor_id, allergen_id),
        FOREIGN KEY (flavor_id) REFERENCES flavors(id),
        FOREIGN KEY (allergen_id) REFERENCES allergens(id)
    )''')

    # Insert allergens data
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Nuts')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Dairy')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Gluten')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Pine Nuts')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Soy')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Eggs')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Shellfish')")
    c.execute("INSERT OR IGNORE INTO allergens (name) VALUES ('Wheat')")

    # Insert flavors data
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Vanilla', 0)")   # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Chocolate', 0)")  # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Strawberry', 0)") # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Mint', 0)")       # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Peppermint', 1)")  # Seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Pumpkin Spice', 1)")  # Seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Eggnog', 1)")      # Seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Maple Pecan', 1)")  # Seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Cinnamon', 1)")    # Seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Coffee', 0)")      # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Caramel', 0)")     # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Toffee', 0)")      # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Butter Pecan', 0)") # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Black Cherry', 0)") # Not seasonal
    c.execute("INSERT OR IGNORE INTO flavors (name, seasonal) VALUES ('Pistachio', 0)")    # Not seasonal

    # Insert flavor-allergen associations
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (1, 2)")  # Vanilla and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (1, 3)")  # Vanilla and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (2, 2)")  # Chocolate and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (3, 2)")  # Strawberry and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (4, 3)")  # Mint and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (5, 2)")  # Peppermint and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (5, 1)")  # Peppermint and Nuts
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (6, 2)")  # Pumpkin Spice and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (6, 1)")  # Pumpkin Spice and Nuts
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (7, 2)")  # Eggnog and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (7, 3)")  # Eggnog and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (8, 1)")  # Maple Pecan and Nuts
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (8, 2)")  # Maple Pecan and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (9, 3)")  # Cinnamon and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (10, 2)") # Coffee and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (10, 3)") # Coffee and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (11, 2)") # Caramel and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (11, 3)") # Caramel and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (12, 2)") # Toffee and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (12, 3)") # Toffee and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (13, 2)") # Butter Pecan and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (13, 3)") # Butter Pecan and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (14, 2)") # Black Cherry and Dairy
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (14, 3)") # Black Cherry and Gluten
    c.execute("INSERT OR IGNORE INTO flavor_allergens (flavor_id, allergen_id) VALUES (15, 2)") # Pistachio and Dairy

    conn.commit()
    conn.close()


def get_flavors_with_allergens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Query to get all flavors and their associated allergens
    query = '''
        SELECT 
            flavors.id,
            flavors.name AS flavor_name,
            flavors.seasonal,
            GROUP_CONCAT(allergens.name, ', ') AS allergens_list
        FROM 
            flavors
        LEFT JOIN 
            flavor_allergens ON flavors.id = flavor_allergens.flavor_id
        LEFT JOIN 
            allergens ON flavor_allergens.allergen_id = allergens.id
        GROUP BY 
            flavors.id
        ORDER BY 
            flavors.name ASC
    '''
    c.execute(query)
    results = c.fetchall()
    conn.close()

    # Format results for display
    flavors_data = []
    for row in results:
        flavor_id, flavor_name, seasonal, allergens_list = row
        seasonal_status = "Seasonal" if seasonal == 1 else "Non-Seasonal"
        allergens_text = f"{flavor_name} contains {allergens_list}" if allergens_list else f"{flavor_name} contains no allergens"
        flavors_data.append({
            "Flavor": flavor_name,
            "Status": seasonal_status,
            "Allergens": allergens_text
        })

    return flavors_data


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        role = request.form['role']
        if role == 'owner':
            return redirect(url_for('owner_login'))
        else:
            # Customer can directly view the customer dashboard without login
            return redirect(url_for('customer_dashboard'))

    return render_template('select_role.html')

@app.route('/owner_login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('db/database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()

        if user:
            session['user_id'] = user[0]
            session['role'] = user[3]
            return redirect(url_for('owner_dashboard'))
        else:
            return "Invalid credentials", 401

    return render_template('owner_login.html')

@app.route('/owner_dashboard')
def owner_dashboard():
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM flavors")
    flavors = c.fetchall()
    conn.close()

    return render_template('owner_dashboard.html', flavors=flavors)

@app.route('/owner_inventory', methods=['GET', 'POST'])
def owner_inventory():
    if 'role' not in session or session['role'] != 'owner':
        return redirect(url_for('login'))

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if request.method == 'POST':
        action = request.form.get('action')
        flavor_name = request.form.get('flavor_name')
        seasonal = request.form.get('seasonal') == 'on'

        if action == 'Add':
            c.execute("INSERT INTO flavors (name, seasonal) VALUES (?, ?)", (flavor_name, seasonal))
        elif action == 'Remove':
            c.execute("DELETE FROM flavors WHERE name = ?", (flavor_name,))
        conn.commit()

    c.execute("SELECT * FROM flavors")
    flavors = c.fetchall()
    conn.close()

    return render_template('owner_inventory.html', flavors=flavors)

@app.route('/cart')
def view_cart():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Fetch cart items with flavor names and quantities
    query = '''
        SELECT
            cart.id AS cart_id,
            flavors.name AS flavor_name,
            cart.quantity
        FROM
            cart
        JOIN
            flavors ON cart.flavor_id = flavors.id
    '''
    c.execute(query)
    cart_items = c.fetchall()
    conn.close()

    # Debugging to ensure cart items are fetched
    print("Cart items:", cart_items)

    return render_template('cart.html', cart_items=cart_items)




@app.route('/add_to_cart/<int:flavor_id>', methods=['POST'])
def add_to_cart(flavor_id):
    quantity = request.form.get('quantity', 0)  # Default to 0 if no quantity provided
    if not quantity.isdigit():
        quantity = 0  # Handle invalid input gracefully

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Check if the flavor is already in the cart
    c.execute("SELECT id FROM cart WHERE flavor_id = ?", (flavor_id,))
    existing_item = c.fetchone()

    if existing_item:
        # Update the existing quantity
        c.execute("UPDATE cart SET quantity = quantity + ? WHERE flavor_id = ?", (int(quantity), flavor_id))
    else:
        # Insert new item into cart
        c.execute("INSERT INTO cart (flavor_id, quantity) VALUES (?, ?)", (flavor_id, quantity))

    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))



@app.route('/update_cart/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    new_quantity = request.form.get('quantity', 0)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    if int(new_quantity) > 0:
        # Update the quantity
        c.execute("UPDATE cart SET quantity = ? WHERE id = ?", (new_quantity, cart_id))
    else:
        # Remove the item if quantity is 0
        c.execute("DELETE FROM cart WHERE id = ?", (cart_id,))

    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


@app.route('/remove_from_cart/<int:cart_id>')
def remove_from_cart(cart_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_cart'))


@app.route('/customer/dashboard')
def customer_dashboard():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Fetch all available flavors
    c.execute("SELECT id, name FROM flavors")
    flavors = c.fetchall()
    conn.close()
    return render_template('customer_dashboard.html', flavors=flavors)


def get_flavors_with_allergens():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    query = '''
        SELECT 
            flavors.id,
            flavors.name AS flavor_name,
            flavors.seasonal,
            GROUP_CONCAT(allergens.name, ', ') AS allergens_list
        FROM 
            flavors
        LEFT JOIN 
            flavor_allergens ON flavors.id = flavor_allergens.flavor_id
        LEFT JOIN 
            allergens ON flavor_allergens.allergen_id = allergens.id
        GROUP BY 
            flavors.id
        ORDER BY 
            flavors.name ASC
    '''
    c.execute(query)
    results = c.fetchall()
    conn.close()

    flavors_data = []
    for row in results:
        flavor_id, flavor_name, seasonal, allergens_list = row
        seasonal_status = "Seasonal" if seasonal == 1 else "Non-Seasonal"
        allergens_text = f"{flavor_name} contains {allergens_list}" if allergens_list else f"{flavor_name} contains no allergens"
        flavors_data.append({
            "Flavor": flavor_name,
            "Status": seasonal_status,
            "Allergens": allergens_text
        })

    return flavors_data


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
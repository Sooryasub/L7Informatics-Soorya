# Ice Cream Parlor Cafe App

This application is a simple Flask-based web app designed for managing customer orders in an ice cream parlor. The system allows users to view available flavors, add them to a cart, and place orders. The app consists of a front-end built with HTML, CSS, and JavaScript, and a back-end powered by Flask and SQLite for database management.

## Front-End

The front-end is composed of HTML templates rendered by Flask. The main components of the front-end are:

- **Customer Dashboard** (`customer_dashboard.html`): Displays a list of available ice cream flavors with an option to add them to the cart.
- **Cart** (`cart.html`): Displays the current cart with selected items and their quantities. Users can update quantities or remove items from the cart.
- **Base Template** (`base.html`): Contains the common structure and styles for the pages, with placeholders for dynamic content.

The front-end uses forms to send data to the back-end (e.g., adding flavors to the cart), and JavaScript is used for dynamically updating parts of the page (e.g., updating quantities).

### Key HTML Components:
- **Add to Cart Button**: When clicked, it adds the selected flavor to the cart. This is achieved using a form that sends a POST request to the backend.
- **Cart Management**: Displays the current cart, including flavor names, quantities, and a button to update or remove items.

## Back-End

The back-end is built using Flask, a Python web framework. It handles requests from the front-end, processes the data, and interacts with the SQLite database to store and retrieve information about flavors, orders, and the cart.

### Routes:
- **Home (`/`)**: Displays the list of available ice cream flavors.
- **Add to Cart (`/add_to_cart/<int:flavor_id>`)**: Adds a flavor to the cart.
- **View Cart (`/cart`)**: Displays the current cart and allows users to manage quantities and remove items.
- **Place Order (`/place_order`)**: Allows users to place an order and clear the cart.

### SQL Query or ORM Abstraction Implementation

The application uses raw SQL queries for interacting with the SQLite database. Here's how the queries are implemented:

1. **Fetching Flavors**:
   ```python
   c.execute("SELECT id, name, price FROM flavors")
   flavors = c.fetchall()
This query retrieves all the flavors from the flavors table, including the id, name, and price of each flavor.

Adding Flavor to Cart: When a flavor is added to the cart, the app checks if the flavor already exists in the cart. If it does, it updates the quantity; otherwise, it adds the new item:

python
Copy code
c.execute("SELECT * FROM cart WHERE flavor_id = ?", (flavor_id,))
existing_item = c.fetchone()
if existing_item:
    c.execute("UPDATE cart SET quantity = quantity + 1 WHERE flavor_id = ?", (flavor_id,))
else:
    c.execute("INSERT INTO cart (flavor_id, quantity) VALUES (?, ?)", (flavor_id, 1))
Placing an Order: The app retrieves the cart items, creates an order entry, and then clears the cart:

python
Copy code
c.execute("SELECT * FROM cart")
cart_items = c.fetchall()
for item in cart_items:
    c.execute("INSERT INTO orders (flavor_id, quantity) VALUES (?, ?)", (item['flavor_id'], item['quantity']))
c.execute("DELETE FROM cart")
Test Steps to Validate the Application
Start the Application:

Run the application using python app.py.
Access the homepage (http://127.0.0.1:5000/) in a web browser.
Add Items to Cart:

On the homepage, click on the "Add to Cart" button for any flavor.
Verify that the flavor appears in the cart page.
View Cart:

Go to the cart page (/cart) and verify that the selected flavors are listed with their quantities.
Update the quantity or remove items from the cart, and ensure that the changes are reflected on the page.
Place Order:

Click on "Place Order" in the cart page.
Verify that the order is placed successfully and the cart is cleared.
Database Verification:

Check the database to ensure that cart entries are added and removed properly.
Verify that the orders table is populated when an order is placed.
Code Documentation
app.py:

Contains the Flask app and defines routes for home, adding flavors to the cart, viewing the cart, and placing an order.
The app handles form submissions, interacts with the SQLite database, and updates the UI dynamically.
customer_dashboard.html:

Renders the list of flavors with options to add them to the cart.
cart.html:

Displays the current cart with flavor names, quantities, and the option to modify or remove items.
base.html:

A common base template for layout and structure, used across all pages.
Docker Setup
To run the application using Docker, follow these steps:

Create a Dockerfile:

In the root directory of your project, create a Dockerfile with the following contents:

Dockerfile
Copy code
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
Create a .dockerignore file:

To prevent unnecessary files from being copied to the Docker image, create a .dockerignore file:

markdown
Copy code
__pycache__
*.pyc
*.pyo
venv/
Build and Run the Docker Container:

From your project directory, run the following commands to build and run the Docker container:

bash
Copy code
# Build the Docker image
docker build -t ice-cream-app .

# Run the Docker container
docker run -p 5000:5000 ice-cream-app
Access the Application:

Open a browser and visit http://localhost:5000 to see the app running inside the Docker container.

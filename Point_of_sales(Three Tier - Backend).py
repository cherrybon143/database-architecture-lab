import sqlite3
import tkinter as tk
from tkinter import messagebox

# Create database and tables
def create_database():
    conn = sqlite3.connect("pos.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        total_price REAL NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products(id)
    )
    """)

    conn.commit()
    conn.close()

# Function to add a product
def add_product():
    name = entry_name.get()
    price = entry_price.get()
    stock = entry_stock.get()

    if name and price and stock:
        try:
            price = float(price)
            stock = int(stock)

            conn = sqlite3.connect("pos.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Product added successfully!")
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value!")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Function to process a sale
def process_sale():
    product_id = entry_product_id.get()
    quantity = entry_quantity.get()

    if product_id and quantity:
        try:
            product_id = int(product_id)
            quantity = int(quantity)

            conn = sqlite3.connect("pos.db")
            cursor = conn.cursor()

            cursor.execute("SELECT price, stock FROM products WHERE id=?", (product_id,))
            result = cursor.fetchone()

            if result:
                price, stock = result
                if stock >= quantity:
                    total_price = price * quantity
                    cursor.execute("INSERT INTO sales (product_id, quantity, total_price) VALUES (?, ?, ?)",
                                   (product_id, quantity, total_price))
                    cursor.execute("UPDATE products SET stock = stock - ? WHERE id=?", (quantity, product_id))
                    conn.commit()
                    messagebox.showinfo("Success", f"Sale processed. Total: ${total_price:.2f}")
                else:
                    messagebox.showerror("Error", "Not enough stock!")
            else:
                messagebox.showerror("Error", "Invalid Product ID!")

            conn.close()
        except ValueError:
            messagebox.showerror("Error", "Invalid input values!")
    else:
        messagebox.showerror("Error", "All fields are required!")

# Initialize database
create_database()

# Create GUI
root = tk.Tk()
root.title("POS System")

tk.Label(root, text="Product Name").grid(row=0, column=0)
tk.Label(root, text="Price").grid(row=1, column=0)
tk.Label(root, text="Stock").grid(row=2, column=0)

entry_name = tk.Entry(root)
entry_price = tk.Entry(root)
entry_stock = tk.Entry(root)

entry_name.grid(row=0, column=1)
entry_price.grid(row=1, column=1)
entry_stock.grid(row=2, column=1)

tk.Button(root, text="Add Product", command=add_product).grid(row=3, column=0, columnspan=2)

tk.Label(root, text="Product ID").grid(row=4, column=0)
tk.Label(root, text="Quantity").grid(row=5, column=0)

entry_product_id = tk.Entry(root)
entry_quantity = tk.Entry(root)

entry_product_id.grid(row=4, column=1)
entry_quantity.grid(row=5, column=1)

tk.Button(root, text="Process Sale", command=process_sale).grid(row=6, column=0, columnspan=2)

root.mainloop()

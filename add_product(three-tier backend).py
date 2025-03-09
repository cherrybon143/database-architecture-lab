import tkinter as tk
from tkinter import messagebox
import requests

API_URL = "http://127.0.0.1:5000"

def add_product():
    name = entry_name.get()
    price = entry_price.get()
    stock = entry_stock.get()

    if name and price and stock:
        try:
            data = {"name": name, "price": float(price), "stock": int(stock)}
            response = requests.post(f"{API_URL}/add_product", json=data)

            if response.status_code == 201:
                messagebox.showinfo("Success", f"Product '{name}' added successfully!")
                entry_name.delete(0, tk.END)
                entry_price.delete(0, tk.END)
                entry_stock.delete(0, tk.END)
                view_products()
            else:
                messagebox.showerror("Error", "Failed to add product!")
        except ValueError:
            messagebox.showerror("Error", "Invalid price or stock value!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def view_products():
    response = requests.get(f"{API_URL}/products")
    if response.status_code == 200:
        products = response.json()
        product_list.delete(0, tk.END)
        for product in products:
            product_list.insert(tk.END, f"{product['id']}. {product['name']} - ${product['price']} ({product['stock']} in stock)")
    else:
        messagebox.showerror("Error", "Failed to load products!")

def delete_product():
    selected = product_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select a product to delete!")
        return

    product_info = product_list.get(selected[0])
    product_id = product_info.split(".")[0]  

    response = requests.delete(f"{API_URL}/delete_product/{product_id}")
    
    if response.status_code == 200:
        messagebox.showinfo("Success", "Product deleted successfully!")
        view_products()
    else:
        messagebox.showerror("Error", f"Failed to delete product! {response.json().get('error')}")

root = tk.Tk()
root.title("Point of Sale System")

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

tk.Label(root, text="Product List").grid(row=4, column=0, columnspan=2)

product_list = tk.Listbox(root, width=50, height=10)
product_list.grid(row=5, column=0, columnspan=2)

tk.Button(root, text="View Products", command=view_products).grid(row=6, column=0, columnspan=2)
tk.Button(root, text="Delete Product", command=delete_product).grid(row=7, column=0, columnspan=2)

view_products()

root.mainloop()

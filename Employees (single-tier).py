import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database Setup
conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    position TEXT NOT NULL,
    salary REAL NOT NULL
)
""")
conn.commit()

# Functions
def add_employee():
    name = entry_name.get().strip()
    position = entry_position.get().strip()
    salary = entry_salary.get().strip()

    if name and position and salary:
        try:
            cursor.execute("INSERT INTO employees (name, position, salary) VALUES (?, ?, ?)",
                           (name, position, float(salary)))
            conn.commit()
            messagebox.showinfo("Success", "Employee added successfully!")
            clear_fields()
            view_employees()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Employee with this name already exists!")
        except ValueError:
            messagebox.showerror("Error", "Invalid salary value!")
    else:
        messagebox.showerror("Error", "All fields are required!")

def view_employees():
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    employee_list.delete(0, tk.END)
    for emp in employees:
        employee_list.insert(tk.END, f"{emp[0]}. {emp[1]} - {emp[2]} (${emp[3]})")

def delete_employee():
    selected = employee_list.curselection()
    if not selected:
        messagebox.showerror("Error", "Please select an employee to delete!")
        return

    emp_info = employee_list.get(selected[0])
    emp_id = emp_info.split(".")[0]  

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Employee ID {emp_id}?")
    if confirm:
        cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
        conn.commit()
        messagebox.showinfo("Success", "Employee deleted successfully!")
        view_employees()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_position.delete(0, tk.END)
    entry_salary.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Employee Management System")

tk.Label(root, text="Name").grid(row=0, column=0)
tk.Label(root, text="Position").grid(row=1, column=0)
tk.Label(root, text="Salary").grid(row=2, column=0)

entry_name = tk.Entry(root)
entry_position = tk.Entry(root)
entry_salary = tk.Entry(root)

entry_name.grid(row=0, column=1)
entry_position.grid(row=1, column=1)
entry_salary.grid(row=2, column=1)

tk.Button(root, text="Add Employee", command=add_employee).grid(row=3, column=0, columnspan=2)

tk.Label(root, text="Employee List").grid(row=4, column=0, columnspan=2)

employee_list = tk.Listbox(root, width=50, height=10)
employee_list.grid(row=5, column=0, columnspan=2)

tk.Button(root, text="View Employees", command=view_employees).grid(row=6, column=0, columnspan=2)
tk.Button(root, text="Delete Employee", command=delete_employee).grid(row=7, column=0, columnspan=2)

view_employees()

root.mainloop()

conn.close()

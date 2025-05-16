import tkinter as tk
from tkinter import simpledialog, messagebox
import csv
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import os

DATA_FILE = 'data.csv'

def ensure_file_exists():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])

def add_transaction():
    trans_type = simpledialog.askstring("Transaction Type", "Enter transaction type (income/expense):")
    if not trans_type or trans_type.lower() not in ['income', 'expense']:
        messagebox.showerror("Error", "Invalid transaction type!")
        return

    category = simpledialog.askstring("Category", "Enter category (e.g., food, salary):")
    if not category:
        messagebox.showerror("Error", "Category cannot be empty!")
        return

    try:
        amount_str = simpledialog.askstring("Amount", "Enter amount:")
        amount = float(amount_str)
    except (TypeError, ValueError):
        messagebox.showerror("Error", "Invalid amount!")
        return

    description = simpledialog.askstring("Description", "Enter description:")
    if description is None:  # Allow empty description, but not cancel
        description = ""

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, trans_type.lower(), category, amount, description])

    messagebox.showinfo("Success", "Transaction added successfully!")

def show_expense_chart():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Type'] = df['Type'].str.strip().str.lower()
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

        expense_data = df[df['Type'] == 'expense']

        if expense_data.empty:
            messagebox.showinfo("No Data", "No expense data to show in chart.")
            return

        summary = expense_data.groupby('Category')['Amount'].sum()
        summary.plot.pie(autopct='%1.1f%%', startangle=140, figsize=(6, 6))
        plt.title('Expense Distribution by Category')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"Error showing expense chart: {e}")

def main():
    ensure_file_exists()

    root = tk.Tk()
    root.title("Smart Expense Tracker")
    root.geometry("300x200")

    btn_add = tk.Button(root, text="Add Transaction", command=add_transaction)
    btn_add.pack(pady=10)

    btn_chart = tk.Button(root, text="Show Expense Chart", command=show_expense_chart)
    btn_chart.pack(pady=10)

    btn_exit = tk.Button(root, text="Exit", command=root.destroy)
    btn_exit.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

DATA_FILE = 'data.csv'

# Ensure the data file exists
def ensure_file_exists():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Type', 'Category', 'Amount', 'Description'])

# Add a new transaction
def add_transaction():
    trans_type = input("Enter transaction type (income/expense): ").strip().lower()
    if trans_type not in ['income', 'expense']:
        print("Invalid type!")
        return

    category = input("Enter category (e.g., food, salary, transport): ").strip()
    amount = float(input("Enter amount: "))
    description = input("Enter description: ").strip()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(DATA_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, trans_type, category, amount, description])

    print("✅ Transaction added successfully!")

# View all transactions
def view_transactions():
    print("\n📄 All Transactions:")
    try:
        df = pd.read_csv(DATA_FILE)
        print(df.to_string(index=False))
    except Exception as e:
        print("⚠️ Error reading file:", e)

# Show income, expense, and balance
def show_balance():
    df = pd.read_csv(DATA_FILE)
    df['Type'] = df['Type'].astype(str).str.strip().str.lower()
    income = df[df['Type'] == 'income']['Amount'].sum()
    expense = df[df['Type'] == 'expense']['Amount'].sum()
    balance = income - expense
    print(f"\n💰 Total Income: Rs.{income}")
    print(f"💸 Total Expense: Rs.{expense}")
    print(f"🧾 Current Balance: Rs.{balance}")

# Show a pie chart of expenses by category
def show_expense_chart():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Type'] = df['Type'].astype(str).str.strip().str.lower()
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')

        expense_data = df[df['Type'] == 'expense']

        if expense_data.empty:
            print("\n❌ No expense data to show in chart.")
            return

        summary = expense_data.groupby('Category')['Amount'].sum()
        summary.plot.pie(autopct='%1.1f%%', startangle=140, figsize=(6, 6))
        plt.title('📊 Expense Distribution by Category')
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print("⚠️ Error showing expense chart:", e)

# Export full report
def export_report():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Type'] = df['Type'].astype(str).str.strip().str.lower()

        income = df[df['Type'] == 'income']['Amount'].sum()
        expense = df[df['Type'] == 'expense']['Amount'].sum()
        balance = income - expense

        report = f"Smart Expense Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += "-"*50 + "\n"
        report += f"Total Income: ₹{income}\n"
        report += f"Total Expense: ₹{expense}\n"
        report += f"Balance: ₹{balance}\n"
        report += "-"*50 + "\n"
        report += "Transactions:\n"
        report += df.to_string(index=False)

        # Fix encoding issue for Windows
        report = report.replace("₹", "Rs.")

        filename = f"expense_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Report exported successfully as '{filename}'")

    except Exception as e:
        print("⚠️ Error exporting report:", e)

# Export report for a specific month
def export_monthly_report():
    try:
        df = pd.read_csv(DATA_FILE)
        df['Type'] = df['Type'].astype(str).str.strip().str.lower()
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        month_input = input("Enter month and year (YYYY-MM): ")
        df = df[df['Date'].dt.strftime('%Y-%m') == month_input]

        if df.empty:
            print("❌ No transactions found for that month.")
            return

        income = df[df['Type'] == 'income']['Amount'].sum()
        expense = df[df['Type'] == 'expense']['Amount'].sum()
        balance = income - expense

        report = f"Monthly Expense Report - {month_input}\n"
        report += "-"*50 + "\n"
        report += f"Total Income: Rs.{income}\n"
        report += f"Total Expense: Rs.{expense}\n"
        report += f"Balance: Rs.{balance}\n"
        report += "-"*50 + "\n"
        report += "Transactions:\n"
        report += df.to_string(index=False)

        filename = f"monthly_report_{month_input.replace('-', '')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"✅ Monthly report exported as '{filename}'")

    except Exception as e:
        print("⚠️ Error exporting monthly report:", e)

# Main menu
def main_menu():
    ensure_file_exists()

    while True:
        print("\n📘 Smart Expense Tracker")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Show Balance")
        print("4. Show Expense Chart")
        print("5. Export Report to Text File")
        print("6. Export Monthly Report")
        print("7. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            show_balance()
        elif choice == '4':
            show_expense_chart()
        elif choice == '5':
            export_report()
        elif choice == '6':
            export_monthly_report()
        elif choice == '7':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.")

# ✅ Run the program
if __name__ == "__main__":
    main_menu()

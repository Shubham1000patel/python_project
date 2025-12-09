import tkinter as tk
from tkinter import ttk, messagebox
from database import (
    connect_db,
    create_user,
    login_user,
    add_income,
    add_expense,
    get_all_income,
    get_all_expenses
)

# -----------------------------------
# LOGIN WINDOW
# -----------------------------------
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager - Login")
        self.root.geometry("400x300")

        tk.Label(root, text="Username").pack(pady=5)
        self.username = tk.Entry(root)
        self.username.pack(pady=5)

        tk.Label(root, text="Password").pack(pady=5)
        self.password = tk.Entry(root, show="*")
        self.password.pack(pady=5)

        tk.Button(root, text="Login", command=self.login).pack(pady=10)
        tk.Button(root, text="Sign Up", command=self.signup).pack(pady=5)

        self.conn = connect_db()

    def login(self):
        user = login_user(self.conn, self.username.get(), self.password.get())
        if user:
            messagebox.showinfo("Success", "Login Successful!")
            self.root.destroy()
            open_dashboard(self.conn)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def signup(self):
        if create_user(self.conn, self.username.get(), self.password.get()):
            messagebox.showinfo("Success", "User created, now login")
        else:
            messagebox.showerror("Error", "Username already exists")


# -----------------------------------
# DASHBOARD WINDOW
# -----------------------------------
def open_dashboard(conn):
    dashboard = tk.Tk()
    dashboard.title("Finance Manager")
    dashboard.geometry("700x600")

    tabControl = ttk.Notebook(dashboard)

    tab_income = ttk.Frame(tabControl)
    tab_expense = ttk.Frame(tabControl)
    tab_view_income = ttk.Frame(tabControl)
    tab_view_expense = ttk.Frame(tabControl)

    tabControl.add(tab_income, text="Add Income")
    tabControl.add(tab_expense, text="Add Expense")
    tabControl.add(tab_view_income, text="View Income")
    tabControl.add(tab_view_expense, text="View Expenses")

    tabControl.pack(expand=1, fill="both")

    # ---------------------------
    # ADD INCOME TAB
    # ---------------------------
    tk.Label(tab_income, text="Amount").pack()
    income_amount = tk.Entry(tab_income)
    income_amount.pack()

    tk.Label(tab_income, text="Date (YYYY-MM-DD)").pack()
    income_date = tk.Entry(tab_income)
    income_date.pack()

    tk.Label(tab_income, text="Source").pack()
    income_source = tk.Entry(tab_income)
    income_source.pack()

    def save_income():
        amount = float(income_amount.get())
        date = income_date.get()
        source = income_source.get()
        if add_income(conn, amount, date, source):
            messagebox.showinfo("Success", "Income added!")

    tk.Button(tab_income, text="Save Income", command=save_income).pack(pady=10)

    # ---------------------------
    # ADD EXPENSE TAB
    # ---------------------------
    tk.Label(tab_expense, text="Amount").pack()
    expense_amount = tk.Entry(tab_expense)
    expense_amount.pack()

    tk.Label(tab_expense, text="Date (YYYY-MM-DD)").pack()
    expense_date = tk.Entry(tab_expense)
    expense_date.pack()

    tk.Label(tab_expense, text="Category").pack()
    expense_category = tk.Entry(tab_expense)
    expense_category.pack()

    tk.Label(tab_expense, text="Description").pack()
    expense_desc = tk.Entry(tab_expense)
    expense_desc.pack()

    def save_expense():
        amount = float(expense_amount.get())
        date = expense_date.get()
        category = expense_category.get()
        desc = expense_desc.get()
        if add_expense(conn, amount, date, category, desc):
            messagebox.showinfo("Success", "Expense added!")

    tk.Button(tab_expense, text="Save Expense", command=save_expense).pack(pady=10)

    # ---------------------------
    # VIEW INCOME TAB
    # ---------------------------
    income_tree = ttk.Treeview(tab_view_income, columns=("Amount", "Date", "Source"), show="headings")
    income_tree.heading("Amount", text="Amount")
    income_tree.heading("Date", text="Date")
    income_tree.heading("Source", text="Source")
    income_tree.pack(fill="both", expand=True)

    for row in get_all_income(conn):
        income_tree.insert("", tk.END, values=row[1:])

    # ---------------------------
    # VIEW EXPENSE TAB
    # ---------------------------
    expense_tree = ttk.Treeview(tab_view_expense, columns=("Amount", "Date", "Category", "Description"), show="headings")
    expense_tree.heading("Amount", text="Amount")
    expense_tree.heading("Date", text="Date")
    expense_tree.heading("Category", text="Category")
    expense_tree.heading("Description", text="Description")
    expense_tree.pack(fill="both", expand=True)

    for row in get_all_expenses(conn):
        expense_tree.insert("", tk.END, values=row[1:])

    dashboard.mainloop()


# -----------------------------------
# START APP
# -----------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

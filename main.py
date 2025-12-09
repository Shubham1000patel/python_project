
from database import (
    connect_db,
    create_tables,
    create_user,
    export_expenses_to_csv,
    export_income_to_csv,
    get_monthly_expense_report,
    get_monthly_income_report,
    get_yearly_expense_report,
    get_yearly_income_report,
    login_user,
    add_income,
    add_expense,
    get_all_income,
    get_all_expenses,
    
)

def login_system(conn):
    print("\n=====================")
    print("   LOGIN SYSTEM")
    print("=====================")

    while True:
        print("\n1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Choose option: ")

        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")

            user = login_user(conn, username, password)
            if user:
                print("✅ Login successful!")
                return True
            else:
                print("❌ Invalid username or password.")

        elif choice == "2":
            username = input("Create username: ")
            password = input("Create password: ")

            if create_user(conn, username, password):
                print("✅ User created successfully! You can now login.")
            else:
                print("❌ Username already exists. Try another.")

        elif choice == "3":
            print("Exiting...")
            exit()

        else:
            print("Invalid choice. Try again.")

# ---------------------------
# MAIN MENU FUNCTION
# ---------------------------
def show_menu():
    print("\n==============================")
    print("   PERSONAL FINANCE MANAGER   ")
    print("==============================")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. View All Income")
    print("4. View All Expenses")
    print("5. Monthly Report")
    print("6. Yearly Report")
    print("7. Export Income Data to CSV")
    print("8. Export Expense Data to CSV")
    print("9. Exit")
    print("==============================")

# ---------------------------
# ADD INCOME FLOW
# ---------------------------
def handle_add_income(conn):
    try:
        amount = float(input("Enter income amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        source = input("Enter income source: ")

        if add_income(conn, amount, date, source):
            print("✅ Income added successfully!")
        else:
            print("❌ Failed to add income.")

    except ValueError:
        print("❌ ERROR: Please enter a valid number for amount.")

# ---------------------------
# ADD EXPENSE FLOW
# ---------------------------
def handle_add_expense(conn):
    try:
        amount = float(input("Enter expense amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        category = input("Enter category (Food, Travel, Bills, etc.): ")
        description = input("Enter description (optional): ")

        if add_expense(conn, amount, date, category, description):
            print("✅ Expense added successfully!")
        else:
            print("❌ Failed to add expense.")

    except ValueError:
        print("❌ ERROR: Please enter a valid number for amount.")

# ---------------------------
# VIEW ALL INCOME
# ---------------------------
def handle_view_income(conn):
    records = get_all_income(conn)

    print("\n===== ALL INCOME RECORDS =====")
    if not records:
        print("No income records found.")
    else:
        for row in records:
            print(f"ID: {row[0]}, Amount: {row[1]}, Date: {row[2]}, Source: {row[3]}")
    print("==============================")

# ---------------------------
# VIEW ALL EXPENSES
# ---------------------------
def handle_view_expenses(conn):
    records = get_all_expenses(conn)

    print("\n===== ALL EXPENSE RECORDS =====")
    if not records:
        print("No expense records found.")
    else:
        for row in records:
            print(f"ID: {row[0]}, Amount: {row[1]}, Date: {row[2]}, Category: {row[3]}, Description: {row[4]}")
    print("==============================")
def show_monthly_report(conn):
    year = input("Enter the year for the monthly report (e.g., 2024): ")
    income_report = get_monthly_income_report(conn, year)
    expense_report = get_monthly_expense_report(conn, year)
    
    print(f"\nMonthly Income Report for {year}:")
    for month, total in income_report:
        print(f"Month: {month}, Total Income: ${total}")

    print(f"\nMonthly Expense Report for {year}:")
    for month, total in expense_report:
        print(f"Month: {month}, Total Expense: ${total}")

def show_yearly_report(conn):
    income_report = get_yearly_income_report(conn)
    expense_report = get_yearly_expense_report(conn)
    
    print("\nYearly Income Report:")
    for year, total in income_report:
        print(f"Year: {year}, Total Income: ${total}")

    print("\nYearly Expense Report:")
    for year, total in expense_report:
        print(f"Year: {year}, Total Expense: ${total}")

# ---------------------------
# MAIN APP LOOP
# ---------------------------
def main():
    print("📌 Initializing Personal Finance Manager...")

    conn = connect_db()
    create_tables(conn)

    print("✅ Database connected and tables ready!")
    
    
    if not login_system(conn):
        return


    while True:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            handle_add_income(conn)

        elif choice == "2":
            handle_add_expense(conn)

        elif choice == "3":
            handle_view_income(conn)

        elif choice == "4":
            handle_view_expenses(conn)
            
            
        elif choice == "5":
            show_monthly_report(conn)
            
            
        elif choice == "6":
            show_yearly_report(conn)
            
            
            
        elif choice == "7":
             file_path = input("Enter the file path for the income export (e.g., income_report.csv): ")
             export_income_to_csv(conn, file_path)
             
        elif choice == "8":
             file_path = input("Enter the file path for the expense export (e.g., expense_report.csv): ")
             export_expenses_to_csv(conn, file_path)

        elif choice == "9":
            print("👋 Exiting... Thank you for using Finance Manager!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

    conn.close()

# ---------------------------
# START PROGRAM
# ---------------------------
if __name__ == "__main__":
    main()

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

class ExpenseTracker:
    """
    A simple console-based expense tracker using pandas for data management
    and matplotlib for visualization.
    """
    def __init__(self, filename='expenses.csv'):
        """
        Initializes the ExpenseTracker. Loads existing data if the file exists,
        otherwise initializes an empty DataFrame.
        """
        self.filename = filename
        self.columns = ['Date', 'Category', 'Description', 'Amount']
        
        # Check if the file exists and load data
        if os.path.exists(self.filename):
            try:
                self.expenses = pd.read_csv(self.filename, parse_dates=['Date'])
                print(f"Loaded {len(self.expenses)} existing expense records.")
            except pd.errors.EmptyDataError:
                print("CSV file is empty. Starting with a new ledger.")
                self.expenses = pd.DataFrame(columns=self.columns)
            except Exception as e:
                print(f"Error loading CSV: {e}. Starting with a new ledger.")
                self.expenses = pd.DataFrame(columns=self.columns)
        else:
            print("No existing expense file found. Starting a new ledger.")
            self.expenses = pd.DataFrame(columns=self.columns)
        
        # Ensure 'Amount' is numeric
        self.expenses['Amount'] = pd.to_numeric(self.expenses['Amount'], errors='coerce')


    def add_expense(self, category: str, description: str, amount: float):
        """
        Adds a new expense entry to the DataFrame.
        """
        try:
            # Validate input
            amount = float(amount)
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            # Create a new record
            new_expense = pd.DataFrame([{
                'Date': datetime.now().date(),
                'Category': category.strip().capitalize(),
                'Description': description.strip(),
                'Amount': amount
            }])
            
            # Append the new expense
            self.expenses = pd.concat([self.expenses, new_expense], ignore_index=True)
            print(f"\n✅ Added expense: {category} - {description} (${amount:.2f})")
            
        except ValueError:
            print("\n❌ Invalid amount entered. Please enter a valid number.")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred while adding expense: {e}")


    def summarize_by_category(self):
        """
        Calculates and displays the total expense grouped by category.
        """
        if self.expenses.empty:
            print("\n💡 No expenses recorded yet to summarize.")
            return None

        # Group by Category and sum the Amount
        category_summary = self.expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False).reset_index()
        category_summary['Amount'] = category_summary['Amount'].map('${:,.2f}'.format)
        
        total = self.expenses['Amount'].sum()
        
        print("\n=== Category Summary ===")
        print(category_summary.to_string(index=False))
        print("-" * 30)
        print(f"TOTAL SPENT: ${total:,.2f}")
        print("========================")
        return category_summary


    def view_all_expenses(self):
        """
        Displays the entire list of recorded expenses.
        """
        if self.expenses.empty:
            print("\n💡 No expenses recorded yet.")
            return

        print("\n=== All Recorded Expenses ===")
        # Format the DataFrame for better display
        df_display = self.expenses.copy()
        df_display['Amount'] = df_display['Amount'].map('${:,.2f}'.format)
        
        print(df_display.to_string(index=True))


    def save_expenses(self):
        """
        Saves the current expense DataFrame back to the CSV file.
        """
        try:
            # Ensure 'Date' is correctly formatted before saving
            self.expenses['Date'] = pd.to_datetime(self.expenses['Date']).dt.date
            self.expenses.to_csv(self.filename, index=False)
            print(f"\n💾 All expense data saved successfully to {self.filename}.")
        except Exception as e:
            print(f"\n❌ Failed to save data: {e}")


    def visualize_expenses(self):
        """
        Generates a simple bar chart of total spending by category.
        """
        if self.expenses.empty:
            print("\n💡 Cannot visualize. No expenses recorded yet.")
            return

        # Use the raw summary data for plotting
        summary = self.expenses.groupby('Category')['Amount'].sum().sort_values(ascending=False)
        
        if summary.empty:
            print("\n💡 Cannot visualize. Summary calculation failed.")
            return

        plt.figure(figsize=(10, 6))
        summary.plot(kind='bar', color='teal')
        plt.title('Total Spending by Category')
        plt.xlabel('Category')
        plt.ylabel('Amount Spent ($)')
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        print("\n📊 Displaying bar chart visualization. Close the window to continue.")
        plt.show()


def main():
    """
    The main function to run the command-line interface.
    """
    tracker = ExpenseTracker()

    while True:
        print("\n" + "="*40)
        print("  PYTHON EXPENSE TRACKER")
        print("="*40)
        print("1. Add a new expense")
        print("2. View all expenses")
        print("3. Summarize by category")
        print("4. Visualize expenses (Bar Chart)")
        print("5. Save and Exit")
        print("6. Exit without Saving (DANGER)")
        print("-" * 40)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            print("\n--- Add New Expense ---")
            category = input("Enter Category (e.g., Food, Transport, Rent): ")
            description = input("Enter Description: ")
            amount = input("Enter Amount ($): ")
            tracker.add_expense(category, description, amount)
            
        elif choice == '2':
            tracker.view_all_expenses()

        elif choice == '3':
            tracker.summarize_by_category()
            
        elif choice == '4':
            tracker.visualize_expenses()

        elif choice == '5':
            tracker.save_expenses()
            print("\nExiting application. Goodbye!")
            break
            
        elif choice == '6':
            print("\n⚠️ Exiting without saving. Changes will be lost.")
            break

        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1 and 6.")


if __name__ == '__main__':
    # Add a note about the dependency installation
    print("NOTE: This program requires 'pandas' and 'matplotlib'.")
    print("Install them using: pip install pandas matplotlib")
    main()

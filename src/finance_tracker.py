import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from datetime import datetime


class FinanceTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")
        
        # Data file paths
        self.data_folder = "data"
        os.makedirs(self.data_folder, exist_ok=True)
        self.data_file = os.path.join(self.data_folder, "finance_data.csv")
        
        
        #Initialize data
        self.df = self.load_data()
        
        # Create main interface
        self.create_widgets()
        self.update_total_display()
        self.update_transaction_list()
        self.update_chart()
        
    def load_data(self):
        """Load financial data from CSV file or create new DataFrame"""
        if os.path.exists(self.data_file):
            try:
                df = pd.read_csv(self.data_file)
                df['date'] = pd.to_datetime(df['date'])
                return df
            except Exception as e:
                messagebox.showerror("Error", f"Error loading data: {str(e)}")
                
        # Create new DataFrame if file doesn't exist
        return pd.DataFrame(columns=['date', 'description', 'category', 'amount', 'type'])
    
    def save_data(self):
        """Save data to CSV file"""
        try:
            self.df.to_csv(self.data_file, index=False)
        except Exception as e:
            messagebox.showerror("Error", f"Error saving data: {str(e)}")
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Main title
        title_label = tk.Label(self.root, text="Personal Finance Tracker", 
                              font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#2c3e50")
        title_label.pack(pady=10)
        
        # Main container
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel for input and totals
        left_panel = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10), pady=5)
        
        # Current balance display
        self.create_balance_display(left_panel)
        
        # Transaction input form
        self.create_input_form(left_panel)
        
        # Right panel for data display and chart
        right_panel = tk.Frame(main_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, pady=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(right_panel)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Transaction list tab
        self.create_transaction_tab(notebook)
        
        # Charts tab
        self.create_chart_tab(notebook)
    
    def create_balance_display(self, parent):
        """Create the current balance display section"""
        balance_frame = tk.LabelFrame(parent, text="Current Balance", font=("Arial", 12, "bold"),
                                     bg="#ffffff", fg="#2c3e50", padx=10, pady=10)
        balance_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.total_label = tk.Label(balance_frame, text="$0.00", font=("Arial", 24, "bold"),
                                   bg="#ffffff", fg="#27ae60")
        self.total_label.pack()
        
        # Income and expense summary
        summary_frame = tk.Frame(balance_frame, bg="#ffffff")
        summary_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.income_label = tk.Label(summary_frame, text="Income: $0.00", 
                                    font=("Arial", 10), bg="#ffffff", fg="#27ae60")
        self.income_label.pack(side=tk.LEFT)
        
        self.expense_label = tk.Label(summary_frame, text="Expenses: $0.00", 
                                     font=("Arial", 10), bg="#ffffff", fg="#e74c3c")
        self.expense_label.pack(side=tk.RIGHT)
    
    def create_input_form(self, parent):
        """Create the transaction input form"""
        input_frame = tk.LabelFrame(parent, text="Add Transaction", font=("Arial", 12, "bold"),
                                   bg="#ffffff", fg="#2c3e50", padx=10, pady=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Description
        tk.Label(input_frame, text="Description:", bg="#ffffff").pack(anchor=tk.W)
        self.desc_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.desc_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Category
        tk.Label(input_frame, text="Category:", bg="#ffffff").pack(anchor=tk.W)
        self.category_var = tk.StringVar()
        category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, 
                                     values=["Food", "Transportation", "Entertainment", "Utilities", 
                                            "Healthcare", "Shopping", "Salary", "Investment", "Other"])
        category_combo.pack(fill=tk.X, pady=(0, 10))
        
        # Amount
        tk.Label(input_frame, text="Amount:", bg="#ffffff").pack(anchor=tk.W)
        self.amount_entry = tk.Entry(input_frame, width=30, font=("Arial", 10))
        self.amount_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Transaction type
        type_frame = tk.Frame(input_frame, bg="#ffffff")
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.transaction_type = tk.StringVar(value="expense")
        tk.Radiobutton(type_frame, text="Income", variable=self.transaction_type, 
                      value="income", bg="#ffffff", fg="#27ae60").pack(side=tk.LEFT)
        tk.Radiobutton(type_frame, text="Expense", variable=self.transaction_type, 
                      value="expense", bg="#ffffff", fg="#e74c3c").pack(side=tk.RIGHT)
        
        # Add button
        add_button = tk.Button(input_frame, text="Add Transaction", command=self.add_transaction,
                              bg="#3498db", fg="white", font=("Arial", 12, "bold"),
                              relief=tk.FLAT, pady=5)
        add_button.pack(fill=tk.X, pady=10)
        
        # Quick actions frame
        actions_frame = tk.Frame(input_frame, bg="#ffffff")
        actions_frame.pack(fill=tk.X, pady=(10, 0))
        
        export_btn = tk.Button(actions_frame, text="Export Data", command=self.export_data,
                              bg="#95a5a6", fg="white", relief=tk.FLAT)
        export_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        clear_btn = tk.Button(actions_frame, text="Clear All", command=self.clear_all_data,
                             bg="#e74c3c", fg="white", relief=tk.FLAT)
        clear_btn.pack(side=tk.RIGHT, padx=(5, 0))
    
    def create_transaction_tab(self, notebook):
        """Create the transaction list tab"""
        transaction_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(transaction_frame, text="Transactions")
        
        # Search and filter frame
        filter_frame = tk.Frame(transaction_frame, bg="#ffffff")
        filter_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(filter_frame, text="Filter by category:", bg="#ffffff").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All", "Food", "Transportation", "Entertainment", 
                                          "Utilities", "Healthcare", "Shopping", "Salary", 
                                          "Investment", "Other"])
        filter_combo.pack(side=tk.LEFT, padx=(10, 20))
        filter_combo.bind('<<ComboboxSelected>>', lambda e: self.update_transaction_list())
        
        refresh_btn = tk.Button(filter_frame, text="Refresh", command=self.update_transaction_list,
                               bg="#3498db", fg="white", relief=tk.FLAT)
        refresh_btn.pack(side=tk.RIGHT)
        
        # Transaction list
        list_frame = tk.Frame(transaction_frame, bg="#ffffff")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Treeview for transaction list
        columns = ("Date", "Description", "Category", "Amount", "Type")
        self.transaction_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configure column headings and widths
        self.transaction_tree.heading("Date", text="Date")
        self.transaction_tree.heading("Description", text="Description")
        self.transaction_tree.heading("Category", text="Category")
        self.transaction_tree.heading("Amount", text="Amount")
        self.transaction_tree.heading("Type", text="Type")
        
        self.transaction_tree.column("Date", width=100)
        self.transaction_tree.column("Description", width=200)
        self.transaction_tree.column("Category", width=120)
        self.transaction_tree.column("Amount", width=100)
        self.transaction_tree.column("Type", width=80)
        
        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.transaction_tree.yview)
        self.transaction_tree.configure(yscrollcommand=scrollbar.set)
        
        self.transaction_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Delete button
        delete_btn = tk.Button(transaction_frame, text="Delete Selected", 
                              command=self.delete_transaction,
                              bg="#e74c3c", fg="white", relief=tk.FLAT)
        delete_btn.pack(pady=10)
    
    def create_chart_tab(self, notebook):
        """Create the charts tab"""
        chart_frame = tk.Frame(notebook, bg="#ffffff")
        notebook.add(chart_frame, text="Charts")
        
        # Chart controls
        control_frame = tk.Frame(chart_frame, bg="#ffffff")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(control_frame, text="Chart Type:", bg="#ffffff").pack(side=tk.LEFT)
        self.chart_type_var = tk.StringVar(value="Monthly Expenses")
        chart_combo = ttk.Combobox(control_frame, textvariable=self.chart_type_var, values=["Monthly Expenses", "Category Breakdown", "Income vs Expenses", "Monthly Income"])
        chart_combo.pack(side=tk.LEFT, padx=(10, 20))
        chart_combo.bind('<<ComboboxSelected>>', lambda e: self.update_chart())
        
        # Chart canvas
        self.figure = Figure(figsize=(10, 6), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.figure, chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def add_transaction(self):
        try:
            description = self.desc_entry.get().strip()
            category = self.category_var.get().strip()
            amount_str = self.amount_entry.get().strip()
            transaction_type = self.transaction_type.get()
            
            if not description or not category or not amount_str:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            amount = float(amount_str)
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
            
            # For expenses, make amount negative
            if transaction_type == "expense":
                amount = -amount
            
            # Add to DataFrame
            new_row = pd.DataFrame({
                'date': [datetime.now()],
                'description': [description],
                'category': [category],
                'amount': [amount],
                'type': [transaction_type]
            })
            
            self.df = pd.concat([self.df, new_row], ignore_index=True)
            self.save_data()
            
            # Clear input fields
            self.desc_entry.delete(0, tk.END)
            self.category_var.set("")
            self.amount_entry.delete(0, tk.END)
            # Update displays
            self.update_total_display()
            self.update_transaction_list()
            self.update_chart()


        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def update_total_display(self):
        """Update the total balance display"""
        if len(self.df) > 0:
            total = self.df['amount'].sum()
            income = self.df[self.df['type'] == 'income']['amount'].sum()
            expenses = abs(self.df[self.df['type'] == 'expense']['amount'].sum())
        else:
            total = income = expenses = 0
        
        # Update labels
        self.total_label.config(text=f"${total:.2f}")
        self.income_label.config(text=f"Income: ${income:.2f}")
        self.expense_label.config(text=f"Expenses: ${expenses:.2f}")
        
        # Change color based on balance
        if total >= 0:
            self.total_label.config(fg="#27ae60")
        else:
            self.total_label.config(fg="#e74c3c")
    
    def update_transaction_list(self):
        """Update the transaction list display"""
        # Clear existing items
        for item in self.transaction_tree.get_children():
            self.transaction_tree.delete(item)
        
        if len(self.df) == 0:
            return
        
        # Filter data if needed
        filtered_df = self.df.copy()
        if self.filter_var.get() != "All":
            filtered_df = filtered_df[filtered_df['category'] == self.filter_var.get()]
        
        # Sort by date (most recent first)
        filtered_df = filtered_df.sort_values('date', ascending=False)
        
        # Add items to tree
        for _, row in filtered_df.iterrows():
            date_str = row['date'].strftime('%Y-%m-%d')
            amount_str = f"${abs(row['amount']):.2f}"
            
            self.transaction_tree.insert("", "end", values=(
                date_str, row['description'], row['category'], amount_str, row['type'].title()
            ))
    
    def update_chart(self):
        """Update the chart display based on selected type"""
        self.figure.clear()

        if len(self.df) == 0:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data to display', ha='center', va='center', transform=ax.transAxes)
            self.canvas.draw()
            return

        chart_type = self.chart_type_var.get()

        if chart_type == "Monthly Expenses":
            self.create_monthly_chart()
        elif chart_type == "Category Breakdown":
            self.create_category_chart()
        elif chart_type == "Income vs Expenses":
            self.create_income_expense_chart()
        elif chart_type == "Monthly Income":
            self.create_monthly_income_chart()  # <-- Add this line

        self.canvas.draw()
    
    def create_monthly_chart(self):
        """Create monthly expenses chart"""
        df_expenses = self.df[self.df['type'] == 'expense'].copy()
        if len(df_expenses) == 0:
            return
        
        df_expenses['month'] = df_expenses['date'].dt.to_period('M')
        monthly_data = df_expenses.groupby('month')['amount'].sum().abs()
        
        ax = self.figure.add_subplot(111)
        monthly_data.plot(kind='bar', ax=ax, color='#e74c3c')
        ax.set_title('Monthly Expenses', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
    
    def create_category_chart(self):
        """Create category breakdown pie chart"""
        df_expenses = self.df[self.df['type'] == 'expense'].copy()
        if len(df_expenses) == 0:
            return
        
        category_data = df_expenses.groupby('category')['amount'].sum().abs()
        
        ax = self.figure.add_subplot(111)
        colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ff99cc', '#c2c2f0', '#ffb3e6']
        wedges, texts, autotexts = ax.pie(category_data.values, labels=category_data.index, 
                                         autopct='%1.1f%%', colors=colors)
        ax.set_title('Expenses by Category', fontsize=14, fontweight='bold')
    
    def create_monthly_income_chart(self):
        df_income = self.df[self.df['type'] == 'income'].copy()
        if len(df_income) == 0:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No income data to display', ha='center', va='center', transform=ax.transAxes)
            return

        df_income['month'] = df_income['date'].dt.to_period('M')
        monthly_data = df_income.groupby('month')['amount'].sum()

        ax = self.figure.add_subplot(111)
        monthly_data.plot(kind='bar', ax=ax, color='#27ae60')
        ax.set_title('Monthly Income', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()

    def create_income_expense_chart(self):
        df_copy = self.df.copy()
        df_copy['month'] = df_copy['date'].dt.to_period('M')
        
        monthly_income = df_copy[df_copy['type'] == 'income'].groupby('month')['amount'].sum()
        monthly_expenses = df_copy[df_copy['type'] == 'expense'].groupby('month')['amount'].sum().abs()
        
        # Align the data
        all_months = sorted(set(monthly_income.index) | set(monthly_expenses.index))
        income_values = [monthly_income.get(month, 0) for month in all_months]
        expense_values = [monthly_expenses.get(month, 0) for month in all_months]
        
        ax = self.figure.add_subplot(111)
        x = range(len(all_months))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], income_values, width, label='Income', color='#27ae60')
        ax.bar([i + width/2 for i in x], expense_values, width, label='Expenses', color='#e74c3c')
        
        ax.set_title('Income vs Expenses by Month', fontsize=14, fontweight='bold')
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount ($)')
        ax.set_xticks(x)
        ax.set_xticklabels([str(month) for month in all_months], rotation=45)
        ax.legend()
        self.figure.tight_layout()
    
    def delete_transaction(self):
        selected_item = self.transaction_tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this transaction?"):
            # Get the selected row data
            item_values = self.transaction_tree.item(selected_item[0])['values']
            
            # Find and remove the transaction from DataFrame
            date_str = item_values[0]
            description = item_values[1]
            category = item_values[2]
            
            # Convert date string back to datetime for comparison
            date_obj = pd.to_datetime(date_str)
            
            # Find matching row and remove it
            mask = ((self.df['date'].dt.date == date_obj.date()) & 
                   (self.df['description'] == description) & 
                   (self.df['category'] == category))
            
            if mask.any():
                self.df = self.df[~mask]
                self.save_data()
                
                # Update displays
                self.update_total_display()
                self.update_transaction_list()
                self.update_chart()
                
                messagebox.showinfo("Success", "Transaction deleted successfully!")
    
    def export_data(self):
        if len(self.df) == 0:
            messagebox.showwarning("Warning", "No data to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save financial data"
        )
        
        if filename:
            try:
                self.df.to_csv(filename, index=False)
                messagebox.showinfo("Success", f"Data exported to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Error exporting data: {str(e)}")
    
    def clear_all_data(self):
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all data? This cannot be undone!"):
            self.df = pd.DataFrame(columns=['date', 'description', 'category', 'amount', 'type'])
            self.save_data()
            
            # Update displays
            self.update_total_display()
            self.update_transaction_list()
            self.update_chart()
            
            messagebox.showinfo("Success", "All data cleared successfully!")

def main():
    root = tk.Tk()
    app = FinanceTracker(root)
    root.mainloop()

if __name__ == "__main__":
    main()
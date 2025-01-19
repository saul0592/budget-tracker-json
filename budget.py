import tkinter as tk
from tkinter import messagebox
import os
import json

EXPENSES_FILE = "expenses.json"


def submit_entry():
    expense_name_value = expense_name.get()
    expense_amount_value = expense_amount.get()

    income_name_value = income_name.get()
    income_amount_value = income_amount.get()
    
    if expense_name_value or expense_amount_value:
        if not expense_name_value:
            messagebox.showerror("Error", "Please enter an expense name")
            return
        try:
            expense_amount_value = float(expense_amount_value)
            if expense_amount_value == 0:
                messagebox.showerror("Error", "Amount cannot be zero")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount for expense")
            return
        
        selected_category = category_values_option.get()
        if not selected_category:
            messagebox.showerror("Error", "Please select a category")
            return
        
        expenses = load_expenses()
        expense = {"name": expense_name_value, "amount": expense_amount_value, "category": selected_category}
        expenses["expenses"].append(expense)
        save_expenses(expenses)
        
        # Clear the input fields
        expense_name.delete(0, tk.END)
        expense_amount.delete(0, tk.END)
        
        # Update the listbox with the new expenses
        update_expenses_list()
        
        # Update the total expenses label
        update_total_label()
    
    if income_name_value or income_amount_value:
        if not income_name_value:
            messagebox.showerror("Error", "Please enter an income name")
            return
        try:
            income_amount_value = float(income_amount_value)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount for income")
            return
        
        incomes = load_incomes()
        income = {"name": income_name_value, "amount_income": income_amount_value}
        incomes.append(income)
        save_incomes(incomes)
        
        # Clear the input fields
        income_name.delete(0, tk.END)
        income_amount.delete(0, tk.END)
        
        # Update the listbox with the new incomes
        update_income_list()

    

def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as file:
            try:
                data = json.load(file)
                # Ensure that the data has the correct structure
                if "expenses" not in data or "incomes" not in data:
                    return {"expenses": [], "incomes": []}
                return data
            except (json.JSONDecodeError, ValueError):
                return {"expenses": [], "incomes": []}
    return {"expenses": [], "incomes": []}

def save_expenses(data):
    with open(EXPENSES_FILE, "w") as file:
        json.dump(data, file)

def load_incomes():
    data = load_expenses()
    return data.get("incomes", [])

def save_incomes(incomes):
    data = load_expenses()
    data["incomes"] = incomes
    save_expenses(data)

def update_expenses_list():
    expenses = load_expenses()["expenses"]
    expense_listbox.delete(0, tk.END)  # Clear existing items
    for expense in expenses:
        expense_listbox.insert(tk.END, f"{expense['name']} - ${expense['amount']} - {expense['category']}")

def update_income_list():
    incomes = load_incomes()
    income_listbox.delete(0, tk.END)
    for income in incomes:
        income_listbox.insert(tk.END, f"{income['name']} - ${income['amount_income']}")

def delete_income_item():
    income_item = income_listbox.curselection()
    expense_item = expense_listbox.curselection()
    if expense_item:
        expense_item = expense_item[0]
        expenses = load_expenses()["expenses"]
        del expenses[expense_item]
        if messagebox.askyesno("Confirm delete", "Are you sure you want to delete this item?"):
            save_expenses({"expenses": expenses, "incomes": load_incomes()})
            update_expenses_list()
            update_total_label()
    if income_item:
        income_item = income_item[0]
        incomes = load_incomes()
        del incomes[income_item]
        if messagebox.askyesno("Confirm delete", "Are you sure you want to delete this item?"):
            save_incomes(incomes)
            update_income_list()
    else:
        show_alert()



def show_alert():
    messagebox.showinfo("Alert", "No item selected")

def sum_expenses():
    expenses = load_expenses()["expenses"]
    total_food = 0
    total_entertainment = 0
    total_clothes = 0
    total_other = 0

    for expense in expenses:
        if expense["category"] == 'food':
            total_food += expense['amount']
        elif expense["category"] == 'entertainment':
            total_entertainment += expense['amount']
        elif expense["category"] == 'clothes':
            total_clothes += expense['amount']
        elif expense["category"] == 'anything else':
            total_other += expense['amount']

    return total_food, total_entertainment, total_clothes, total_other

def update_total_label():
    total_expenses = sum_expenses()
    total_label.config(text=f'Total food: ${total_expenses[0]} Total entertainment: ${total_expenses[1]} Total clothes: ${total_expenses[2]} Total other: ${total_expenses[3]}')

def create_window():
    global category_menu, expense_amount, expense_name, category_values_option, total_label, expense_listbox, income_listbox, income_amount, income_name
    
    window = tk.Tk()
    window.title("Budget Tracker")
    window.geometry("800x600")  

    ## label to get category
    tk.Label(window, text='Name_expense: ' ).grid(row=0, column=0)
    expense_name = tk.Entry(window)
    expense_name.grid(row=0, column=1)
    ##label to get amount
    tk.Label(window, text='Amount_expense: ' ).grid(row=1, column=0)
    expense_amount = tk.Entry(window)
    expense_amount.grid(row=1, column=1)
    ##label to get category
    tk.Label(window, text='Category_expense: ').grid(row=2, column=0)
    ##menu ro select the category
    category_values = ["food", "entertainment", "clothes", "anything else"]
    category_values_option = tk.StringVar(window)
    category_values_option.set(category_values[0])
    category_menu = tk.OptionMenu(window, category_values_option, *category_values).grid(row=2, column=1)

    tk.Label(window, text='Income_name: ' ).grid(row=0, column=3)
    income_name = tk.Entry(window)
    income_name.grid(row=0, column=4)
    tk.Label(window, text='Income_amount: ' ).grid(row=1, column=3)
    income_amount = tk.Entry(window)
    income_amount.grid(row=1, column=4)
    
    
    total_expenses = sum_expenses()
    total_label = tk.Label(window, text=f'Total food: ${total_expenses[0]} Total entertainment: ${total_expenses[1]} Total clothes: ${total_expenses[2]} Total other: ${total_expenses[3]}')
    total_label.grid(row=5, column=0, columnspan=2)
    
    add_button = tk.Button(window, text="Submit", command=submit_entry)
    add_button.grid(row=3, columnspan=2)

    add_button_delete = tk.Button(window, text="Delete", command=delete_income_item)
    add_button_delete.grid(row=3, column=3)
    
    expense_listbox = tk.Listbox(window)
    expense_listbox.grid(row=4, column=0, columnspan=2)
    

    income_listbox = tk.Listbox(window)
    income_listbox.grid(row=6, column=0, columnspan=2)

    window.mainloop()

create_window()
import tkinter as tk
import os
import json

EXPENSES_FILE = "expenses.json"

def get_amount():
    name = expense_name.get()
    amount = float(expense_amount.get())
    category = expense_catergory.get()
    print(name, amount, category)



    expenses = load_expenses()
    

    expense = {"name": name, "amount": amount, "category": category}
    expenses.append(expense)
    
    save_expenses(expenses)
    
    # Clear the input fields
    expense_name.delete(0, tk.END)
    expense_amount.delete(0, tk.END)
    expense_catergory.delete(0, tk.END)

    # Update the listbox with the new expenses
    update_expenses_list()

def update_expenses_list():
    expenses = load_expenses()
    expense_listbox.delete(0, tk.END)  # Clear existing items
    for expense in expenses:
        expense_listbox.insert(tk.END, f"{expense['name']} - ${expense['amount']} - {expense['category']}")


def load_expenses():
    if os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, "r") as file:
            return json.load(file)
    return []


# Guardar en un archivo JSON
def save_expenses(expenses):
    with open(EXPENSES_FILE, "w") as file:
        json.dump(expenses, file, indent=4)

def create_window():
    window = tk.Tk()
    window.title("Budget Tracker")
    window.geometry("400x300")  

    global expense_catergory, expense_amount, expense_name
    ## label to get category
    tk.Label(window, text='Name: ' ).grid(row=0, column=0)
    expense_name = tk.Entry(window)
    expense_name.grid(row=0, column=1)
    ##label to get amount
    tk.Label(window, text='Amount: ' ).grid(row=1, column=0)
    expense_amount = tk.Entry(window)
    expense_amount.grid(row=1, column=1)

    tk.Label(window, text='Category: ' ).grid(row=2, column=0)
    expense_catergory = tk.Entry(window)
    expense_catergory.grid(row=2, column=1)
    

    add_button = tk.Button(window, text="Submit expense", command=get_amount)
    add_button.grid(row=3, columnspan=2)
    global expense_listbox
    expense_listbox = tk.Listbox(window, width=40, height=10)

    expense_listbox = tk.Listbox(window, width=50, height=10)
    expense_listbox.grid(row=4, columnspan=2)

    window.mainloop()
    

if __name__ == "__main__":
    create_window()


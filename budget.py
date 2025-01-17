import tkinter as tk
from tkinter import messagebox
import os
import json

EXPENSES_FILE = "expenses.json"



def get_amount():
    name = expense_name.get()
    try:
        amount = float(expense_amount.get())  # Convert to float, will raise ValueError if invalid
    except ValueError:
        messagebox.showerror("Error","Please enter a valid amount")
        return  # Exit the function if amount is invalid
    
    # Get the selected category
    selected_category = category_values_option.get()
    if not selected_category:  # No category selected
        messagebox.showerror("Error","Please select a category")
        return
    
    print(name, amount, selected_category)

    
    expenses = load_expenses()
    

    expense = {"name": name, "amount": amount, "category": selected_category}
    expenses.append(expense)

    save_expenses(expenses)
    
    # Clear the input fields
    expense_name.delete(0, tk.END)
    expense_amount.delete(0, tk.END)
    

    # Update the listbox with the new expenses
    update_expenses_list()

### LISTBOX

def show_alert():
    messagebox.showinfo("Alert", "No item selected")


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

def delete_expense_item():

    expense_item = expense_listbox.curselection()
    if expense_item:
        expense_item = expense_item[0]
        expenses= load_expenses()
        del expenses[expense_item]
        if message_box_yesno() == True:
            save_expenses(expenses)
            update_expenses_list()
    else:
        show_alert()

def message_box_yesno():
    result =messagebox.askyesnocancel("Confirm delete", "Are you sure you want to delete this item?")
    return result

   


def accion_click(event):
    print(f"Clic en la posición ({event.x}, {event.y})")


def create_window():
    window = tk.Tk()
    window.title("Budget Tracker")
    window.geometry("400x300")  

    global category_menu, expense_amount, expense_name, category_values_option
    ## label to get category
    tk.Label(window, text='Name: ' ).grid(row=0, column=0)
    expense_name = tk.Entry(window)
    expense_name.grid(row=0, column=1)
    ##label to get amount
    tk.Label(window, text='Amount: ' ).grid(row=1, column=0)
    expense_amount = tk.Entry(window)
    expense_amount.grid(row=1, column=1)

    tk.Label(window, text='Category: ').grid(row=2, column=0)


    category_values = ["food", "entertainment", "clothes", "anything else"]
    category_values_option= tk.StringVar(window)
    category_values_option.set(category_values[0])
    category_menu = tk.OptionMenu(window, category_values_option, *category_values).grid(row=2,column=1)

    
    add_button = tk.Button(window, text="Submit expense", command=get_amount)
    add_button.grid(row=3, columnspan=2)

    add_button_delete = tk.Button(window, text="Delete expenses", command=delete_expense_item)
    add_button_delete.grid(row=3, column=3)
    global expense_listbox

    ##CLICK BUTTON
    window.bind("<Button-1>", accion_click)
    

    
    

    expense_listbox = tk.Listbox(window, width=40, height=10)
    
    expense_listbox.grid(row=4, columnspan=2)
    update_expenses_list()

    window.mainloop()
    

if __name__ == "__main__":
    create_window()


import re
from dbmanager import dbmanager


def nav_main()->str:
    print("\n SpendWise-Navigator")
    print("1. Add Expense")
    print("2. Edit Expense")
    print("3. Delete Expense")
    print("4. View Expenses")
    print("5. View Categories")
    print("6. Add Category")
    print("7. Quit")
    
    choice = input("Select an option: ")
    return choice

def add_nav(dbmngr:dbmanager)->None:
    while True:
        date = input("Enter the date (YYYY-MM-DD): ")
        pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if bool(pattern.match(date)):
            break
        else:
            print("Invalid date format. Use YYYY-MM-DD format.")
    while True:
        amount = input("Enter amount: ")
        try:
            amount = float(amount)
        except TypeError:
            print('Amount should be a numerical value')
            continue
        if amount<=0:
            print("Amount should not be less than or equal to zero")
            continue
        else:
            break
    print("Already existing categories : ", dbmngr.categories)
    category = input("Enter category (optional): ")
    if category=='':
        category = None
    else:
        while True:
            if category not in dbmngr.categories:
                print('Given category does not exist currently.')
                create_cat_choice = input(f'Do you wish to create a new category named "{category}" (y/n): ')
                if create_cat_choice in 'Yy':
                    dbmngr.add_category(category)
                    break
                elif create_cat_choice in 'Nn':
                    print("Already existing categories : ", dbmngr.categories)
                    category = input("Enter category (optional): ")
                    continue
                else:
                    print('Invalid choice. Please select a valid choice')
            else:
                break
    dbmngr.add(date, amount, category)
    print("Expense added successfully!")

def mod_nav(dbmngr:dbmanager)->None:
    print(dbmngr.expenses)
    while True:
        index = input("Enter index number of expense to edit")
        try:
            index = int(index)
        except TypeError:
            print('Index is a numerical value. Please enter valid index.')
            continue
        if index not in dbmngr.indexes:
            print("Index out of bound. Enter valid index.")
            continue
        else:
            break
    print("1.Date")
    print("2.Amount")
    print("3.Category")
    choice = input("Which Value do you wish to edit")
    if choice=='1':
        while True:
            new_date = input('Enter new date("YYYY-MM-DD"): ')
            pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
            if bool(pattern.match(new_date)):
                break
            else:
                print("Invalid date format. Use YYYY-MM-DD format.")
        dbmngr.modify(index=index, date=new_date)
    elif choice=='2':
        while True:
            new_amt = input("Enter new amount: ")
            try:
                new_amt = float(new_amt)
            except TypeError:
                print('Amount should be a numerical value')
                continue
            if new_amt<=0:
                print("Amount should not be less than or equal to zero")
                continue
            else:
                break
        dbmngr.modify(index=index, amount=new_amt)
    elif choice=='3':
        while True:
            print("Already existing categories : ", dbmngr.expenses)
            new_cat = input("Enter new category: ")
            if new_cat not in dbmngr.categories:
                print('Given category does not exist currently.')
                create_cat_choice = input(f'Do you wish to create a new category named "{new_cat}" (y/n): ')
                if create_cat_choice in 'Yy':
                    dbmngr.add_category(new_cat)
                    break
                elif create_cat_choice in 'Nn':
                    continue
                else:
                    print('Invalid choice. Please select a valid choice')
            else:
                break
        dbmngr.modify(index=index, category=new_cat)

def rem_nav(dbmngr:dbmanager)->None:
    while True:
        print(dbmngr.expenses)
        index = input("Enter index number of expense to edit")
        try:
            index = int(index)
        except TypeError:
            print('Index is a numerical value. Please enter valid index.')
            continue
        if index not in dbmngr.indexes:
            print("Index out of bound. Enter valid index")
            continue
        else:
            break
    dbmngr.remove(index=index)

def addcat_nav(dbmngr:dbmanager)->None:
    new_category = input("Enter new category: ")
    dbmngr.add_category(new_category)
    print("Category added successfully!")


def main():
    dbm = dbmanager('expenses')

    while True:
        choice = nav_main()

        if choice == '1':
            add_nav(dbm)

        elif choice == '2':
            mod_nav(dbm)

        elif choice == '3':
            rem_nav(dbm)

        elif choice == '4':
            print(dbm.expenses)

        elif choice == '5':
            print(dbm.categories)

        elif choice == '6':
            addcat_nav(dbm)

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()

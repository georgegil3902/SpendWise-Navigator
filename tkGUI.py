import tkinter as tk
from tkinter import ttk
import dbmanager as db


class SpendWiseApp:
    def __init__(self, dbmanager:db.dbmanager=None):
        """GUI Class object for SpendWise-Navigator App

        Args:
            dbmanager (db.dbmanager): dbmanager instance is mandatory to for its functioning.
        """
        self._db = dbmanager    # Instance of dbmanager for data control

        self._root = tk.Tk()    # Tkinter main window
        self._root.title("SpendWise-Navigator")

        # Title Label
        self._title_label = ttk.Label(self._root, text="SpendWise-Navigator", font=("Helvetica", 20))
        self._title_label.pack(pady=20)

        # Frame to contain all data
        self._frame = ttk.Frame(self._root)
        self._frame.pack()

        # TreeView Widget - Table to present our data
        self._tree = self._create_tree(columns=("Date", "Amount", "Category",))
        self._add_button, self._edit_button, self._del_button = self._create_buttons()
        
        # Refresh data inside preview
        # When initiating no data to delete but existing data added
        self._refresh_tree()    

    # Create Treeview widget
    def _create_tree(self, columns:tuple|list=()) -> ttk.Treeview:
        tree = ttk.Treeview(self._frame, columns=columns, show="headings")
        tree.heading("Date", text="Date")  
        tree.heading("Amount", text="Amount")
        tree.heading("Category", text="Category")
        tree.bind('<<TreeviewSelect>>', self._enable_buttons)
        tree.pack()

        return tree

    # Create the buttons under TreeView widget
    def _create_buttons(self)->tuple[ttk.Button, ttk.Button, ttk.Button]:
        add_button = ttk.Button(self._root, text="Add", command=self._add_expense)
        add_button.pack(pady=10, side=tk.RIGHT)

        edit_button = ttk.Button(self._root, text="Edit", state=tk.DISABLED, command=self._edit_expense)
        edit_button.pack(pady=10, side=tk.RIGHT)

        del_button = ttk.Button(self._root, text="Delete", state=tk.DISABLED, command=self._delete_expense)
        del_button.pack(pady=10, side=tk.LEFT)

        return (add_button, edit_button, del_button)
    
    def _enable_buttons(self, event):
        """Function to enable edit button and delete button for use

        Args:
            event (_type_): event variable required for when called through an Event
        """     
        self._edit_button.config(state=tk.NORMAL)
        self._del_button.config(state=tk.NORMAL)
    
    def _disable_buttons(self):
        """Function to disable edit button and delete button from use in certain cases"""
        self._edit_button.config(state=tk.DISABLED)
        self._del_button.config(state=tk.DISABLED)

    def _tree_insert(self, data:dict|list[dict]):
        """Function to add the data to Treeview widget

        Args:
            data (dict | list[dict]): The Expense data. Either a single expense as dictionary or list of multiple expenses as dictionary
        """
        # If only a single expense is given as a dictionary
        if data is dict:
            data = list[data,]  # Add dictionary to a list
        # Iterate through each expense data
        for expense in data:
            # add it to Treeview widget
            self._tree.insert("", tk.END, iid=expense['Index'], values=(expense['Date'], expense['Amount'], expense['Category'],))

    def _refresh_tree(self):
        """Automatically refreshes Treeview widget data when data is added removed or edited
        """
        # Iterate through iid of each element in Treeview
        for iid in self._tree.get_children():
            self._tree.delete(iid)  # Delete it
        self._tree_insert(data=self._db.expenses)   # Freshly delete all data

    def _input_shell(self, date:str=None, amount:int=None, category:str=None):
        
        def confirm():
            print(amountVar.get())
        
        def cancel():
            print('cancel')        

        window = tk.Toplevel(self._root)
        topframe = ttk.Frame(window)
        labelframe = ttk.Frame(topframe)
        entryframe = ttk.Frame(topframe)
        bottomframe = ttk.Frame(window)
        topframe.pack(pady=10 ,side=tk.TOP)
        bottomframe.pack(pady=10 ,side=tk.TOP)
        labelframe.pack(side=tk.LEFT)
        entryframe.pack(side=tk.LEFT)
        
        # Labels
        ttk.Label(labelframe, text="Day-Month", width=10).pack(padx=5, pady=5, side=tk.TOP)
        ttk.Label(labelframe, text="Year", width=10).pack(padx=5, pady=5, side=tk.TOP)
        ttk.Label(labelframe, text="Amount", width=10).pack(padx=5, pady=5, side=tk.TOP)
        ttk.Label(labelframe, text="Category", width=10).pack(padx=5, pady=5, side=tk.TOP)
        
        # Argument preparation
        date = date.split(':') if date else [1,1,2023]
        
        # Variables
        dayVar = tk.IntVar(value=date[0])
        monthVar = tk.IntVar(value=date[1])
        yearVar = tk.IntVar(value=date[2])
        amountVar = tk.IntVar(value=amount)
        categoryVar = tk.StringVar(value=category)
        days = [i for i in range(1,31)]
        months = [i for i in range(1,13)]
        years = [i for i in range(2000,2031)]

        # Entries
        dateframe = ttk.Frame(entryframe)
        dateframe.pack(side=tk.TOP)
        ttk.OptionMenu(dateframe, monthVar, monthVar.get(), *months).pack(side=tk.LEFT)
        ttk.OptionMenu(dateframe, dayVar, dayVar.get(), *days).pack(side=tk.LEFT)
        ttk.OptionMenu(entryframe, yearVar, yearVar.get(), *years).pack(side=tk.TOP)
        ttk.Entry(entryframe, textvariable=amountVar, width=10).pack(padx=5, pady=5, side=tk.TOP)
        ttk.OptionMenu(entryframe, categoryVar, 'None').pack(padx=5, pady=5, side=tk.TOP)


        # Buttons
        ttk.Button(bottomframe, text='cancel', command=cancel).pack(padx=5, pady=5, side=tk.LEFT)
        ttk.Button(bottomframe, text='confirm', command=confirm).pack(padx=5, pady=5, side=tk.RIGHT)


    def _add_expense(self):
        self._input_shell()

    def _edit_expense(self):
        # Get iid(index for DataFrame) of Treeview element
        for index in self._tree.selection():
            if index.isdigit(): # iid is in string format
                index = int(index)  # convert to int
        xpnse = self._db.get_expense(index=index)
        self._input_shell(date=xpnse['Date'], amount=xpnse['Amount'], category=xpnse['Category'])

    def _delete_expense(self):
        """Gets iid of selected element in Treeview and deletes it from database and refreshes Treeview
        """
        self._disable_buttons()
        # Get iid(index for DataFrame) of Treeview element
        for index in self._tree.selection():
            if index.isdigit(): # iid is in string format
                index = int(index)  # convert to int
            self._db.remove(index=index)    # remove row with index 'index' from Expenses
        self._refresh_tree()    # Refresh Treeview


    def start(self):
        self._root.mainloop()


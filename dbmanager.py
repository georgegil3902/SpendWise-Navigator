import pandas as pd
from pathlib import Path

class dbmanager:
    def __init__(self, name:str) -> None:
        """
        dbmanager class handles its own csv file containing expense data such as date of expense, how much was spent, category etc..
        Also offers options like grouping by month, day, category etc...
        It uses pandas to read and write the csv file and also for computational comfort.

        Args:
            name (str): The name variable is used to open a csv file with that name and if it does not exist creates one. 
        """
        self._name = name
        self._categories = ['food','groceries', 'travel']
        self._file_path = Path(f'files/{name}.csv')
        if self._file_path.exists():
            self._csv_df = pd.read_csv(filepath_or_buffer=self._file_path)  # open the csv file
            self._csv_df['Date'] = pd.to_datetime(self._csv_df['Date'], format='%Y-%m-%d')  # 'Date' column is in string format when opened so we convert it into datetime object
            # Retreiving non-default categories from DataFrame
            dbcats = tuple(self._csv_df['Category'].unique())
            for cat in dbcats:
                self.add_category(cat)
        else:
            columns = ['Date', 'Amount', 'Category']
            self._csv_df = pd.DataFrame(columns=columns)

    def commit(self)->bool:
        """The function writes the changes to pandas DataFrame to the csv file for permanent storage
        When the python file execution stops data in pandas DataFrame is lost, So by committing the changes to the csv file the data can be retreived later

        Returns:
            bool: return True if commit is succesful else return False
        """
        try:
            self._csv_df.to_csv(self._file_path, index=False)
            return True
        except FileNotFoundError:
            raise FileNotFoundError("The csv file is not found. It has either been moved or deleted.")
        except PermissionError:
            raise PermissionError("Unable to write to csv file. Lack of permision to modify file. Grant the appropriate permission.")

    def add(self, date:str, amount:float, category:str=None)->bool:
        """The function adds new expense data to DataFrame and commits it to csv file

        Args:
            date (str): date at which money was spent. A string in YYYY-MM-DD format
            amount (float): Amount of money spend
            category (str): Category of the expense. Defaults to None

        Returns:
            None: The function does not return anything
        """

        # Validate date format
        try:
            parsed_date = pd.to_datetime(date, format='%Y-%m-%d')   # Date is converted from string format to datetime object
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD format.")


        # Validate positive amount
        if amount <= 0:
            raise ValueError("Amount must be a positive number.")

        # Check if category is valid (if provided)
        if category is not None and category not in self._categories:
            raise ValueError("Invalid category.")

        # dictionary of {column_name: value,} pair
        new_row = {
            'Date': parsed_date,
            'Amount': amount, 
            'Category': category,
        }
        try:
            self._csv_df.loc[len(self._csv_df)] = new_row   # Try pandas df.loc method
        except:
            # Alternate method  - If df.loc doesnt work
            new_row_df = pd.DataFrame([new_row])    # we use pd.concat method that concats 2 DataFrames
            self._csv_df = pd.concat([self._csv_df, new_row_df], ignore_index=True)
        self.commit()

    def remove(self, index:int)->bool:
        """The function removes an expense from DataFrame and commits the changes to csv file

        Args:
            index (int): The index arg accepts index position of row to be removed

        Returns:
            bool: returns True if succesful otherwise False
        """
        try:
            self._csv_df.drop(index=index, inplace=True)
            self.commit()
            return True
        except KeyError:    # If given index doesnt exist in DataFrame return False
            return False

    def modify(self, index:int, date:str=None, amount:float=None, category:str=None):
        """The modify function accepts values that are to be modified in the row as keyword arguments and updates DataFrame
        and commits changes to csv file

        Args:
            index (int): index position of row to be edited
            date (str, optional): Updated date to update in 'YYYY-MM-DD' format string. Defaults to None.
            amount (float, optional): Updated spent amount. Defaults to None.
            category (str, optional): Updated category in which expense is classified. Defaults to None.

        Returns:
            bool: if values are succesffuly updates return True otherwise returns False
        """
        if index not in self._csv_df.index:
            return False
        if date:
            # Validate date format
            try:
                parsed_date = pd.to_datetime(date, format='%Y-%m-%d')   # Date is converted from string format to datetime object
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD format.")
            except Exception as e:
                raise e
            self._csv_df.loc[index, 'Date'] = parsed_date


        if amount:
            # Validate positive amount
            if amount <= 0:
                raise ValueError("Amount must be a positive number.")
            self._csv_df.loc[index, 'Amount'] = amount
        
        # Check if category is valid (if provided)
        if category:
            if category not in self._categories:
                raise ValueError("Invalid category.")
            self._csv_df.loc[index, 'Category'] = category

        self.commit()
        return True

    @property
    def expenses(self)->pd.DataFrame:
        """Table of all expense data with 
        columns = ['Date', 'Amount', 'Category']

        Returns:
            pd.DataFrame: DataFrame with all expense data
        """
        return self._csv_df

    @property
    def indexes(self):
        return tuple(self._csv_df.index)

    @property
    def categories(self)-> tuple[str]:
        """All categories existing in the DataFrame

        Returns:
            tuple: A tuple of strings of all category names
        """
        return tuple(self._categories)
    
    def add_category(self, new_category: str) -> None:
        """
        Add a new category to the list of existing categories.

        Args:
            new_category (str): The new category to be added.

        Returns:
            None
        """
        if new_category not in self._categories:
            self._categories.append(new_category)



if __name__=='__main__':
    dbm = dbmanager('expenses')
    # dbm.add(date='2003-02-06', amount=6, category='food')
    # dbm.add(date='2003-02-06', amount=6, category='food')
    # dbm.add(date='2003-02-06', amount=6, category='food')
    print(dbm.indexes)

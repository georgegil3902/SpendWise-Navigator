import dbmanager as db
import tkGUI as gui

if __name__=='__main__':
    dbm = db.dbmanager('expenses')
    app = gui.SpendWiseApp(dbm)

    app.start()
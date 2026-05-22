from hospital_management_system.database import connect_db
from tkinter import *
from gui.login import Loginwindow

db = connect_db()

if db:
    print("=" * 10, "Hospital Management System", "=" * 10)
    
root = Tk()
app = Loginwindow(root)
root.mainloop()

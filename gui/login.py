from tkinter import *
from tkinter import messagebox


class Loginwindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("500x400")
        self.root.config(bg='white')
        self.root.resizable(False, False)
        
        title = Label(self.root, text='Hospital Management System', font=("Arial", 20, "bold"), bg='white', fg='darkblue')
        title.pack(pady=20)
        
        frame = Frame(self.root, bg='lightgray')
        frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        username_label = Label(frame, text="Username:", font=('Arial', 12, "bold"), bg='lightgray')
        username_label.pack(pady=(30,5))
        
        self.username_entry = Entry(frame, font=("Arial", 12), width=30)
        self.username_entry.pack()
        
        password_label = Label(frame, text="Password:", font=('Arial', 12, "bold"), bg='lightgray')
        password_label.pack(pady=(15,5))
        
        self.password_entry = Entry(frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack()
        
        login_btn = Button(frame, text="Submit", font=("Arial", 12, "bold"), bg="darkblue", fg="white", width=15, command=self.login)
        login_btn.pack(pady=30)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == '' or password == '':
            messagebox.showerror("Error", "All Field are Required")

        elif username == 'admin' and password == 'admin123':
            messagebox.showinfo("Success", "Login Successfull!")

            self.root.destroy()

            from gui.dashboard import Dashboard

            Dashboard_root = Tk()
            app = Dashboard(Dashboard_root)
            Dashboard_root.mainloop()

        else:
            messagebox.showerror("Error", "Invalid Username or Password")
if __name__ == "__main__":
    root = Tk()
    obj = Loginwindow(root)
    root.mainloop()
from tkinter import *

class Dashboard:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management - Dashboard")
        self.root.geometry("1200x700")
        self.root.config(bg="#f5f7fa")
        
        header = Frame(self.root, bg="#1565c0", height=70)
        header.pack(side="top", fill=X)
        
        title = Label(header, text="Hospital Management System", font=("Arial", 24, "bold"), bg="#1565c0", fg="white")
        title.pack(pady=15)
        
        sidebar = Frame(self.root, bg="#1E293B", width=250)
        sidebar.pack(side=LEFT, fill=Y)
        
        menu_title = Label(sidebar, text="Dashboard Menu", font=('Arial', 15, 'bold'), bg='#1e293b', fg='white')
        menu_title.pack(pady=20)
        
        # buttons = ["Patient Management", "Doctor Management", "Appoinments", "Billings", "Reports", "Logout"]
        
        Button(sidebar, text='Patient Management', font=('Arial', 13, 'bold'), bg='#334155', fg='white', bd=0,
               width=22, height=2, command=self.open_patient).pack(pady=10)
        
        Button(sidebar, text='Doctor Management', font=('Arial', 13, 'bold'), bg='#334155', fg='white', bd=0,
               width=22, height=2, command=self.open_doctor).pack(pady=10)
        
        Button(sidebar, text='Appointments', font=('Arial', 13, 'bold'), bg='#334155', fg='white', bd=0,
               width=22, height=2, command=self.open_appointment).pack(pady=10)
        
        Button(sidebar, text='Billings', font=('Arial', 13, 'bold'), bg='#334155', fg='white', bd=0,
               width=22, height=2, command=self.open_billing).pack(pady=10)

        Button(sidebar, text='Reports', font=('Arial', 13, 'bold'), bg='#334155', fg='white', bd=0,
               width=22, height=2, command=self.open_reports).pack(pady=10)

        Button(sidebar, text='Logout', font=('Arial', 13, 'bold'), bg='#334155', fg='white', bd=0,
               width=22, height=2, command=self.root.destroy).pack(pady=10)
             
        # for button in buttons:
        #     btn = Button(
        #         sidebar, text=button, font=("Arial", 13, "bold"), bg="#334155", fg='white', activebackground='#2563eB',
        #         activeforeground='white', bd=0, cursor='hand2', width=22,height=2
        #     )
        #     btn.pack(pady=10)
            
        content = Frame(self.root, bg="#f5f7fa")
        content.pack()
        
        welcome = Label(content, text="Welcome to Hospital Management Dashboard",
                        font=('Arial', 25, 'bold'), bg='#f5f7fa', fg='#0f172a')
        welcome.pack()    
        
        card_frame = Frame(content, bg='#f5f7fa')
        card_frame.pack(pady=30)
        
        self.create_card(card_frame, "Total Patients", "120", 0, 0)
        self.create_card(card_frame, "Total Doctors", "25", 0, 1)
        self.create_card(card_frame, "Appoinments", "52", 1, 0)
        self.create_card(card_frame, "Revenue", "$45,000", 1, 1)
        
    def create_card(self, parent, title, value, row, col):
        card = Frame(
            parent, bg='white', width=250, height=140, bd=1, relief=SOLID
        )
        card.grid(row=row, column=col, padx=10, pady=10)
        card.propagate(False)

        title_label = Label(card, text=title, font=('Arial', 16, 'bold'), bg='white', fg='#475569')
        title_label.pack(pady=15)

        value_label = Label(card, text=value, font=('Arial', 24, 'bold'), bg='white', fg='#1565c0')
        value_label.pack()
    
    def open_patient(self):
        from gui.patient import PatientWindow

        new_window = Toplevel(self.root)
        PatientWindow(new_window)


    def open_doctor(self):
        from gui.doctor import DoctorWindow

        new_window = Toplevel(self.root)
        DoctorWindow(new_window)

    def open_appointment(self):
        from gui.appointment import AppointmentWindow

        new_window = Toplevel(self.root)
        AppointmentWindow(new_window)

    def open_billing(self):
        from gui.billing import BillingWindow

        new_window = Toplevel(self.root)
        BillingWindow(new_window)
                
    def open_reports(self):
        from gui.reports import ReportsWindow

        new_window = Toplevel(self.root)
        ReportsWindow(new_window)                
                    
if __name__ == "__main__":
    root = Tk()
    obj = Dashboard(root)
    root.mainloop()        
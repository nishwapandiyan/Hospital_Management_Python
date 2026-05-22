from tkinter import *
from tkinter import ttk, messagebox
from hospital_management_system.database import connect_db

class PatientWindow:
    
    def __init__(self,root):
        
        self.root = root
        self.root.title("Patient Management")
        self.root.geometry("1250x650")
        self.root.config(bg='white')
        
        title = Label(
            self.root, text='Patient Management',font=('Arial',22,'bold'),bg='#1565c0',fg='white',pady=10
        )
        title.pack(fill=X)
        
        # Label(self.root, text='Patient Module', font=('Arial',18),bg='white').pack(pady=40)
        
        
        self.name_var = StringVar()
        self.age_var = StringVar()
        self.gender_var = StringVar()
        self.phone_var = StringVar()
        self.disease_var = StringVar()
        self.address_var = StringVar()
        self.search_var = StringVar()
        self.patient_id = None
        
        left_frame = Frame(self.root, bd=2, relief='ridge', bg='white')
        left_frame.place(x=10, y=60, width=350, height=570)
        
        Label(left_frame, text='Patient Details',font=('Arial', 18, 'bold'), bg='white').pack(pady=10)
        
        Label(left_frame, text='Name',font=('Arial', 12), bg='white').pack()
        Entry(left_frame, textvariable=self.name_var,font=('Arial', 12),bd=2).pack(fill=X, padx=20)
        
        Label(left_frame, text='Age',font=('Arial', 12), bg='white').pack()
        Entry(left_frame, textvariable=self.age_var,font=('Arial', 12),bd=2).pack(fill=X, padx=20)
        
        Label(left_frame, text='Gender',font=('Arial', 12), bg='white').pack()
        Entry(left_frame, textvariable=self.gender_var,font=('Arial', 12),bd=2).pack(fill=X, padx=20)
        
        Label(left_frame, text='Phone',font=('Arial', 12), bg='white').pack()
        Entry(left_frame, textvariable=self.phone_var,font=('Arial', 12),bd=2).pack(fill=X, padx=20)
        
        Label(left_frame, text='Disease',font=('Arial', 12), bg='white').pack()
        Entry(left_frame, textvariable=self.disease_var,font=('Arial', 12),bd=2).pack(fill=X, padx=20)
        
        Label(left_frame, text='Address',font=('Arial', 12), bg='white').pack()
        Entry(left_frame, textvariable=self.address_var,font=('Arial', 12),bd=2).pack(fill=X, padx=20)                
        
        btn_frame = Frame(left_frame,bg='white')
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="Add", bg='green', fg='white', width=10,command=self.add_patient).grid(row=0,column=0,padx=5)
        Button(btn_frame, text="Update", bg='green', fg='white', width=10,command=self.update_patient).grid(row=0,column=1,padx=5)
        Button(btn_frame, text="Delete", bg='green', fg='white', width=10,command=self.delete_patient).grid(row=1,column=0,padx=5,pady=2)
        Button(btn_frame, text="Clear", bg='green', fg='white', width=10,command=self.clear_fields).grid(row=1,column=1,padx=5,pady=2)
        
        right_frame = Frame(self.root,bd=2, relief= 'ridge')
        right_frame.place(x=370, y=60, width=810, height= 520)
        
        search_frame = Frame(right_frame,  bg="#1565C0")
        search_frame.pack(fill=X)
        
        Label(search_frame, text='Search Name:', bg='#1565c0', fg='white', font=('Arial', 12,'bold')).pack(side=LEFT, padx=10)
        Entry(search_frame, textvariable=self.search_var, font=('Arial', 12)).pack(side=LEFT, padx=10)
        
        Button(search_frame, text='Search', command=self.search_patient).pack(side=LEFT)
        Button(search_frame, text='Show All', command=self.fetch_patient).pack(side=LEFT,padx=10)
        
        scroll_x = Scrollbar(right_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(right_frame, orient=VERTICAL)
        
        self.patient_table = ttk.Treeview(right_frame,columns=("id", "name", "age","gender", "phone","disease", "address"),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        
        # ================= TABLE STYLE =================
        style = ttk.Style()
        
        style.theme_use("clam")
        
        # Header Style
        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background="#1565C0",
            foreground="white",
            relief="flat"
        )
        
        style.map(
            "Treeview.Heading",
            background=[("active", "#0D47A1")]
        )
        
        # Table Style
        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=32,
            font=("Arial", 11),
            fieldbackground="white"
        )
        
        style.map(
            "Treeview",
            background=[("selected", "#90CAF9")],
            foreground=[("selected", "black")]
        )
        
        # Scrollbars
        scroll_x = ttk.Scrollbar(
            right_frame,
            orient=HORIZONTAL
        )
        
        scroll_y = ttk.Scrollbar(
            right_frame,
            orient=VERTICAL
        )
        
        # ================= TREEVIEW =================
        self.patient_table = ttk.Treeview(
            right_frame,
            columns=(
                "id",
                "name",
                "age",
                "gender",
                "phone",
                "disease",
                "address"
            ),
            xscrollcommand=scroll_x.set,
            yscrollcommand=scroll_y.set
        )
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        
        scroll_x.config(command=self.patient_table.xview)
        scroll_y.config(command=self.patient_table.yview)
        
        # Headings
        self.patient_table.heading("id", text="Patient ID")
        self.patient_table.heading("name", text="Full Name")
        self.patient_table.heading("age", text="Age")
        self.patient_table.heading("gender", text="Gender")
        self.patient_table.heading("phone", text="Phone")
        self.patient_table.heading("disease", text="Disease")
        self.patient_table.heading("address", text="Address")
        
        self.patient_table["show"] = "headings"
        
        # Column Widths
        self.patient_table.column("id", width=100, anchor=CENTER)
        self.patient_table.column("name", width=180)
        self.patient_table.column("age", width=80, anchor=CENTER)
        self.patient_table.column("gender", width=100, anchor=CENTER)
        self.patient_table.column("phone", width=140, anchor=CENTER)
        self.patient_table.column("disease", width=150)
        self.patient_table.column("address", width=220)
        
        self.patient_table.column("id", stretch=True)
        self.patient_table.column("name", stretch=True)
        self.patient_table.column("age", stretch=True)
        self.patient_table.column("gender", stretch=True)
        self.patient_table.column("phone", stretch=True)
        self.patient_table.column("disease", stretch=True)
        self.patient_table.column("address", stretch=True)
        
        self.patient_table.pack(
            fill=BOTH,
            expand=True
        )
        
        # Zebra Row Colors
        self.patient_table.tag_configure(
            "evenrow",
            background="#F8FAFC"
        )
        
        self.patient_table.tag_configure(
            "oddrow",
            background="#E3F2FD"
        )
        self.patient_table.bind(
            "<ButtonRelease-1>",
            self.get_cursor
        )

        self.fetch_patient()                        
        
    def add_patient(self):
        
        if self.name_var.get() == '':
            messagebox.showerror("Error", "Name Must Required")
            return
        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()
        
        try:
            query = """
                        insert into patients(name,age,gender,phone,disease,address) values(%s,%s,%s,%s,%s,%s) """
                        
            values = (self.name_var.get(), self.age_var.get(),self.gender_var.get(), self.phone_var.get(),self.disease_var.get(),self.address_var.get()) 
            
            cursor.execute(query,values)
            conn.commit()
            messagebox.showinfo("Success","Patient Details Addes Successfully")
            self.fetch_patient()
            self.clear_fields()
            
        except Exception as e:
            messagebox.showerror("Database Error",str(e))
        finally:
            cursor.close()
            conn.close()                   
            
        
    def update_patient(self):
        
        if self.patient_id is None:
            messagebox.showerror("Error","Please Select Patient ID!")
            return
        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            query = """
                        update patients set name=%s, age=%s, gender=%s, phone=%s, disease=%s, address=%s where patient_id=%s"""
            values = (self.name_var.get(), self.age_var.get(), self.gender_var.get(),self.phone_var.get(),self.disease_var.get(),self.address_var.get(),self.patient_id )    
            
            cursor.execute(query,values)
            conn.commit()
            messagebox.showinfo("Success","Patient Updated Successfully")
            
            self.fetch_patient()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error",str(e))
        finally:
            cursor.close()
            conn.close()              
            
    def delete_patient(self):
        
        if self.patient_id is None:
            messagebox.showerror("Error", "Please Select the Patient First!")
            return
        confirm = messagebox.askyesno("Confirm","Do you want to Delete Patient")
        if not confirm:
            return
        conn = connect_db()
        if conn is None:
            return
        cursor = conn.cursor()
        try:
            cursor.execute("delete from patients where patient_id=%s",(self.patient_id,))
            conn.commit()
            messagebox.showinfo("Deleted","Patient Deleted Successfully")
            self.fetch_patient()
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Database Error",str(e))
        finally:
            cursor.close()
            conn.close()
                    
    def search_patient(self):
     
     
         if self.search_var.get() == "":
             messagebox.showerror(
                 "Error",
                 "Please enter patient name!"
             )
             return
     
         conn = connect_db()
     
         if conn is None:
             return
     
         cursor = conn.cursor()
     
         try:
             query = """
             SELECT * FROM patients
             WHERE name LIKE %s
             """
     
             search_text = "%" + self.search_var.get() + "%"
     
             cursor.execute(query, (search_text,))
             rows = cursor.fetchall()
     
             self.patient_table.delete(
                 *self.patient_table.get_children()
             )
     
             for row in rows:
                 self.patient_table.insert(
                     "",
                     END,
                     values=row
                 )
     
         except Exception as e:
             messagebox.showerror(
                 "Database Error",
                 str(e)
             )
     
         finally:
             cursor.close()
             conn.close()
                        
    def fetch_patient(self):

        conn = connect_db()
    
        if conn is None:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute(
                "SELECT * FROM patients"
            )
    
            rows = cursor.fetchall()
    
            self.patient_table.delete(
                *self.patient_table.get_children()
            )
    
            count = 0
    
            for row in rows:
    
                if count % 2 == 0:
                    self.patient_table.insert(
                        "",
                        END,
                        values=row,
                        tags=("evenrow",)
                    )
                else:
                    self.patient_table.insert(
                        "",
                        END,
                        values=row,
                        tags=("oddrow",)
                    )
    
                count += 1
    
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
    
        finally:
            cursor.close()
            conn.close()
            
    def clear_fields(self):
        self.patient_id = None
        self.name_var.set("")
        self.age_var.set("")
        self.gender_var.set("")
        self.phone_var.set("")
        self.disease_var.set("")
        self.address_var.set("")

    def get_cursor(self, event=""):
        cursor_row = self.patient_table.focus()
        content = self.patient_table.item(cursor_row)

        row = content["values"]

        if row:
            self.patient_id = row[0]
            self.name_var.set(row[1])
            self.age_var.set(row[2])
            self.gender_var.set(row[3])
            self.phone_var.set(row[4])
            self.disease_var.set(row[5])
            self.address_var.set(row[6])    
            
if __name__ == "__main__":
    root = Tk()
    obj = PatientWindow(root)
    root.mainloop()
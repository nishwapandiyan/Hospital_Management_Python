from tkinter import *
from tkinter import ttk, messagebox
from hospital_management_system.database import connect_db


class DoctorWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Doctor Management")
        self.root.geometry("1250x650")
        self.root.config(bg="white")

        # ================= TITLE =================
        title = Label(
            self.root,
            text="Doctor Management System",
            font=("Arial", 22, "bold"),
            bg="#1565C0",
            fg="white",
            pady=10
        )
        title.pack(fill=X)

        # ================= VARIABLES =================
        self.doctor_id = None

        self.name_var = StringVar()
        self.department_var = StringVar()
        self.specialization_var = StringVar()
        self.phone_var = StringVar()
        self.time_var = StringVar()
        self.fee_var = StringVar()
        self.search_var = StringVar()

        # ================= LEFT FRAME =================
        left_frame = Frame(
            self.root,
            bd=2,
            relief=RIDGE,
            bg="white"
        )

        left_frame.place(
            x=10,
            y=60,
            width=350,
            height=570
        )

        Label(
            left_frame,
            text="Doctor Details",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        fields = [
            ("Doctor Name", self.name_var),
            ("Department", self.department_var),
            ("Specialization", self.specialization_var),
            ("Phone", self.phone_var),
            ("Available Time", self.time_var),
            ("Consultation Fee", self.fee_var)
        ]

        for label_text, variable in fields:

            Label(
                left_frame,
                text=label_text,
                font=("Arial", 12,'bold'),
                bg="white"
            ).pack()

            Entry(
                left_frame,
                textvariable=variable,
                font=("Arial", 12)
            ).pack(fill=X, padx=20, pady=3)

        # ================= BUTTONS =================
        btn_frame = Frame(left_frame, bg="white")
        btn_frame.pack(pady=20)

        Button(
            btn_frame,
            text="Add",
            command=self.add_doctor,
            bg="green",
            fg="white",
            width=10
        ).grid(row=0, column=0, padx=5)

        Button(
            btn_frame,
            text="Update",
            command=self.update_doctor,
            bg="blue",
            fg="white",
            width=10
        ).grid(row=0, column=1, padx=5)

        Button(
            btn_frame,
            text="Delete",
            command=self.delete_doctor,
            bg="red",
            fg="white",
            width=10
        ).grid(row=1, column=0, pady=10)

        Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields,
            bg="gray",
            fg="white",
            width=10
        ).grid(row=1, column=1)

        # ================= RIGHT FRAME =================
        right_frame = Frame(
            self.root,
            bd=2,
            relief=RIDGE
        )

        right_frame.place(
            x=370,
            y=60,
            width=860,
            height=570
        )

        search_frame = Frame(
            right_frame,
            bg="#1565C0"
        )
        search_frame.pack(fill=X)

        Label(
            search_frame,
            text="Search Doctor:",
            bg="#1565C0",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(side=LEFT, padx=10)

        Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 12)
        ).pack(side=LEFT, padx=10)

        Button(
            search_frame,
            text="Search",
            command=self.search_doctor
        ).pack(side=LEFT)

        Button(
            search_frame,
            text="Show All",
            command=self.fetch_data
        ).pack(side=LEFT, padx=10)

        # ================= TABLE STYLE =================
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview.Heading",
            font=("Arial", 12, "bold"),
            background="#1565C0",
            foreground="white"
        )

        style.configure(
            "Treeview",
            rowheight=32,
            font=("Arial", 11)
        )
        style.map(
            "Treeview.Heading",
            background=[("active", "#0D47A1")]
        )
        scroll_y = ttk.Scrollbar(
            right_frame,
            orient=VERTICAL
        )

        self.doctor_table = ttk.Treeview(
            right_frame,
            columns=(
                "id",
                "name",
                "department",
                "specialization",
                "phone",
                "time",
                "fee"
            ),
            yscrollcommand=scroll_y.set
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.doctor_table.yview)

        headings = [
            ("id", "ID", 70),
            ("name", "Doctor Name", 170),
            ("department", "Department", 150),
            ("specialization", "Specialization", 170),
            ("phone", "Phone", 140),
            ("time", "Available Time", 140),
            ("fee", "Fee", 100)
        ]

        for col, text, width in headings:
            self.doctor_table.heading(col, text=text)
            self.doctor_table.column(col, width=width)

        self.doctor_table["show"] = "headings"
        self.doctor_table.pack(fill=BOTH, expand=True)

        self.doctor_table.bind(
            "<ButtonRelease-1>",
            self.get_cursor
        )

        self.fetch_data()

    # ================= ADD =================
    def add_doctor(self):

        if self.name_var.get() == "":
            messagebox.showerror(
                "Error",
                "Doctor Name Required!"
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO doctors
        (
            doctor_name,
            department,
            specialization,
            phone,
            available_time,
            consultation_fee
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            self.name_var.get(),
            self.department_var.get(),
            self.specialization_var.get(),
            self.phone_var.get(),
            self.time_var.get(),
            self.fee_var.get()
        )

        cursor.execute(query, values)
        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            "Doctor Added Successfully"
        )

        self.fetch_data()
        self.clear_fields()

    # ================= FETCH =================
    def fetch_data(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM doctors")
        rows = cursor.fetchall()

        self.doctor_table.delete(
            *self.doctor_table.get_children()
        )

        for row in rows:
            self.doctor_table.insert(
                "",
                END,
                values=row
            )

        conn.close()

    # ================= CURSOR =================
    def get_cursor(self, event=""):

        row_id = self.doctor_table.focus()
        content = self.doctor_table.item(row_id)
        row = content["values"]

        if row:
            self.doctor_id = row[0]

            self.name_var.set(row[1])
            self.department_var.set(row[2])
            self.specialization_var.set(row[3])
            self.phone_var.set(row[4])
            self.time_var.set(row[5])
            self.fee_var.set(row[6])

    # ================= UPDATE =================
    def update_doctor(self):
    
        if self.doctor_id is None:
            messagebox.showerror(
                "Error",
                "Please select a doctor first!"
            )
            return
    
        conn = connect_db()
    
        if conn is None:
            return
    
        cursor = conn.cursor()
    
        try:
            query = """
            UPDATE doctors
            SET doctor_name=%s,
                department=%s,
                specialization=%s,
                phone=%s,
                available_time=%s,
                consultation_fee=%s
            WHERE doctor_id=%s
            """
    
            values = (
                self.name_var.get(),
                self.department_var.get(),
                self.specialization_var.get(),
                self.phone_var.get(),
                self.time_var.get(),
                self.fee_var.get(),
                self.doctor_id
            )
    
            cursor.execute(query, values)
            conn.commit()
    
            messagebox.showinfo(
                "Success",
                "Doctor Updated Successfully"
            )
    
            self.fetch_data()
            self.clear_fields()
    
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
    
        finally:
            cursor.close()
            conn.close()
    
        # ================= DELETE =================
    def delete_doctor(self):
    
        if self.doctor_id is None:
            messagebox.showerror(
                "Error",
                "Please select a doctor first!"
            )
            return
    
        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Do you want to delete this doctor?"
        )
    
        if not confirm:
            return
    
        conn = connect_db()
    
        if conn is None:
            return
    
        cursor = conn.cursor()
    
        try:
            cursor.execute(
                "DELETE FROM doctors WHERE doctor_id=%s",
                (self.doctor_id,)
            )
    
            conn.commit()
    
            messagebox.showinfo(
                "Deleted",
                "Doctor Deleted Successfully"
            )
    
            self.fetch_data()
            self.clear_fields()
    
        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )
    
        finally:
            cursor.close()
            conn.close()
    
        # ================= SEARCH =================
    def search_doctor(self):
    
        if self.search_var.get() == "":
            messagebox.showerror(
                "Error",
                "Please enter doctor name!"
            )
            return
    
        conn = connect_db()
    
        if conn is None:
            return
    
        cursor = conn.cursor()
    
        try:
            query = """
            SELECT * FROM doctors
            WHERE doctor_name LIKE %s
            """
    
            search_text = "%" + self.search_var.get() + "%"
    
            cursor.execute(query, (search_text,))
            rows = cursor.fetchall()
    
            self.doctor_table.delete(
                *self.doctor_table.get_children()
            )
    
            for row in rows:
                self.doctor_table.insert(
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
    
        # ================= CLEAR =================
    def clear_fields(self):
    
        self.doctor_id = None
    
        self.name_var.set("")
        self.department_var.set("")
        self.specialization_var.set("")
        self.phone_var.set("")
        self.time_var.set("")
        self.fee_var.set("")
        
if __name__ == "__main__":
    root = Tk()
    obj = DoctorWindow(root)
    root.mainloop()        
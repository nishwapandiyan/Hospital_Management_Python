from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from hospital_management_system.database import connect_db


class AppointmentWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Appointment Management")
        self.root.geometry("1250x650")
        self.root.config(bg="white")

        # ================= TITLE =================
        title = Label(
            self.root,
            text="Appointment Management",
            font=("Arial", 22, "bold"),
            bg="#1565C0",
            fg="white",
            pady=10
        )
        title.pack(fill=X)

        # ================= VARIABLES =================
        self.appointment_id = None

        self.patient_var = StringVar()
        self.doctor_var = StringVar()
        self.fee_var = StringVar()
        self.time_var = StringVar()
        self.status_var = StringVar()

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
            text="Appointment Details",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        # ================= PATIENT =================
        Label(
            left_frame,
            text="Patient Name",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.patient_combo = ttk.Combobox(
            left_frame,
            textvariable=self.patient_var,
            font=("Arial", 12),
            state="readonly"
        )

        self.patient_combo.pack(
            fill=X,
            padx=20,
            pady=5
        )

        # ================= DOCTOR =================
        Label(
            left_frame,
            text="Doctor Name",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.doctor_combo = ttk.Combobox(
            left_frame,
            textvariable=self.doctor_var,
            font=("Arial", 12),
            state="readonly"
        )

        self.doctor_combo.pack(
            fill=X,
            padx=20,
            pady=5
        )

        self.doctor_combo.bind(
            "<<ComboboxSelected>>",
            self.get_doctor_fee
        )

        # ================= FEE =================
        Label(
            left_frame,
            text="Consultation Fee",
            font=("Arial", 12),
            bg="white"
        ).pack()

        Entry(
            left_frame,
            textvariable=self.fee_var,
            font=("Arial", 12),
            state="readonly"
        ).pack(fill=X, padx=20)

        # ================= DATE =================
        Label(
            left_frame,
            text="Appointment Date",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.date_entry = DateEntry(
            left_frame,
            width=20,
            font=("Arial", 12),
            date_pattern="yyyy-mm-dd"
        )

        self.date_entry.pack(pady=5)

        # ================= TIME =================
        Label(
            left_frame,
            text="Appointment Time",
            font=("Arial", 12),
            bg="white"
        ).pack()

        Entry(
            left_frame,
            textvariable=self.time_var,
            font=("Arial", 12)
        ).pack(fill=X, padx=20)

        # ================= STATUS =================
        Label(
            left_frame,
            text="Status",
            font=("Arial", 12),
            bg="white"
        ).pack()

        self.status_combo = ttk.Combobox(
            left_frame,
            textvariable=self.status_var,
            values=[
                "Booked",
                "Completed",
                "Cancelled"
            ],
            state="readonly"
        )

        self.status_combo.pack(
            fill=X,
            padx=20,
            pady=5
        )

        # ================= BUTTONS =================
        btn_frame = Frame(
            left_frame,
            bg="white"
        )

        btn_frame.pack(pady=20)

        Button(
            btn_frame,
            text="Book",
            command=self.add_appointment,
            bg="green",
            fg="white",
            width=12
        ).grid(row=0, column=0, padx=5)

        Button(
            btn_frame,
            text="Delete",
            command=self.delete_appointment,
            bg="red",
            fg="white",
            width=12
        ).grid(row=0, column=1)

        Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields,
            bg="gray",
            fg="white",
            width=12
        ).grid(row=1, column=0, columnspan=2, pady=10)

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

        # ================= SCROLLBAR =================
        scroll_y = ttk.Scrollbar(
            right_frame,
            orient=VERTICAL
        )

        # ================= TABLE =================
        self.appointment_table = ttk.Treeview(
            right_frame,
            columns=(
                "id",
                "patient",
                "doctor",
                "fee",
                "date",
                "time",
                "status"
            ),
            yscrollcommand=scroll_y.set
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(
            command=self.appointment_table.yview
        )

        headings = [
            ("id", "ID", 70),
            ("patient", "Patient", 150),
            ("doctor", "Doctor", 150),
            ("fee", "Fee", 100),
            ("date", "Date", 120),
            ("time", "Time", 120),
            ("status", "Status", 120)
        ]

        for col, text, width in headings:
            self.appointment_table.heading(
                col,
                text=text
            )

            self.appointment_table.column(
                col,
                width=width,
                anchor=CENTER
            )

        self.appointment_table["show"] = "headings"

        self.appointment_table.pack(
            fill=BOTH,
            expand=True
        )

        self.appointment_table.bind(
            "<ButtonRelease-1>",
            self.get_cursor
        )

        # ================= LOAD DATA =================
        self.load_patients()
        self.load_doctors()
        self.fetch_data()

    # ================= LOAD PATIENTS =================
    def load_patients(self):

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT name FROM patients"
            )

            patients = cursor.fetchall()

            self.patient_combo["values"] = [
                patient[0]
                for patient in patients
            ]

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            cursor.close()
            conn.close()

    # ================= LOAD DOCTORS =================
    def load_doctors(self):

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT doctor_name FROM doctors"
            )

            doctors = cursor.fetchall()

            self.doctor_combo["values"] = [
                doctor[0]
                for doctor in doctors
            ]

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            cursor.close()
            conn.close()

    # ================= GET DOCTOR FEE =================
    def get_doctor_fee(self, event=""):

        if self.doctor_var.get() == "":
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            query = """
            SELECT consultation_fee
            FROM doctors
            WHERE doctor_name=%s
            """

            cursor.execute(
                query,
                (self.doctor_var.get(),)
            )

            result = cursor.fetchone()

            if result:
                self.fee_var.set(result[0])

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            cursor.close()
            conn.close()

    # ================= ADD APPOINTMENT =================
    def add_appointment(self):

        if (
            self.patient_var.get() == "" or
            self.doctor_var.get() == "" or
            self.time_var.get() == "" or
            self.status_var.get() == ""
        ):

            messagebox.showerror(
                "Error",
                "Please fill all fields!"
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            query = """
            INSERT INTO appointments
            (
                patient_name,
                doctor_name,
                consultation_fee,
                appointment_date,
                appointment_time,
                status
            )
            VALUES (%s,%s,%s,%s,%s,%s)
            """

            values = (
                self.patient_var.get(),
                self.doctor_var.get(),
                self.fee_var.get(),
                self.date_entry.get_date(),
                self.time_var.get(),
                self.status_var.get()
            )

            cursor.execute(query, values)
            conn.commit()

            messagebox.showinfo(
                "Success",
                "Appointment Booked Successfully"
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

    # ================= FETCH DATA =================
    def fetch_data(self):

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT * FROM appointments"
            )

            rows = cursor.fetchall()

            self.appointment_table.delete(
                *self.appointment_table.get_children()
            )

            for row in rows:
                self.appointment_table.insert(
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

    # ================= GET CURSOR =================
    def get_cursor(self, event=""):

        row_id = self.appointment_table.focus()

        content = self.appointment_table.item(
            row_id
        )

        row = content["values"]

        if row:

            self.appointment_id = row[0]

            self.patient_var.set(row[1])
            self.doctor_var.set(row[2])
            self.fee_var.set(row[3])

            self.date_entry.set_date(
                str(row[4])
            )

            self.time_var.set(row[5])
            self.status_var.set(row[6])

    # ================= DELETE =================
    def delete_appointment(self):

        if self.appointment_id is None:

            messagebox.showerror(
                "Error",
                "Please select an appointment!"
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Delete this appointment?"
        )

        if not confirm:
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM appointments
                WHERE appointment_id=%s
                """,
                (self.appointment_id,)
            )

            conn.commit()

            messagebox.showinfo(
                "Deleted",
                "Appointment Deleted Successfully"
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

    # ================= CLEAR =================
    def clear_fields(self):

        self.appointment_id = None

        self.patient_var.set("")
        self.doctor_var.set("")
        self.fee_var.set("")
        self.time_var.set("")
        self.status_var.set("")

        self.date_entry.set_date("today")


if __name__ == "__main__":
    root = Tk()
    obj = AppointmentWindow(root)
    root.mainloop()
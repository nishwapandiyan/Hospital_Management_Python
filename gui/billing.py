from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from hospital_management_system.database import connect_db


class BillingWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Billing Management")
        self.root.geometry("1200x720")
        self.root.config(bg="white")

        # ================= TITLE =================
        title = Label(
            self.root,
            text="Billing Management",
            font=("Arial", 22, "bold"),
            bg="#1565C0",
            fg="white",
            pady=10
        )
        title.pack(fill=X)

        # ================= VARIABLES =================
        self.bill_id = None

        self.patient_var = StringVar()
        self.doctor_var = StringVar()

        self.consultation_var = StringVar()
        self.medicine_var = StringVar()
        self.room_var = StringVar()
        self.other_var = StringVar()
        self.total_var = StringVar()

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
            height=600
        )

        Label(
            left_frame,
            text="Billing Details",
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
            state="readonly",
            font=("Arial", 12)
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
            state="readonly",
            font=("Arial", 12)
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

        # ================= CHARGES =================
        fields = [
            ("Consultation Fee", self.consultation_var),
            ("Medicine Charge", self.medicine_var),
            ("Room Charge", self.room_var),
            ("Other Charge", self.other_var),
            ("Total Amount", self.total_var)
        ]

        for text, variable in fields:

            Label(
                left_frame,
                text=text,
                font=("Arial", 12),
                bg="white"
            ).pack()

            Entry(
                left_frame,
                textvariable=variable,
                font=("Arial", 12)
            ).pack(fill=X, padx=20, pady=3)

        # ================= BILL DATE =================
        Label(
            left_frame,
            text="Bill Date",
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

        # ================= BUTTONS =================
        btn_frame = Frame(
            left_frame,
            bg="white"
        )

        btn_frame.pack(pady=20)

        Button(
            btn_frame,
            text="Calculate",
            command=self.calculate_total,
            bg="orange",
            fg="white",
            width=12
        ).grid(row=0, column=0, padx=5)

        Button(
            btn_frame,
            text="Generate Bill",
            command=self.add_bill,
            bg="green",
            fg="white",
            width=12
        ).grid(row=0, column=1)

        Button(
            btn_frame,
            text="Delete",
            command=self.delete_bill,
            bg="red",
            fg="white",
            width=12
        ).grid(row=1, column=0, pady=10)

        Button(
            btn_frame,
            text="Clear",
            command=self.clear_fields,
            bg="gray",
            fg="white",
            width=12
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
            height=600
        )

        # ================= SCROLLBAR =================
        scroll_y = ttk.Scrollbar(
            right_frame,
            orient=VERTICAL
        )

        # ================= TABLE =================
        self.billing_table = ttk.Treeview(
            right_frame,
            columns=(
                "id",
                "patient",
                "doctor",
                "consultation",
                "medicine",
                "room",
                "other",
                "total",
                "date"
            ),
            yscrollcommand=scroll_y.set
        )

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(
            command=self.billing_table.yview
        )

        headings = [
            ("id", "Bill ID", 80),
            ("patient", "Patient", 130),
            ("doctor", "Doctor", 130),
            ("consultation", "Consultation", 110),
            ("medicine", "Medicine", 100),
            ("room", "Room", 100),
            ("other", "Other", 100),
            ("total", "Total", 100),
            ("date", "Bill Date", 120)
        ]

        for col, text, width in headings:

            self.billing_table.heading(
                col,
                text=text
            )

            self.billing_table.column(
                col,
                width=width,
                anchor=CENTER
            )

        self.billing_table["show"] = "headings"

        self.billing_table.pack(
            fill=BOTH,
            expand=True
        )

        self.billing_table.bind(
            "<ButtonRelease-1>",
            self.get_cursor
        )

        self.load_patients()
        self.load_doctors()
        self.fetch_data()

    # ================= LOAD PATIENTS =================
    def load_patients(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT name FROM patients"
        )

        patients = cursor.fetchall()

        self.patient_combo["values"] = [
            patient[0]
            for patient in patients
        ]

        conn.close()

    # ================= LOAD DOCTORS =================
    def load_doctors(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT doctor_name FROM doctors"
        )

        doctors = cursor.fetchall()

        self.doctor_combo["values"] = [
            doctor[0]
            for doctor in doctors
        ]

        conn.close()

    # ================= GET DOCTOR FEE =================
    def get_doctor_fee(self, event=""):

        conn = connect_db()
        cursor = conn.cursor()

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
            self.consultation_var.set(
                result[0]
            )

        conn.close()

    # ================= CALCULATE =================
    def calculate_total(self):

        consultation = float(
            self.consultation_var.get() or 0
        )

        medicine = float(
            self.medicine_var.get() or 0
        )

        room = float(
            self.room_var.get() or 0
        )

        other = float(
            self.other_var.get() or 0
        )

        total = (
            consultation +
            medicine +
            room +
            other
        )

        self.total_var.set(total)

    # ================= ADD BILL =================
    def add_bill(self):

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        INSERT INTO billing
        (
            patient_name,
            doctor_name,
            consultation_fee,
            medicine_charge,
            room_charge,
            other_charge,
            total_amount,
            bill_date
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """

        values = (
            self.patient_var.get(),
            self.doctor_var.get(),
            self.consultation_var.get(),
            self.medicine_var.get(),
            self.room_var.get(),
            self.other_var.get(),
            self.total_var.get(),
            self.date_entry.get_date()
        )

        cursor.execute(query, values)
        conn.commit()

        conn.close()

        messagebox.showinfo(
            "Success",
            "Bill Generated Successfully"
        )

        self.fetch_data()
        self.clear_fields()

    # ================= FETCH =================
    def fetch_data(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM billing"
        )

        rows = cursor.fetchall()

        self.billing_table.delete(
            *self.billing_table.get_children()
        )

        for row in rows:

            self.billing_table.insert(
                "",
                END,
                values=row
            )

        conn.close()

    # ================= CURSOR =================
    def get_cursor(self, event=""):

        row_id = self.billing_table.focus()

        content = self.billing_table.item(
            row_id
        )

        row = content["values"]

        if row:

            self.bill_id = row[0]

            self.patient_var.set(row[1])
            self.doctor_var.set(row[2])

            self.consultation_var.set(row[3])
            self.medicine_var.set(row[4])
            self.room_var.set(row[5])
            self.other_var.set(row[6])

            self.total_var.set(row[7])

            self.date_entry.set_date(
                str(row[8])
            )

    # ================= DELETE =================
    def delete_bill(self):

        if self.bill_id is None:
            messagebox.showerror(
                "Error",
                "Select a bill first!"
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM billing WHERE bill_id=%s",
            (self.bill_id,)
        )

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Deleted",
            "Bill Deleted Successfully"
        )

        self.fetch_data()
        self.clear_fields()

    # ================= CLEAR =================
    def clear_fields(self):

        self.bill_id = None

        self.patient_var.set("")
        self.doctor_var.set("")

        self.consultation_var.set("")
        self.medicine_var.set("")
        self.room_var.set("")
        self.other_var.set("")
        self.total_var.set("")

        self.date_entry.set_date("today")


if __name__ == "__main__":
    root = Tk()
    obj = BillingWindow(root)
    root.mainloop()
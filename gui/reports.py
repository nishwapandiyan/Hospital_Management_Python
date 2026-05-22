from tkinter import *
from tkinter import messagebox
from hospital_management_system.database import connect_db


class ReportsWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Reports Management")
        self.root.geometry("1350x750")
        self.root.config(bg="#f5f7fa")

        # ================= TITLE =================
        title = Label(
            self.root,
            text="Reports Management System",
            font=("Segoe UI", 26, "bold"),
            bg="#1565C0",
            fg="white",
            pady=12
        )
        title.pack(fill=X)

        # ================= SUBTITLE =================
        Label(
            self.root,
            text="Hospital Analytics Dashboard",
            font=("Segoe UI", 12),
            bg="#f5f7fa",
            fg="gray"
        ).pack(pady=12)

        # ================= MAIN FRAME =================
        main_frame = Frame(
            self.root,
            bg="#f5f7fa"
        )

        main_frame.pack(
            fill=BOTH,
            expand=True,
            padx=40,
            pady=20
        )

        # Responsive Grid
        for i in range(3):
            main_frame.grid_columnconfigure(
                i,
                weight=1
            )

        for i in range(2):
            main_frame.grid_rowconfigure(
                i,
                weight=1
            )

        # ================= REPORT CARDS =================
        self.patient_label = self.create_card(
            main_frame,
            "👤 Total Patients",
            "#1976D2",
            0,
            0
        )

        self.doctor_label = self.create_card(
            main_frame,
            "🩺 Total Doctors",
            "#2E7D32",
            0,
            1
        )

        self.revenue_label = self.create_card(
            main_frame,
            "💰 Total Revenue",
            "#C62828",
            0,
            2
        )

        self.appointment_label = self.create_card(
            main_frame,
            "📅 Appointments",
            "#EF6C00",
            1,
            0
        )

        self.bill_label = self.create_card(
            main_frame,
            "🧾 Total Bills",
            "#6A1B9A",
            1,
            1
        )

        # Empty space card for balance
        empty_frame = Frame(
            main_frame,
            bg="#f5f7fa"
        )
        empty_frame.grid(
            row=1,
            column=2,
            padx=20,
            pady=20,
            sticky="nsew"
        )

        # ================= REFRESH BUTTON =================
        Button(
            self.root,
            text="🔄 Refresh Report",
            command=self.load_reports,
            bg="#1565C0",
            fg="white",
            font=("Segoe UI", 12, "bold"),
            width=20,
            cursor="hand2",
            relief=FLAT
        ).pack(pady=20)

        self.load_reports()

    # ================= CARD DESIGN =================
    def create_card(
        self,
        parent,
        title,
        color,
        row,
        column
    ):

        card = Frame(
            parent,
            bg=color,
            bd=0,
            relief=RIDGE,
            highlightthickness=0
        )

        card.grid(
            row=row,
            column=column,
            padx=20,
            pady=20,
            sticky="nsew"
        )

        card.config(
            width=350,
            height=180
        )

        card.grid_propagate(False)

        # Title
        Label(
            card,
            text=title,
            font=("Segoe UI", 18, "bold"),
            bg=color,
            fg="white"
        ).pack(pady=(30, 10))

        # Value
        value_label = Label(
            card,
            text="0",
            font=("Segoe UI", 34, "bold"),
            bg=color,
            fg="white"
        )

        value_label.pack()

        return value_label

    # ================= LOAD REPORTS =================
    def load_reports(self):

        conn = connect_db()

        if conn is None:
            return

        cursor = conn.cursor()

        try:

            # Total Patients
            cursor.execute(
                "SELECT COUNT(*) FROM patients"
            )
            patient_count = cursor.fetchone()[0]

            # Total Doctors
            cursor.execute(
                "SELECT COUNT(*) FROM doctors"
            )
            doctor_count = cursor.fetchone()[0]

            # Total Appointments
            cursor.execute(
                "SELECT COUNT(*) FROM appointments"
            )
            appointment_count = cursor.fetchone()[0]

            # Total Bills
            cursor.execute(
                "SELECT COUNT(*) FROM billing"
            )
            bill_count = cursor.fetchone()[0]

            # Total Revenue
            cursor.execute(
                """
                SELECT SUM(total_amount)
                FROM billing
                """
            )

            revenue = cursor.fetchone()[0]

            if revenue is None:
                revenue = 0

            # ================= UPDATE UI =================
            self.patient_label.config(
                text=str(patient_count)
            )

            self.doctor_label.config(
                text=str(doctor_count)
            )

            self.appointment_label.config(
                text=str(appointment_count)
            )

            self.bill_label.config(
                text=str(bill_count)
            )

            self.revenue_label.config(
                text=f"₹ {revenue}"
            )

        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e)
            )

        finally:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = ReportsWindow(root)
    root.mainloop()
from tkinter import Tk, StringVar, messagebox, font
from tkinter.ttk import (
    Frame,
    Label,
    Entry,
    Button,
    Treeview,
    Style,
    Labelframe,
    Separator,
)
from datetime import datetime
import sqlite3
from payments_tracker import (
    add_loan,
    initialize_database,
    add_transaction,
    calculate_interest,
    DB_PATH,
)
from ttkthemes import ThemedTk


class PaymentTrackerApp(ThemedTk):
    def __init__(self):
        super().__init__()
        self.title("Car Payments Tracker")
        # self.geometry("800x600")
        self.set_theme("arc")
        self.minsize(1400, 400)
        self.tk_font = font.nametofont("TkDefaultFont")
        self.tk_font_bold = self.tk_font.copy()
        self.tk_font_bold.configure(weight="bold")

        initialize_database()

        # Call the create_widgets function to initialize all widgets
        self.create_widgets()

    def create_widgets(self):
        """Call all widget creation functions."""
        frame = Frame(self)
        frame.pack(expand=True, fill="both")

        sidebar_form = Frame(frame)
        sidebar_form.pack(side="left", expand=True, fill="y", padx=16, pady=16)

        root_form = Frame(frame)
        root_form.pack(side="left", expand=True, fill="both", padx=16, pady=16)

        separator_style = Style()
        separator_style.configure("Separator.TFrame", background="#d7d7d7")

        self.create_initial_loan_form(sidebar_form)
        Frame(sidebar_form, height=1, style="Separator.TFrame").pack(fill="x")
        self.create_payment_form(sidebar_form)
        Frame(sidebar_form, height=1, style="Separator.TFrame").pack(fill="x")
        self.create_interest_form(sidebar_form)

        self.create_transactions_table(root_form)

    def create_initial_loan_form(self, master):
        form = Frame(master)
        form.pack()
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=0)

        Label(form, text="Add Initial Loan", font=self.tk_font_bold).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        Label(form, text="Principal Amount:").grid(row=1, column=0, sticky="e", padx=5)
        self.principal_amount_var = StringVar()

        principal_frame = Frame(form)
        principal_frame.grid(row=1, column=1, sticky="ew")
        Label(principal_frame, text="R").pack(side="left", padx=5)
        Entry(principal_frame, textvariable=self.principal_amount_var).pack(
            fill="x", pady=2
        )

        Label(form, text="Name:").grid(row=2, column=0, sticky="w", padx=5)

        self.name_var = StringVar()
        Entry(form, textvariable=self.name_var).grid(
            row=2, column=1, pady=2, sticky="ew"
        )

        Label(form, text="Description:").grid(row=3, column=0, sticky="w", padx=5)

        self.description_var = StringVar()
        Entry(form, textvariable=self.description_var).grid(
            row=3, column=1, pady=2, sticky="ew"
        )

        Button(form, text="Add Loan", command=self.add_initial_loan).grid(
            row=4, column=0, columnspan=2, pady=10
        )

    def add_initial_loan(self):
        try:
            # loan_id = int(self.initial_loan_id_var.get())
            name = self.name_var.get()
            principal_amount = float(self.principal_amount_var.get())
            description = self.description_var.get()
            date = datetime.now()

            add_loan(name, date, principal_amount, description)

            # conn = sqlite3.connect(DB_PATH)
            # cursor = conn.cursor()
            # cursor.execute(
            #     """
            # INSERT INTO transactions (id, date, amount, type, description)
            # VALUES (?, ?, ?, ?, ?)
            # """,
            #     (
            #         loan_id,
            #         date.strftime("%Y-%m-%d %H:%M:%S"),
            #         principal_amount,
            #         "loan",
            #         description,
            #     ),
            # )
            # conn.commit()
            # conn.close()

            messagebox.showinfo("Success", "Initial loan added successfully!")
            self.refresh_transactions_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add initial loan: {e}")

    def create_payment_form(self, master):
        form = Frame(master)
        form.pack(fill="x")
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=0)

        Label(form, text="Add Payment Transaction", font=self.tk_font_bold).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        Label(form, text="Loan ID:").grid(row=1, column=0, sticky="w", padx=5)
        self.loan_id_var = StringVar()
        Entry(form, textvariable=self.loan_id_var).grid(row=1, column=1, sticky="ew")

        Label(form, text="Amount:").grid(row=2, column=0, sticky="w", padx=5)
        self.amount_var = StringVar()

        amount_frame = Frame(form)
        amount_frame.grid(row=2, column=1, sticky="ew")
        Label(amount_frame, text="R").pack(side="left", padx=5)
        Entry(amount_frame, textvariable=self.amount_var).pack(fill="x", pady=2)

        Button(form, text="Add Payment", command=self.add_payment).grid(
            row=8, column=0, columnspan=2, pady=10
        )

    def add_payment(self):
        try:
            loan_id = int(self.loan_id_var.get())
            amount = float(self.amount_var.get())
            date = datetime.now()
            add_transaction(loan_id, date, amount, "payment")
            messagebox.showinfo("Success", "Payment transaction added successfully!")
            self.refresh_transactions_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add payment: {e}")

    def create_interest_form(self, master):
        form = Frame(master)
        form.pack(fill="x")
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=0)

        Label(form, text="Calculate Interest", font=self.tk_font_bold).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        Label(form, text="Loan ID:").grid(row=1, column=0, sticky="w", padx=5)
        self.interest_loan_id_var = StringVar()
        Entry(form, textvariable=self.interest_loan_id_var).grid(
            row=1, column=1, sticky="ew"
        )

        Label(form, text="Rate:").grid(row=3, column=0, sticky="w", padx=5)
        self.rate_var = StringVar()

        rate_frame = Frame(form)
        rate_frame.grid(row=3, column=1, sticky="ew")
        Label(rate_frame, text="%").pack(side="right", padx=5)
        Entry(rate_frame, textvariable=self.rate_var).pack(fill="x", pady=2)

        Button(form, text="Calculate Interest", command=self.calculate_interest).grid(
            row=4, column=0, columnspan=3, pady=10
        )

        Label(form, text="Current Month Interest:").grid(
            row=5, column=0, sticky="w", padx=5
        )
        Entry(form, state="readonly").grid(row=5, column=1, sticky="ew")

    def calculate_interest(self):
        try:
            loan_id = int(self.interest_loan_id_var.get())
            rate = float(self.rate_var.get())
            _, total_interest = calculate_interest(loan_id, rate)
            messagebox.showinfo(
                "Interest Accrued", f"Total interest accrued: {total_interest:.2f}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate interest: {e}")

    def create_transactions_table(self, master):
        form = Frame(master)
        form.pack(fill="both", expand=True)

        heading_frame = Frame(form)
        heading_frame.pack(side="top", pady=10, fill="x")
        Label(
            heading_frame, text="Transactions for Current Month", font=self.tk_font_bold
        ).pack(side="left", fill="x", pady=10)
        Button(
            heading_frame, text="Refresh", command=self.refresh_transactions_table
        ).pack(side="right", padx=10)

        self.transactions_table = Treeview(
            form,
            columns=("ID", "Date", "Amount", "Type", "Description"),
            show="headings",
        )
        self.transactions_table.heading("ID", text="ID")
        self.transactions_table.heading("Date", text="Date")
        self.transactions_table.heading("Amount", text="Amount")
        self.transactions_table.heading("Type", text="Type")
        self.transactions_table.heading("Description", text="Description")
        self.transactions_table.pack(fill="both", expand=True)

        self.refresh_transactions_table()

    def refresh_transactions_table(self):
        for row in self.transactions_table.get_children():
            self.transactions_table.delete(row)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        today = datetime.now()
        first_day_of_month = today.replace(day=1).strftime("%Y-%m-%d")
        last_day_of_month = today.strftime("%Y-%m-%d")
        cursor.execute(
            """
            SELECT id, start_date, amount, type, description
            FROM transactions
            WHERE start_date BETWEEN ? AND ?
            """,
            (first_day_of_month, last_day_of_month),
        )
        rows = cursor.fetchall()
        for row in rows:
            self.transactions_table.insert("", "end", values=row)
        conn.close()


if __name__ == "__main__":
    app = PaymentTrackerApp()
    app.mainloop()

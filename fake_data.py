import csv
import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from faker import Faker
from database import get_connection

fake = Faker("en_PH")  # Philippine-style names and addresses

# The 10 fields: (database column, heading shown in the table)
FIELDS = [
    ("full_name", "Full Name"),
    ("gender", "Gender"),
    ("birthdate", "Birthdate"),
    ("address", "Address"),
    ("city", "City"),
    ("mobile", "Mobile Number"),
    ("email", "Email"),
    ("username", "Username"),
    ("job", "Job"),
    ("company", "Company"),
]


def create_table():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fake_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT, gender TEXT, birthdate TEXT, address TEXT,
            city TEXT, mobile TEXT, email TEXT, username TEXT,
            job TEXT, company TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def generate_record():
    gender = random.choice(["Male", "Female"])
    name = fake.name_male() if gender == "Male" else fake.name_female()
    return (
        name,
        gender,
        fake.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
        fake.address().replace("\n", ", "),
        fake.city(),
        "09" + "".join(random.choices("0123456789", k=9)),
        fake.email(),
        fake.user_name(),
        fake.job(),
        fake.company(),
    )


def save_records(records):
    cols = ", ".join(col for col, _ in FIELDS)
    marks = ", ".join("?" for _ in FIELDS)
    conn = get_connection()
    conn.executemany(f"INSERT INTO fake_records ({cols}) VALUES ({marks})", records)
    conn.commit()
    conn.close()


def load_records():
    cols = ", ".join(col for col, _ in FIELDS)
    conn = get_connection()
    rows = conn.execute(f"SELECT id, {cols} FROM fake_records ORDER BY id DESC").fetchall()
    conn.close()
    return rows


def delete_all():
    conn = get_connection()
    conn.execute("DELETE FROM fake_records")
    conn.commit()
    conn.close()


class FakeDataTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        create_table()

        # --- Controls ---
        controls = ttk.Frame(self)
        controls.pack(fill="x")

        ttk.Label(controls, text="Number of records (min 10):").pack(side="left")
        self.count = tk.IntVar(value=10)
        ttk.Spinbox(controls, from_=10, to=500, textvariable=self.count, width=6).pack(side="left", padx=5)

        ttk.Button(controls, text="Generate & Save", command=self.generate).pack(side="left", padx=5)
        ttk.Button(controls, text="Export CSV", command=self.export_csv).pack(side="left", padx=5)
        ttk.Button(controls, text="Clear All", command=self.clear).pack(side="left", padx=5)

        self.status = ttk.Label(self, text="")
        self.status.pack(anchor="w", pady=(8, 4))

        # --- Table ---
        table_frame = ttk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        columns = ["id"] + [col for col, _ in FIELDS]
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=40, anchor="center")
        for col, heading in FIELDS:
            self.tree.heading(col, text=heading)
            self.tree.column(col, width=140)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        x_scroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=y_scroll.set, xscrollcommand=x_scroll.set)

        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        rows = load_records()
        for row in rows:
            self.tree.insert("", "end", values=row)
        self.status.config(text=f"Total saved records: {len(rows)}")

    def generate(self):
        try:
            n = int(self.count.get())
        except (tk.TclError, ValueError):
            messagebox.showerror("Error", "Please enter a valid number.")
            return
        if n < 10:
            messagebox.showwarning("Minimum", "Please generate at least 10 records.")
            return
        save_records([generate_record() for _ in range(n)])
        self.refresh()
        messagebox.showinfo("Done", f"{n} records generated and saved to the database.")

    def export_csv(self):
        rows = load_records()
        if not rows:
            messagebox.showwarning("Nothing to export", "Generate some records first.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV file", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID"] + [heading for _, heading in FIELDS])
            writer.writerows(rows)
        messagebox.showinfo("Exported", f"Saved to {path}")

    def clear(self):
        if messagebox.askyesno("Confirm", "Delete all saved records?"):
            delete_all()
            self.refresh()
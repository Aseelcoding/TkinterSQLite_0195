import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


DATABASE_NAME = "prediksi_diabetes.db"


def initialize_database():
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS pasien (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_pasien TEXT NOT NULL,
                usia INTEGER NOT NULL,
                gula_darah REAL NOT NULL,
                bmi REAL NOT NULL,
                riwayat_ortu TEXT NOT NULL,
                hasil_prediksi TEXT NOT NULL
            )
            """
        )


def validate_patient_input(nama, usia, gula_darah, bmi):
    if not nama.strip():
        messagebox.showerror("Invalid Input", "Please enter the patient's name.")
        return False

    try:
        age_value = int(usia)
        sugar_value = float(gula_darah)
        bmi_value = float(bmi)
    except ValueError:
        messagebox.showerror(
            "Invalid Input",
            "Age must be a whole number. Blood sugar and BMI must be numbers."
        )
        return False

    if age_value <= 0 or sugar_value <= 0 or bmi_value <= 0:
        messagebox.showerror("Invalid Input", "Age, blood sugar, and BMI must be greater than zero.")
        return False

    return True


def predict_risk(usia, gula_darah, bmi, riwayat_ortu):
    risk_score = 0

    if gula_darah >= 126:
        risk_score += 2
    elif gula_darah >= 100:
        risk_score += 1

    if bmi >= 30:
        risk_score += 1

    if usia >= 45:
        risk_score += 1

    if riwayat_ortu == "Yes":
        risk_score += 1

    if risk_score >= 3:
        return "Higher estimated risk"
    if risk_score >= 1:
        return "Moderate estimated risk"
    return "Lower estimated risk"


def save_patient(nama, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi):
    with sqlite3.connect(DATABASE_NAME) as connection:
        connection.execute(
            """
            INSERT INTO pasien (
                nama_pasien, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (nama, usia, gula_darah, bmi, riwayat_ortu, hasil_prediksi)
        )


def get_patient_records():
    with sqlite3.connect(DATABASE_NAME) as connection:
        return connection.execute(
            """
            SELECT id, nama_pasien, usia, gula_darah, bmi,
                   riwayat_ortu, hasil_prediksi
            FROM pasien
            ORDER BY id DESC
            """
        ).fetchall()


def show_patient_records():
    records_window = tk.Toplevel()
    records_window.title("Patient Records")
    records_window.geometry("900x350")

    columns = ("id", "nama", "usia", "gula", "bmi", "riwayat", "hasil")
    records_table = ttk.Treeview(
        records_window,
        columns=columns,
        show="headings"
    )

    headings = {
        "id": "ID",
        "nama": "Patient Name",
        "usia": "Age",
        "gula": "Blood Sugar",
        "bmi": "BMI",
        "riwayat": "Family History",
        "hasil": "Estimated Risk"
    }

    for column, heading in headings.items():
        records_table.heading(column, text=heading)

    records_table.column("id", width=45, anchor="center")
    records_table.column("nama", width=160)
    records_table.column("usia", width=60, anchor="center")
    records_table.column("gula", width=100, anchor="center")
    records_table.column("bmi", width=70, anchor="center")
    records_table.column("riwayat", width=110, anchor="center")
    records_table.column("hasil", width=220)

    scrollbar = ttk.Scrollbar(
        records_window,
        orient="vertical",
        command=records_table.yview
    )
    records_table.configure(yscrollcommand=scrollbar.set)
    records_table.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
    scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)

    try:
        records = get_patient_records()
    except sqlite3.Error as error:
        messagebox.showerror("Database Error", str(error), parent=records_window)
        records_window.destroy()
        return

    for record in records:
        records_table.insert("", "end", values=record)

    if not records:
        messagebox.showinfo(
            "Patient Records",
            "No patient records have been saved yet.",
            parent=records_window
        )


def main():
    initialize_database()

    root = tk.Tk()
    root.title("Diabetes Risk Prediction")
    root.geometry("500x520")
    root.resizable(False, False)

    title_label = tk.Label(
        root,
        text="Diabetes Risk Prediction",
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=15)

    form_frame = tk.Frame(root)
    form_frame.pack(pady=5)

    tk.Label(form_frame, text="Patient Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    nama_entry = tk.Entry(form_frame, width=30)
    nama_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Age:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    usia_entry = tk.Entry(form_frame, width=30)
    usia_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Blood Sugar (mg/dL):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
    gula_darah_entry = tk.Entry(form_frame, width=30)
    gula_darah_entry.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="BMI:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
    bmi_entry = tk.Entry(form_frame, width=30)
    bmi_entry.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(form_frame, text="Family History:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
    riwayat_ortu_var = tk.StringVar(value="No")
    riwayat_ortu_menu = tk.OptionMenu(form_frame, riwayat_ortu_var, "No", "Yes")
    riwayat_ortu_menu.config(width=25)
    riwayat_ortu_menu.grid(row=4, column=1, padx=5, pady=5)

    def handle_save():
        nama = nama_entry.get().strip()
        usia = usia_entry.get().strip()
        gula_darah = gula_darah_entry.get().strip()
        bmi = bmi_entry.get().strip()
        riwayat_ortu = riwayat_ortu_var.get()

        if not validate_patient_input(nama, usia, gula_darah, bmi):
            return

        age_value = int(usia)
        sugar_value = float(gula_darah)
        bmi_value = float(bmi)
        hasil_prediksi = predict_risk(age_value, sugar_value, bmi_value, riwayat_ortu)

        try:
            save_patient(nama, age_value, sugar_value, bmi_value, riwayat_ortu, hasil_prediksi)
        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))
            return

        messagebox.showinfo(
            "Estimated Result",
            hasil_prediksi + "\n\nThis is an educational estimate, not a medical diagnosis."
        )

    save_button = tk.Button(root, text="Save Patient and Estimate Risk", command=handle_save, width=28)
    save_button.pack(pady=10)

    records_button = tk.Button(
        root,
        text="View Patient Records",
        command=show_patient_records,
        width=28
    )
    records_button.pack(pady=5)

    note_label = tk.Label(
        root,
        text="Educational estimate only; not a medical diagnosis.",
        font=("Arial", 8),
        fg="gray"
    )
    note_label.pack(pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()

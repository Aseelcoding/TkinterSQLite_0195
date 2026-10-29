import sqlite3
import tkinter as tk
from tkinter import messagebox


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


def main():
    initialize_database()

    root = tk.Tk()
    root.title("Diabetes Risk Prediction")
    root.geometry("500x450")
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

    tk.Label(form_frame, text="Blood Sugar:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
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

    root.mainloop()


if __name__ == "__main__":
    main()

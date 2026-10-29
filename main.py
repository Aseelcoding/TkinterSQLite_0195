import sqlite3
import tkinter as tk


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


def main():
    initialize_database()

    root = tk.Tk()
    root.title("Diabetes Risk Prediction")
    root.geometry("500x350")
    root.resizable(False, False)

    title_label = tk.Label(
        root,
        text="Diabetes Risk Prediction",
        font=("Arial", 16, "bold")
    )
    title_label.pack(pady=30)

    info_label = tk.Label(
        root,
        text="Enter patient information to estimate diabetes risk.",
        font=("Arial", 10)
    )
    info_label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()

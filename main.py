import tkinter as tk


def main():
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

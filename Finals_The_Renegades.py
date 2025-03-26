import tkinter as tk
from tkinter import messagebox
import os

# File for Data Persistence
DATA_FILE = "records.txt"

def initialize_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as file:
            file.write("ID,First Name,Middle Name,Last Name,Birthday,Gender\n")

def save_to_file(record):
    with open(DATA_FILE, "a") as file:
        file.write(",".join(record) + "\n")

def load_records():
    with open(DATA_FILE, "r") as file:
        return file.readlines()[1:]

def sign_up():
    def save_record():
        try:
            first_name = entry_first_name.get()
            middle_name = entry_middle_name.get()
            last_name = entry_last_name.get()
            birthday = entry_birthday.get()
            gender = gender_var.get()

            if not (first_name and last_name and birthday and gender):
                raise ValueError("All fields except Middle Name are required!")

            records = load_records()

            # Check for duplicate records
            for record in records:
                fields = record.strip().split(",")
                if (
                    first_name.lower() == fields[1].lower() and
                    last_name.lower() == fields[3].lower() and
                    birthday == fields[4] and
                    gender.lower() == fields[5].lower()
                ):
                    messagebox.showerror("Duplicate Record", "This record already exists!")
                    return

            new_id = len(records) + 1
            record = [str(new_id), first_name, middle_name, last_name, birthday, gender]
            save_to_file(record)

            messagebox.showinfo("Success", "Record saved successfully!")
            signup_window.destroy()
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    tk.Label(signup_window, text="First Name:").grid(row=0, column=0, padx=10, pady=5)
    entry_first_name = tk.Entry(signup_window)
    entry_first_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(signup_window, text="Middle Name:").grid(row=1, column=0, padx=10, pady=5)
    entry_middle_name = tk.Entry(signup_window)
    entry_middle_name.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(signup_window, text="Last Name:").grid(row=2, column=0, padx=10, pady=5)
    entry_last_name = tk.Entry(signup_window)
    entry_last_name.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(signup_window, text="Birthday (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
    entry_birthday = tk.Entry(signup_window)
    entry_birthday.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(signup_window, text="Gender:").grid(row=4, column=0, padx=10, pady=5)
    gender_var = tk.StringVar()
    tk.Radiobutton(signup_window, text="Male", variable=gender_var, value="Male").grid(row=4, column=1)
    tk.Radiobutton(signup_window, text="Female", variable=gender_var, value="Female").grid(row=5, column=1)

    tk.Button(signup_window, text="Save", command=save_record).grid(row=6, column=0, columnspan=2, pady=10)

def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("All Records")

    # Set a monospaced font for better alignment
    header_font = ("Courier", 10, "bold")
    record_font = ("Courier", 10)

    # Header for records
    tk.Label(records_window, text="ID   First Name   Middle Name   Last Name     Birthday     Gender", font=header_font).pack()
    tk.Label(records_window, text="-" * 70, font=record_font).pack()

    records = load_records()
    for record in records:
        fields = record.strip().split(",")
        formatted_record = f"{fields[0]:<5} {fields[1]:<12} {fields[2]:<13} {fields[3]:<12} {fields[4]:<12} {fields[5]:<6}"
        tk.Label(records_window, text=formatted_record, font=record_font).pack()

def search_record():
    def search():
        try:
            last_name = entry_last_name.get()
            if not last_name:
                raise ValueError("Last Name is required to search!")

            records = load_records()
            result_text.delete("1.0", tk.END)

            found = False
            for record in records:
                if last_name.lower() in record.split(",")[3].lower():
                    fields = record.strip().split(",")
                    formatted_record = f"ID: {fields[0]}\nFirst Name: {fields[1]}\nMiddle Name: {fields[2]}\nLast Name: {fields[3]}\nBirthday: {fields[4]}\nGender: {fields[5]}\n"
                    result_text.insert(tk.END, formatted_record + "\n")
                    found = True

            if not found:
                result_text.insert(tk.END, "No records found.")
        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))

    search_window = tk.Toplevel(root)
    search_window.title("Search Record")

    tk.Label(search_window, text="Last Name:").grid(row=0, column=0, padx=10, pady=5)
    entry_last_name = tk.Entry(search_window)
    entry_last_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(search_window, text="Search", command=search).grid(row=1, column=0, columnspan=2, pady=10)

    result_text = tk.Text(search_window, height=10, width=50)
    result_text.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

def remove_record():
    def delete_record():
        try:
            record_id = entry_record_id.get()
            if not record_id.isdigit():
                raise ValueError("Please enter a valid numeric ID.")
            
            record_id = int(record_id)
            records = load_records()
            remaining_records = []
            record_found = False

            for record in records:
                fields = record.strip().split(",")
                if int(fields[0]) == record_id:
                    record_found = True
                else:
                    remaining_records.append(record)

            if not record_found:
                raise ValueError(f"No record found with ID: {record_id}")

            # Overwrite the file with the updated records
            with open(DATA_FILE, "w") as file:
                file.write("ID,First Name,Middle Name,Last Name,Birthday,Gender\n")
                for record in remaining_records:
                    file.write(record)

            messagebox.showinfo("Success", f"Record with ID {record_id} removed successfully!")
            remove_window.destroy()

        except ValueError as ve:
            messagebox.showerror("Input Error", str(ve))

    # Create a new window for removing records
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove Record")

    tk.Label(remove_window, text="Enter the ID of the record to remove:").grid(row=0, column=0, padx=10, pady=5)
    entry_record_id = tk.Entry(remove_window)
    entry_record_id.grid(row=0, column=1, padx=10, pady=5)

    tk.Button(remove_window, text="Delete", command=delete_record).grid(row=1, column=0, columnspan=2, pady=10)
    
# GUI Setup
initialize_file()

root = tk.Tk()
root.title("User Management System")
root.geometry("400x400")  # Increased size of JFrame

tk.Label(root, text="Choose an Operation", font=("Arial", 14)).pack(pady=10)

btn_sign_up = tk.Button(root, text="Sign Up", command=sign_up, width=20)
btn_sign_up.pack(pady=5)

btn_view_records = tk.Button(root, text="View All Records", command=view_records, width=20)
btn_view_records.pack(pady=5)

btn_search_record = tk.Button(root, text="Search Record", command=search_record, width=20)
btn_search_record.pack(pady=5)

btn_remove_record = tk.Button(root, text="Remove Record", command=remove_record, width=20)
btn_remove_record.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=root.quit, width=20)
btn_exit.pack(pady=5)

root.mainloop()

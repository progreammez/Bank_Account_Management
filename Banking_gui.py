import tkinter as tk
from tkinter import messagebox
import json, hashlib, os

# ---------- Bank Data Handling ----------
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def load_accounts():
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            return json.load(f).get("accounts", [])
    return []

def save_accounts():
    with open("accounts.json", "w") as f:
        json.dump({"accounts": accounts}, f, indent=4)

accounts = load_accounts()

# ---------- GUI Logic ----------
def login():
    username = user_entry.get()
    password = pass_entry.get()
    role = role_var.get()

    if role == 1:  # User
        hashed_password = hash_password(password)

        # Search for user in accounts.json
        for acc in accounts:
            if acc["name"] == username and acc["password"] == hashed_password:
                messagebox.showinfo("Login Successful", f"Welcome {username}!")
                open_user_dashboard(acc)
                return

        messagebox.showerror("Login Failed", "Invalid username or password!")

    elif role == 2:  # Admin placeholder
        messagebox.showinfo("Login", "Admin login not implemented yet!")

    else:
        messagebox.showwarning("Error", "Please select User or Admin!")

def open_user_dashboard(account):
    dash = tk.Toplevel(root)
    dash.title(f"User Dashboard - {account['name']}")
    dash.geometry("500x600")

    # Display basic info
    balance_var = tk.StringVar()
    balance_var.set(f"Balance: ₹{account['account_balance']}")

    tk.Label(dash, text=f"Welcome, {account['name']}!", font=("Arial", 16)).pack(pady=10)
    tk.Label(dash, text=f"Account No: {account['account_number']}").pack()
    tk.Label(dash, textvariable=balance_var).pack(pady=5)

    # --- Withdraw Function ---
    def withdraw():
        try:
            amt = int(withdraw_entry.get())
            if amt <= 0:
                raise ValueError
            if account['account_balance'] >= amt:
                account['account_balance'] -= amt
                balance_var.set(f"Balance: ₹{account['account_balance']}")
                save_accounts()
                messagebox.showinfo("Success", f"₹{amt} withdrawn!")
            else:
                messagebox.showerror("Error", "Insufficient balance!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount!")

    # --- Deposit Function ---
    def deposit():
        try:
            amt = int(deposit_entry.get())
            if amt <= 0:
                raise ValueError
            account['account_balance'] += amt
            balance_var.set(f"Balance: ₹{account['account_balance']}")
            save_accounts()
            messagebox.showinfo("Success", f"₹{amt} deposited!")
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount!")

    import random

    # ------------------ Transfer Section ------------------

    tk.Label(dash, text="Transfer To (Account No)").pack(pady=5)
    transfer_acc_entry = tk.Entry(dash)
    transfer_acc_entry.pack()

    tk.Label(dash, text="Amount to Transfer").pack(pady=5)
    transfer_amt_entry = tk.Entry(dash)
    transfer_amt_entry.pack()

    def send_otp_and_transfer():
        try:
            target_acc = transfer_acc_entry.get().strip()
            amount = int(transfer_amt_entry.get())

            if amount <= 0:
                raise ValueError("Invalid amount!")

            if account['account_balance'] < amount:
                messagebox.showerror("Error", "Insufficient balance!")
                return

            # Find target account
            target = next((acc for acc in accounts if str(acc["account_number"]) == target_acc), None)
            if not target:
                messagebox.showerror("Error", "Target account not found!")
                return

            # Generate OTP
            otp = str(random.randint(100000, 999999))
            otp_window = tk.Toplevel(dash)
            otp_window.title("OTP Verification")

            tk.Label(otp_window, text=f"Enter OTP (for demo, it's {otp})").pack(pady=10)
            otp_entry = tk.Entry(otp_window)
            otp_entry.pack()

            def verify_otp():
                if otp_entry.get().strip() == otp:
                    # Transfer money
                    account["account_balance"] -= amount
                    target["account_balance"] += amount
                    save_accounts()
                    balance_var.set(f"Balance: ₹{account['account_balance']}")
                    messagebox.showinfo("Success", f"₹{amount} transferred to {target['name']}")
                    otp_window.destroy()
                else:
                    messagebox.showerror("Error", "Incorrect OTP!")

            tk.Button(otp_window, text="Confirm", command=verify_otp).pack(pady=10)

        except ValueError:
            messagebox.showerror("Error", "Enter valid amount!")

    tk.Button(dash, text="Transfer", command=send_otp_and_transfer).pack(pady=10)

    # Withdraw UI
    tk.Label(dash, text="Withdraw Amount").pack(pady=5)
    withdraw_entry = tk.Entry(dash)
    withdraw_entry.pack()
    tk.Button(dash, text="Withdraw", command=withdraw).pack(pady=5)

    # Deposit UI
    tk.Label(dash, text="Deposit Amount").pack(pady=5)
    deposit_entry = tk.Entry(dash)
    deposit_entry.pack()
    tk.Button(dash, text="Deposit", command=deposit).pack(pady=5)

    # Logout
    tk.Button(dash, text="Logout", command=dash.destroy).pack(pady=20)

# ---------- Tkinter Window ----------
root = tk.Tk()
root.title("Bank Management System")
root.geometry("400x350")

tk.Label(root, text="Login to Bank", font=("Arial", 16)).pack(pady=10)

role_var = tk.IntVar()
tk.Radiobutton(root, text="User", variable=role_var, value=1).pack()
tk.Radiobutton(root, text="Admin", variable=role_var, value=2).pack()

tk.Label(root, text="Username").pack()
user_entry = tk.Entry(root)
user_entry.pack()

tk.Label(root, text="Password").pack()
pass_entry = tk.Entry(root, show="*")
pass_entry.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()

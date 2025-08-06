import json
import os
import time
from datetime import datetime
import random

# ----- Global Account Number Counter -----
next_account_number = 1000000

def generate_account_number():
    global next_account_number
    acc_no = next_account_number
    next_account_number += 1
    return acc_no

def generate_otp():
    return random.randint(1000000, 9999999)

# ----- Bank Account Class -----
class BankAccount:
    def __init__(self, name, password, balance, account_type="Savings"):
        self.name = name
        self.password = password
        self.account_number = generate_account_number()
        self.account_balance = balance
        self.account_type = account_type
        self.failed_attempts = 0
        self.is_locked = False
        self.transactions = []  

    def display(self):
        print(f"\nName: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: ₹{self.account_balance}")
        print(f"Account Type: {self.account_type}")
        print(f"Status: {'Locked' if self.is_locked else 'Active'}\n")

    def log_transaction(self, txn_type, amount, note=""):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append({
            "type": txn_type,
            "amount": amount,
            "note": note,
            "time": timestamp
        })

    def deposit(self, deposit):
        self.account_balance += deposit
        self.log_transaction("Deposit", deposit)
        print("Money deposited successfully.")

    def withdraw(self, withdrawal):
        # Restrict FD account withdrawals
        if self.account_type == "Fixed Deposit":
            print("Withdrawals are not allowed for Fixed Deposit accounts!")
            return

        if self.account_balance >= withdrawal:
            # OTP for large withdrawals
            if withdrawal >= 10000:
                otp = generate_otp()
                print(f"OTP for withdrawal: {otp}")  # simulate sending OTP

                for attempt in range(3):
                    user_otp = int(input("Enter OTP to confirm withdrawal: "))
                    if user_otp == otp:
                        self.account_balance -= withdrawal
                        self.log_transaction("Withdrawal", withdrawal)
                        print("Money withdrawn successfully.")
                        break
                    else:
                        print(f"Incorrect OTP! Attempts left: {2 - attempt}")
                else:
                    print("Withdrawal cancelled due to incorrect OTP attempts.")
                    return
            else:
                self.account_balance -= withdrawal
                self.log_transaction("Withdrawal", withdrawal)
                print("Money withdrawn successfully.")
        else:
            print("Insufficient balance.")

    def to_dict(self):
        return {
            "name": self.name,
            "password": self.password,
            "account_number": self.account_number,
            "account_balance": self.account_balance,
            "account_type": self.account_type,
            "failed_attempts": self.failed_attempts,
            "is_locked": self.is_locked,
            "transactions": self.transactions
        }

    @classmethod
    def from_dict(cls, data):
        acc = cls.__new__(cls)  
        acc.name = data["name"]
        acc.password = data["password"]
        acc.account_number = data["account_number"]
        acc.account_balance = data["account_balance"]
        acc.account_type = data["account_type"]
        acc.failed_attempts = data["failed_attempts"]
        acc.is_locked = data["is_locked"]
        acc.transactions = data["transactions"]
        return acc

# ----- JSON Save/Load -----
def save_accounts(accounts, next_acc_num):
    data = {
        "next_account_number": next_acc_num,
        "accounts": [acc.to_dict() for acc in accounts]
    }
    with open("accounts.json", "w") as f:
        json.dump(data, f, indent=4)

def load_accounts():
    global next_account_number
    if os.path.exists("accounts.json"):
        with open("accounts.json", "r") as f:
            data = json.load(f)
            next_account_number = data.get("next_account_number", 1000000)
            return [BankAccount.from_dict(acc) for acc in data.get("accounts", [])]
    return []

# Load accounts at start
accounts = load_accounts()
logged_in_user = None

# Admin credentials
ADMIN_USER = "admin"
ADMIN_PASS = "1234"

print("WELCOME TO BANK")
time.sleep(1)
print("Loading system...")
time.sleep(1)
print("System loaded successfully!\n")

while True:
    print("\nLogin as:\n 1. User\n 2. Admin\n 3. Exit")
    role_choice = int(input("Enter choice: "))

    # ---------- USER MODE ----------
    if role_choice == 1:
        while True:
            choice = int(input("\nUser Menu:\n 1. Create Account\n 2. Login\n 3. Exit User Menu\n"))

            if choice == 1:
                name = input("Enter your name: ")
                password = input("Set a password: ")
                balance = int(input("Enter initial balance: "))

                print("\nSelect Account Type:\n 1. Savings\n 2. Current\n 3. Fixed Deposit (FD)")
                acc_type_choice = int(input("Enter choice: "))
                if acc_type_choice == 1:
                    account_type = "Savings"
                elif acc_type_choice == 2:
                    account_type = "Current"
                elif acc_type_choice == 3:
                    account_type = "Fixed Deposit"
                else:
                    print("Invalid choice! Defaulting to Savings.")
                    account_type = "Savings"

                if name and balance >= 0:
                    acc = BankAccount(name, password, balance, account_type)
                    accounts.append(acc)
                    print(f"Account created successfully! Your account number is {acc.account_number}")
                else:
                    print("Invalid details. Try again.")

            elif choice == 2:
                name = input("Enter your account name: ")
                password = input("Enter your password: ")

                for acc in accounts:
                    if acc.name == name:
                        if acc.is_locked:
                            print("Account is locked due to multiple failed attempts. Contact admin.")
                            break

                        if acc.password == password:
                            acc.failed_attempts = 0  # reset on success

                            # OTP Verification for login
                            otp = generate_otp()
                            print(f"Your OTP is: {otp}")  # simulate sending OTP

                            for attempt in range(3):
                                user_otp = int(input("Enter OTP: "))
                                if user_otp == otp:
                                    logged_in_user = acc
                                    print(f"Welcome {name}, login successful!")
                                    break
                                else:
                                    print(f"Incorrect OTP! Attempts left: {2 - attempt}")
                            else:
                                print("Too many incorrect OTP attempts. Login failed.")
                                break
                            
                            # ---- User Logged In Menu ----
                            while logged_in_user:
                                user_action = int(input(
                                    "\n1. Withdraw\n2. Deposit\n3. View Details\n4. Transfer Money\n5. View Transaction History\n6. Logout\n"
                                ))

                                if user_action == 1:
                                    amt = int(input("Enter amount to withdraw: "))
                                    logged_in_user.withdraw(amt)

                                elif user_action == 2:
                                    amt = int(input("Enter amount to deposit: "))
                                    logged_in_user.deposit(amt)

                                elif user_action == 3:
                                    logged_in_user.display()

                                elif user_action == 4:
                                    if logged_in_user.account_type == "Fixed Deposit":
                                        print("Transfers are not allowed from Fixed Deposit accounts!")
                                        continue

                                    receiver_acc_number = int(input("Enter recipient account number: "))
                                    amount = int(input("Enter amount to transfer: "))

                                    # Find recipient
                                    receiver = None
                                    for acc_r in accounts:
                                        if acc_r.account_number == receiver_acc_number:
                                            receiver = acc_r
                                            break

                                    if receiver is None:
                                        print("Recipient account not found.")
                                        continue

                                    if receiver.account_number == logged_in_user.account_number:
                                        print("You cannot transfer money to your own account.")
                                        continue

                                    if logged_in_user.account_balance < amount:
                                        print("Insufficient balance for this transfer.")
                                        continue

                                    # 🔹 Always require OTP for transfer
                                    otp = generate_otp()
                                    print(f"OTP for transfer: {otp}")  # simulate sending OTP
                                    
                                    for attempt in range(3):
                                        user_otp = int(input("Enter OTP to confirm transfer: "))
                                        if user_otp == otp:
                                            break
                                        else:
                                            print(f"Incorrect OTP! Attempts left: {2 - attempt}")
                                    else:
                                        print("Transfer cancelled due to incorrect OTP attempts.")
                                        continue

                                    # Perform transfer
                                    logged_in_user.account_balance -= amount
                                    receiver.account_balance += amount

                                    # Log transactions
                                    logged_in_user.log_transaction("Transfer Out", amount, f"To {receiver.account_number}")
                                    receiver.log_transaction("Transfer In", amount, f"From {logged_in_user.account_number}")

                                    print(f"₹{amount} transferred successfully to {receiver.name} (Acc: {receiver.account_number})")

                                elif user_action == 5:
                                    if not logged_in_user.transactions:
                                        print("No transactions yet.")
                                    else:
                                        print("\n--- Transaction History (Last 10) ---")
                                        for txn in logged_in_user.transactions[-10:]:
                                            print(f"[{txn['time']}] {txn['type']} ₹{txn['amount']} {txn['note']}")

                                elif user_action == 6:
                                    print("Logging out...")
                                    logged_in_user = None
                                    break

                        else:
                            acc.failed_attempts += 1
                            print(f"Incorrect password! Attempts left: {3 - acc.failed_attempts}")
                            if acc.failed_attempts >= 3:
                                acc.is_locked = True
                                print("Account locked due to 3 failed attempts!")
                        break
                else:
                    print("Account not found.")
                    continue

            elif choice == 3:
                print("Exiting user menu...")
                time.sleep(1)
                break

    # ---------- ADMIN MODE ----------
    elif role_choice == 2:
        username = input("Admin Username: ")
        password = input("Admin Password: ")

        if username == ADMIN_USER and password == ADMIN_PASS:
            print("Admin login successful!")
            while True:
                admin_choice = int(input(
                    "\nAdmin Menu:\n 1. View All Accounts\n 2. Delete Account\n 3. Total Bank Balance\n 4. Unlock Account\n 5. Logout\n"
                ))

                if admin_choice == 1:
                    if not accounts:
                        print("No accounts exist.")
                    else:
                        print("\n--- All Bank Accounts ---")
                        for acc in accounts:
                            acc.display()

                elif admin_choice == 2:
                    acc_number = int(input("Enter account number to delete: "))
                    for acc in accounts:
                        if acc.account_number == acc_number:
                            accounts.remove(acc)
                            print("Account deleted successfully!")
                            break
                    else:
                        print("Account not found.")

                elif admin_choice == 3:
                    total_balance = sum(acc.account_balance for acc in accounts)
                    print(f"Total Bank Balance: ₹{total_balance}")

                elif admin_choice == 4:
                    acc_number = int(input("Enter account number to unlock: "))
                    for acc in accounts:
                        if acc.account_number == acc_number:
                            if acc.is_locked:
                                acc.is_locked = False
                                acc.failed_attempts = 0
                                print("Account unlocked successfully!")
                            else:
                                print("This account is already active.")
                            break
                    else:
                        print("Account not found.")

                elif admin_choice == 5:
                    print("Logging out...")
                    time.sleep(1)
                    break
        else:
            print("Invalid admin credentials.")

    # ---------- EXIT ----------
    else:
        save_accounts(accounts, next_account_number)
        print("Exiting the bank system. Accounts saved. Goodbye!")
        time.sleep(1)
        break

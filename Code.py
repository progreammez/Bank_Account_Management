import random
import time

class BankAccount:
    def __init__(self, name, password, balance):
        self.name = name
        self.password = password
        self.account_number = random.randint(1000000, 9999999)
        self.account_balance = balance

    def display(self):
        print(f"\nName: {self.name}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: {self.account_balance}\n")
    
    def withdraw(self, withdrawl):
        if self.account_balance >= withdrawl:
            self.account_balance -= withdrawl
            print("Money withdrawn successfully.")
        else:
            print("Insufficient balance.")
    
    def deposit(self, deposit):
        self.account_balance += deposit
        print("Money deposited successfully.")


# ----- Bank System -----
accounts = []  
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
                if name and balance >= 0:
                    acc = BankAccount(name, password, balance)
                    accounts.append(acc)
                    print(f"Account created successfully! Your account number is {acc.account_number}")
                else:
                    print("Invalid details. Try again.")

            elif choice == 2:
                name = input("Enter your account name: ")
                password = input("Enter your password: ")

                # Check if account exists
                for acc in accounts:
                    if acc.name == name and acc.password == password:
                        logged_in_user = acc
                        print(f"Welcome {name}, login successful!")
                        break
                else:
                    print("Invalid credentials.")
                    continue

                # User logged in menu
                while True:
                    user_action = int(input("\n1. Withdraw\n2. Deposit\n3. View Details\n4. Logout\n"))
                    
                    if user_action == 1:
                        amt = int(input("Enter amount to withdraw: "))
                        logged_in_user.withdraw(amt)
                    
                    elif user_action == 2:
                        amt = int(input("Enter amount to deposit: "))
                        logged_in_user.deposit(amt)
                    
                    elif user_action == 3:
                        logged_in_user.display()
                    
                    elif user_action == 4:
                        print("Logging out...")
                        logged_in_user = None
                        break
                    else:
                        print("Invalid choice!")

            elif choice == 3:
                print("Logging out...")
                time.sleep(1)
                break

            else:
                print("Invalid choice!")

    # ---------- ADMIN MODE ----------
    elif role_choice == 2:
        username = input("Admin Username: ")
        password = input("Admin Password: ")

        if username == ADMIN_USER and password == ADMIN_PASS:
            print("Admin login successful!")
            while True:
                admin_choice = int(input("\nAdmin Menu:\n 1. View All Accounts\n 2. Delete Account\n 3. Total Bank Balance\n 4. Logout\n"))
                
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
                    print(f"Total Bank Balance: {total_balance}")

                elif admin_choice == 4:
                    print("Logging out...")
                    time.sleep(1)
                    break
    
    else:
        print("Exiting the bank system. Goodbye")
        time.sleep(1)
        break


from datetime import datetime
import random
import csv
import json
import os

def create_account():
    print("\nCreate your account")
    name = input("Enter your name")

    if name.replace(" ","").isalpha() :
        address = input("Enter your address")

        if address.replace(" ","").isalnum():
            account_type = input("Enter account type (saving/current)").lower().strip()

            if account_type == "saving" or account_type == "current":

                amount = float(input("Enter initial deposit amount"))

                if amount > 0 : 
                    user_date = input("Enter date (dd-mm-yyyy)").strip()
                    
                    if datetime.strptime(user_date, "%d-%m-%Y"):
                        print("Details fetched sucesffuly")
                    else:
                        print("Enter a valid date in dd-mm-yyyy")
                else:
                    print("Enter amount > 0")
                    return 
                
            else :
                print("Your can choose only saving or current account")
                return 
        else:
            print("Dont use symbols or characters in Address")   
            return 
    else:
        print("Enter a valid name")
        return

    print("Account Created Successfully")
    acc_no = random.randint(100, 999)

    print("Your account number: ",acc_no)

    pin = input("Set up your 4 digit pin:")

    if pin.isdigit() and len(pin) == 4:
        print("PIN registered successfully")
    else:
        print("Enter valid PIn")
    
    


    
    user = {
            "account_no": acc_no,
            "name" : name,
            "address" : address,
            "account_type" : account_type,
            "amount" : amount,
            "pin" : pin,
            "date" : user_date,
            "transactions" : [
                {
                    "type" : "Initial Deposit",
                    "amount" : amount,
                    "time" : datetime.now().strftime("%d - %m -%y %H:%M:%S")
                }
            ]
    }

    
    

    json_file = "data.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            data = json.load(file)
    else:
        data = []

    data.append(user)

    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)


    csv_file = f"{user_date}.csv"
    file_exists = os.path.exists(csv_file)

    with open(csv_file, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Account No", "Holder Name", "Account Type", "Initial Amount"])

        writer.writerow([acc_no, name, account_type, amount])

        # print(f"User data saved in {json_file}")
        # print(f"Account summary saved in {csv_file}")

    

def verify_user():
    account_no = input("Enter your account number: ")
    pin = input("Enter your PIN: ")

    for file in os.listdir():
        if file.endswith(".json"):
            with open(file, "r") as f:
                data = json.load(f)
                for user in data:
                    if str(user["account_no"]) == account_no and user["pin"] == pin:
                        return user
    print("Invalid account number or PIN")
    return None

def deposit():
    print("_____DEPOSIT MONEY_____")
    user = verify_user()
    if user:
        amount = float(input("Enter aount to deposit"))
        
        user["amount"] = user["amount"] + amount

        update_user_data(user)

        print(f"Account Holder: {user['name']}\nCurrent Balance : {user['amount']}")

    else:
        print("Invalid User! Despoit failed")

def withdraw():
    print("\n--- Withdraw Money ---")
    user = verify_user()
    if user:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= user['amount']:
            user["amount"] = user["amount"] - amount
            update_user_data(user)
            print(f"Withdrawal successful! Remaining balance: {user['amount']}")
        else:
            print("Insufficient balance!")

def check_balance():
    print("Check Balance ")
    user = verify_user()
    if user:
        print(f"Account Holder : {user['name']}\nCurrent Balance: {user['amount']}")

def change_pin():
    print("\nChange PIN")
    user = verify_user()

    if user: 
        new_pin = input("Enter new 4 digit PIN: ")
        if len(new_pin)  ==  4 and new_pin.isdigit():
            user["pin"] = new_pin
            update_user_data(user)
            print("PIN changed successfully!!")
        else:
            print("Enter a 4 digit PIN")


def update_user_data(updated_user):
    for file in os.listdir():
        if file.endswith(".json"):
            with open(file, "r") as f:
                data = json.load(f)

            for user in data: 
                if user["account_no"] == updated_user["account_no"]:
                    user.update(updated_user)

            with open(file, "w") as f:
                json.dump(data, f, indent = 4)

    #update CSV with latest amoun and date
    csv_file = f"{updated_user['date']}.csv"
    if os.path.exists(csv_file):
        rows = []

        with open(csv_file, "r") as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if row[0] == str(updated_user["account_no"]):
                    row[3] = str(updated_user["amount"])
                rows.append(row)

            with open(csv_file, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(header)
                writer.writerows(rows)

    

def main():

    while True:
        print(" \nWELCOME TO ATM ")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdrawal")
        print("4. Check Balance")
        print("5. Change PIN")
        print("6. Exit")


        choice = input("Enter your choice")

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            change_pin()
        
        elif choice == "6":
            print("Thankyou for using ATM!")
            break

        else:

            print("Invalid choice ! Please try again")


if __name__ == "__main__":
    main()




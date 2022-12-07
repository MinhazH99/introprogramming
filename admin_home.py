from admin_accountm import admin
from admin_features import adminFeatures

def admin_home():
    print("[1] Volunteer Account Management")
    print("[2] Emergency Plan Mangement")

    while True:
        user_input = input("Please select an option: ")

        if user_input == '1':
            admin()
            break

        elif user_input == '2':
            adminFeatures()
            break

        else:
            print("Please select a valid option")


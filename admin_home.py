import admin_accountm
import admin_features
import home

def admin_home():
    print("-------------------------------------------------------------------------------") 
    print("[1] Volunteer Account Management")
    print("[2] Emergency Plan Management")
    print("[3] Logout")

    while True:
        user_input = input("Please select an option: ")

        if user_input == '1':
            admin_accountm.admin_accountm()
            break

        elif user_input == '2':
            admin_features.adminFeatures()
            break

        elif user_input == '3':
            print("Successfully logged out!")
            home.home()
            break

        else:
            print("Please select a valid option")
            user_input = input("Please select an option: ")
import csv
import pandas as pd
import volunteer_home

def volunteerEditDetails(user):
    print("-------------------------------------------------------------------------------")
    print("[1] Change Name")
    print("[2] Change Password")
    print("[3] Change Phone Number")
    print("[4] Change Email Address")
    print("[5] Return to Volunter Home Page")
    

    while True:
        user_input = input("Please select an option: ")
        if user_input == '1':
            print("-------------------------------------------------------------------------------")
            volunteerFirstName(user)
            break
        elif user_input == '2':
            print("-------------------------------------------------------------------------------")
            volunteerPassword(user)
            break
        elif user_input == '3':
            print("-------------------------------------------------------------------------------")
            volunteerPhoneNo(user)
            break
        
        elif user_input == '4':
            print("-------------------------------------------------------------------------------")
            volunteerEmailAdd(user)
            break

        elif user_input == '5':
            print("-------------------------------------------------------------------------------")
            volunteer_home.volunteer_home(user)
            break

        else:
            print("Not a valid option")

def volunteerFirstName(user):

    change_firstname = input("Please enter your new first name: ")
    change_secondname = input("Pleae enter your new family name: ")

    print(f"To confirm you would like to change your name to {change_firstname} {change_secondname}")
    
    while True:

        confirm = input("Please select Y/N: ")

        if confirm == 'Y' or confirm == 'y':
            userData = pd.read_csv("volunteers_db.csv")
            df = pd.DataFrame(userData).astype('str')
            df.loc[df["usernames"] == user,"firstname"] = change_firstname
            df.loc[df["usernames"] == user,"familyname"] = change_secondname

            df.to_csv("volunteers_db.csv",index = False)

            print(f"Name has succesfully been changed to {change_firstname} {change_secondname}")

            volunteerEditDetails(user)
            break

            
        elif confirm == 'N' or confirm =='n':
            volunteerEditDetails(user)
            break
        
        else:
            print("Please select a valid option")


def volunteerPassword(user):
    userData = pd.read_csv("volunteers_db.csv")
    df = pd.DataFrame(userData).astype('str')
    
    while True:
        old_password = input("Please enter old password: ")
    
        validate_input = (len(df[(df.usernames == user) & (df.password == old_password)]) > 0)

        if validate_input:
            new_password = input("Please enter your new password: ")
            confirm_new_pass = input("Please confirm new password: ")

            if new_password == confirm_new_pass:
                print("Password successfuly changed")
                df.loc[df["usernames"] == user,"password"] = new_password
                df.to_csv("volunteers_db.csv",index = False)
                volunteerEditDetails(user)
                break
                
            
            else:
                print("Passwords do not match. Try again")

        else:
            print("Incorrect password. Please try again")






def volunteerPhoneNo(user):

    change_phoneno = input("Please enter your new phone number: ")

    print(f"To confirm you would like to change your name to {change_phoneno}")
    
    while True:

        confirm = input("Please select Y/N: ")

        if confirm == 'Y' or confirm == 'y':
            userData = pd.read_csv("volunteers_db.csv")
            df = pd.DataFrame(userData).astype('str')
            df.loc[df["usernames"] == user,"phoneno"] = change_phoneno

            df.to_csv("volunteers_db.csv",index = False)

            #print(df.loc[df["usernames"] == user])

            print(f"Your phone number has succesfully been changed to {change_phoneno}")
            volunteerEditDetails(user)
            break

            
        elif confirm == 'N' or confirm =='n':
            volunteerEditDetails(user)
            break
        
        else:
            print("Please select a valid option")


def volunteerEmailAdd(user):
    
    while True:
        change_email = input("Please enter your new email address: ")
        userData = pd.read_csv("admin_db.csv")    
        df = pd.DataFrame(userData).astype('str')
        if df['usernames'].eq(change_email).any():
            print("Email already exist. Please enter another")
        else:
             break

    print(f"To confirm you would like to change your email to {change_email}")

    while True:

        confirm = input("Please select Y/N: ")

        if confirm == 'Y' or confirm == 'y':
            userData = pd.read_csv("volunteers_db.csv")
            df = pd.DataFrame(userData).astype('str')
            df.loc[df["usernames"] == user,"email"] = change_email

            df.to_csv("volunteers_db.csv",index = False)

            print(f"Email has succesfully been changed to {change_email}")

            volunteerEditDetails(user)
            break

            
        elif confirm == 'N' or confirm =='n':
            volunteerEditDetails(user)
            break
        
        else:
            print("Please select a valid option")


    

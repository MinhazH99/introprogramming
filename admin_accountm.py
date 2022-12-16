import pandas as pd
import admin_home
import csv
from tabulate import tabulate



def admin_accountm():
    print("[1] View Volunteer Accounts")
    print("[2] Deactivate Volunteer Accounts")
    print("[3] Reactivate Volunteer Accounts")
    print("[4] Delete Volunteer Accounts")
    print("[5] Return to home screen")

    while True:
        user_input = input("Please select an option: ")

        if user_input == '1':
            viewVolunteers()
            break

        elif user_input == '2':
            EditVolunteers(user_input)
            break

        elif user_input == '3':
            EditVolunteers(user_input)
            break

        elif user_input == '4':
            deleteVolunteers()
            break

        elif user_input =='5':
            admin_home.admin_home()

        else:
            print("Please select a valid option")
        break


def viewVolunteers():
    df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])
    print("\n")
    print(tabulate(df,headers=["usernames","status"],tablefmt='fancy_grid',showindex=False))
    print("\n")
    while True:

        askUserInput = input("Please enter # to return to home page: ")

        if askUserInput == '#':
            admin_accountm()
            break
            
    


def EditVolunteers(inp):
    showdf = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

    print(tabulate(showdf,headers=["usernames","status"],tablefmt='fancy_grid',showindex=False))
    
    userData = pd.read_csv("volunteers_db.csv")
    df = pd.DataFrame(userData).astype('str')

    usernames = []
    with open("volunteers_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                usernames.append(row[2])
    
    if inp == '2':
        
        while True:
        
            user_input = input("Please type in username which you would like to deactivate or # to return to home page: ")
            print(usernames)
            if user_input == '#':
                admin_accountm()
       
            if user_input in usernames:
                df.loc[df["usernames"] == user_input,"status"]='Deactivated'
                
                print("Account succesfully deactivated!")

                df.to_csv("volunteers_db.csv",index=False)

                df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

                print(tabulate(df,headers=["usernames","status"],tablefmt='fancy_grid',showindex=False))

                print("Would you like to deactivate another account?")

                while True:
                    user_input2 = input("Please enter [Y/N]: ")
                    if user_input2 == 'Y' or user_input2 == 'y':
                        EditVolunteers('2')
                        break
                    elif user_input2 == 'N' or user_input2 == 'n':
                        admin_accountm()
                        break

                    else:
                        print("Please enter Y or N")


                break
            else:
                print("Please enter a valid username!")

    elif inp == '3':
        while True:
            user_input = input("Please type in username which you would like to reactivate or # to return to home page: ")

            if user_input == '#':
                admin_accountm()

            if user_input in usernames:
                df.loc[df["usernames"] == user_input,"status"]='Activated'

                print("Account sucessfully activated!")

                df.to_csv("volunteers_db.csv",index=False)

                df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

                print(tabulate(df,headers=["usernames","status"],tablefmt='fancy_grid',showindex=False))
                
                print("Would you like to reactivate another account?")
                while True:
                    user_input2 = input("Please enter [Y/N]: ")
                    if user_input2 == 'Y' or user_input2 == 'y':
                        EditVolunteers('3')
                        break
                    elif user_input2 == 'N' or user_input2 == 'n':
                        admin_accountm()
                        break
                    else:
                        print("Please enter Y or N")
                break
            else:
                print("Please enter a valid username")



def deleteVolunteers():
    showdf = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

    print(tabulate(showdf,headers=["usernames","status"],tablefmt='fancy_grid',showindex=False))

    usernames = []
    with open("volunteers_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                usernames.append(row[2])
    while True:

        user_input = input("Please type in username of volunteer you would like to delete or # to return to home page: ")
        if user_input =='#':
            admin_accountm()
           
        if user_input in usernames:
            while True:
                doubleCheck = print(f"Please confirm you would like to delete {user_input} from the database?")
                doubleCheck = input("Please enter Y or N: ")
                
                if doubleCheck == 'Y' or doubleCheck =='y':
                    userData = pd.read_csv("volunteers_db.csv")
                    df = pd.DataFrame(userData).astype('str')
                    df = df.loc[df['usernames'] != user_input]

                    df.to_csv("volunteers_db.csv",index=False)

                    df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

                    print("Account succesfully deleted!")
                    print(tabulate(df,headers=["usernames","status"],tablefmt='fancy_grid',showindex=False))

                    print("Would you like to delete another account? ")

                    while True:
                        user_input2 = input("Please enter [Y/N]: ")
                        if user_input2 == 'Y' or user_input2 == 'y':
                            deleteVolunteers()
                            break
                        elif user_input2 == 'N' or user_input2 == 'n':
                            admin_accountm()
                            break
                        else:
                            print("Please enter Y or N")
                    break
                
                elif doubleCheck == 'N' or doubleCheck =='n':
                    print("Returning to home page")
                    admin_accountm()

                else:
                    print("Please select a valid option Y or N")

        else:
            print("Please enter a valid username!")






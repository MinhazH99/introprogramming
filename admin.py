import pandas as pd
import csv

def admin():
    print("[1] View Volunteer Accounts")
    print("[2] Deactivate Volunteer Accounts")
    print("[3] Reactivate Volunteer Accounts")
    print("[4] Delete Volunteer Accounts")

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

        else:
            print("Please select a valid option")


def viewVolunteers():
    df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])
    print(df)
    print("\n")
    returnToHomePage()
            
    


def EditVolunteers(inp):
    showdf = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

    print(showdf)
    
    df = pd.read_csv("volunteers_db.csv")

    usernames = []
    with open("volunteers_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                usernames.append(row[0])
    
    if inp == '2':
        
        while True:
        
            user_input = input("Please type in username which you would like to deactivate: ")
       
            if user_input in usernames:
                df.loc[df["usernames"] == user_input,"status"]='Deactivated'
                print("Account succesfully deactivated!")
                break
            else:
                print("Please enter a valid username!")

    elif inp == '3':
        while True:
            user_input = input("Please type in username which you would like to reactivate: ")

            if user_input in usernames:
                df.loc[df["usernames"] == user_input,"status"]='Activated'
                print("Account sucessfully activated!")
                break
            else:
                print("Please enter a valid username")


    df.to_csv("volunteers_db.csv",index=False)

    df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

    print(df)

    returnToHomePage()



def deleteVolunteers():
    showdf = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

    print(showdf)

    usernames = []
    with open("volunteers_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                usernames.append(row[0])
    while True:

        user_input = input("Please type in username of volunteer you would like to delete: ")

        if user_input in usernames:
            df = pd.read_csv("volunteers_db.csv")
            df = df.loc[df['usernames'] != user_input]

            df.to_csv("volunteers_db.csv",index=False)

            df = pd.read_csv("volunteers_db.csv", usecols = ["usernames","status"])

            print("Account succesfully deleted!")
            print(df)
            returnToHomePage()
            break

        else:
            print("Please enter a valid username!")

def returnToHomePage():
    while True:

        askUserInput = input("Please enter # to return to home page: ")

        if askUserInput == '#':
            admin()
    





import pandas as pd
import csv

class User:
    def __init__(self,name,username,password):
        self.name = name
        self.username - username
        self.password = password



def home():
    print("[1] Register as volunter")
    print("[2] Login")

    while True:
        user_input = int(input("Please select option: "))

        if user_input == 1:
            print("-------------------------------------------------------------------------------")
            register()
            break
        elif user_input == 2:
            print("-------------------------------------------------------------------------------")
            login()
            break
        else:
            print("Please enter a valid option")

def register():
    
    usernames = []
   
    while True:

        user_input = input("Please enter a username: ")
        with open("usernames_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                usernames.append(row[0])

        if user_input not in usernames:
            break

        else:
            print("Username is taken. Please enter another username or login!")
    
    while True:

        password = input("Please enter a password: ")
        confirm_pass = input("Please confirm password: ")

        if password == confirm_pass:
            break
        else:
            print("Passwords do not match! Please re-enter password.")

    with open("usernames_db.csv","a") as test:
        writer = csv.writer(test,delimiter=',',lineterminator='\n')
        writer.writerow((user_input,password))

    print("Account successfully created")
    print("-------------------------------------------------------------------------------")
    home()
    
def login_volunteer():
    print("Logged in as volunteer")

def login_admin():
    print("Logged in as admin")
    
def login():
    print("[1] Login as admin")
    print("[2] Login as volunteer")
    while True:
        login_input = int(input("Please select an option: "))

        if login_input == 1:
            if ValidateUser:
                login_admin()
            break
        elif login_input ==2:
            if ValidateUser():
                login_volunteer()
            break
        else:
            print("Please enter a valid option: [1] or [2]")


def ValidateUser():
    userData = pd.read_csv("usernames_db.csv")    
    df = pd.DataFrame(userData)

    while True:

        user = input("Please enter your username: ")
        password = input("Please enter your password: ")
        
        validateInput = (len(df[(df.usernames == user) & (df.password == password)]) > 0)

        if validateInput:
            return True
        else:
            print('Incorrect username or password')



home()


import pandas as pd
import csv
from admin import admin

class User:
    '''Represents any user'''
    def __init__(self,username,password,status = "Activated"):
        self.username = username
        self.password = password
        self.status = status

class Volunteer(User):
    '''Represents a volunteer'''
    def __init__(self,username,password, phoneno, status ="Activated",accounttype = "Volunteer"):
        User.__init__(self,username,password,status)
        self.accounttype = accounttype
        self.phoneno = phoneno

class Admin(User):
    '''Represents admin account'''
    def __init__(self,username, password, status = "Activated",accounttype = "Admin"):
        User.__init__(self,username,password,status)
        self.accounttype = accounttype
        print(f"Initialized Admin: {self.username}")
    



def home():
    print("Welcome to the E-Mergency Management System")
    print("[1] Register as volunter")
    print("[2] Login")

    while True:
        user_input = input("Please select option: ")

        if user_input == '1':
            print("-------------------------------------------------------------------------------")
            register()
            break
        elif user_input == '2':
            print("-------------------------------------------------------------------------------")
            login()
            break
        else:
            print("Please enter a valid option")

def register():
    
    usernames = []
   
    while True:

        user_input = input("Please enter a username: ")
        with open("volunteers_db.csv") as file:
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

    while True:

        phone_number = input("Please enter your phone number: ")
        confirm_phone_number = input("Please enter your phone number: ")

        if phone_number == confirm_phone_number:
            break
        else:
            print("Phone numbers do not match. Please re-enter")


    volunteer = Volunteer(user_input,password,phone_number)

    with open("volunteers_db.csv","a") as file2:
        writer = csv.writer(file2,delimiter=',',lineterminator='\n')
        writer.writerow((volunteer.username,volunteer.password,volunteer.phoneno,volunteer.status,volunteer.accounttype))

    print("Account successfully created")
    print("-------------------------------------------------------------------------------")
    home()
    
def login_volunteer():
    print("Logged in as volunteer")
    print("-------------------------------------------------------------------------------")

def login_admin():
    print("Logged in as admin")
    print("-------------------------------------------------------------------------------")
    admin()
    
def login():
    print("[1] Login as admin")
    print("[2] Login as volunteer")
    while True:
        login_input = input("Please select an option: ")

        if login_input == '1':
            if ValidateUser(login_input):
                login_admin()
            break
        elif login_input == '2':
            if ValidateUser(login_input):
                login_volunteer()
            break
        else:
            print("Please enter a valid option: [1] or [2]")


def ValidateUser(login_input):
    if login_input == '1':
        userData = pd.read_csv("admin_db.csv")    
        df = pd.DataFrame(userData).astype('str')
    elif login_input == '2':
        userData = pd.read_csv("volunteers_db.csv")    
        df = pd.DataFrame(userData).astype('str')
    
    while True:

        user = input("Please enter your username: ")
        password = input("Please enter your password: ")
        
        validateInput = (len(df[(df.usernames == user) & (df.password == password)]) > 0)

        if validateInput:
            return True
        else:
            print('Incorrect username or password')





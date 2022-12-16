import pandas as pd
import csv
from admin_home import admin_home
from volunteer_home import volunteer_home

class User:
    '''Represents any user'''
    def __init__(self,firstname,familyname,username,password,status = "Activated"):
        self.firstname = firstname
        self.familyname = familyname
        self.username = username
        self.password = password
        self.status = status

class Volunteer(User):
    '''Represents a volunteer'''
    def __init__(self,firstname,familyname,username,password, phoneno, status ="Activated",accounttype = "Volunteer"):
        User.__init__(self,firstname,familyname,username,password,status)
        self.accounttype = accounttype
        self.phoneno = phoneno

class Admin(User):
    '''Represents admin account'''
    def __init__(self,firstname,familyname,username, password, status = "Activated",accounttype = "Admin"):
        User.__init__(self,firstname,familyname,username,password,status)
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
    
    first_name = input("Please enter your first name: ")

    family_name = input("Please enter your family name: ")
    usernames = []
   
    while True:

        user_input = input("Please enter a username: ")
        with open("volunteers_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                usernames.append(row[2])

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


    volunteer = Volunteer(first_name,family_name,user_input,password,phone_number)

    with open("volunteers_db.csv","a") as file2:
        writer = csv.writer(file2,delimiter=',',lineterminator='\n')
        writer.writerow((volunteer.firstname,volunteer.familyname,volunteer.username,volunteer.password,volunteer.phoneno,volunteer.status,volunteer.accounttype))

    print("Account successfully created")
    print("-------------------------------------------------------------------------------")
    home()
    
def login_volunteer(inp):
    print("Logged in as volunteer")
    volunteer_home(user)
def login_admin():
    print("Logged in as admin")
    admin_home()
    
def login():
    print("[1] Login as admin")
    print("[2] Login as volunteer")
    while True:
        login_input = input("Please select an option: ")

        if login_input == '1':
            print("-------------------------------------------------------------------------------")
            if ValidateUser(login_input):
                login_admin()
            break
        elif login_input == '2':
            print("-------------------------------------------------------------------------------")
            if ValidateUser(login_input):
                login_volunteer(user)
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
    
    global user
    # usernames = []
    while True:
        user = input("Please enter your username: ")   
        if df['usernames'].eq(user).any():
                break
        else:
            print("Username does not exist. Please re-enter correct username")

    for i in range(6):
            password = input("Please enter your password: ")

            validateInput = (len(df[(df.usernames == user) & (df.password == password)]) > 0)

            validateStatus = (len(df[(df.usernames == user) & (df.password == password) & (df.status == "Activated")]) > 0)

            if validateInput and validateStatus:
                return True
            
            elif validateInput and validateStatus == False:
                print("Account deactivated. Please contact admin")
                print("Returning to home screen")
                print("-------------------------------------------------------------------------------")
                home()
                return False
            elif i == 5:
                df.loc[df["usernames"] == user,"status"]='Deactivated'
                df.to_csv("volunteers_db.csv",index=False)
                print('Your account has now been deactivated! Please contact admin')
            else:
                print(f"Incorrect password. You have {5 - i} attempts left before account is deactivated")


home()


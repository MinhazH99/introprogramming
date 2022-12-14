import pandas as pd
import csv
import random
import string
import re
import admin_home
import volunteer_home
import mail_demo
import pyfiglet

class User:
    '''Represents any user'''
    def __init__(self,firstname,familyname,email,username,password,status = "Activated"):
        self.firstname = firstname
        self.familyname = familyname
        self.email = email
        self.username = username
        self.password = password
        self.status = status

class Volunteer(User):
    '''Represents a volunteer'''
    def __init__(self,firstname,familyname,email,username,password, phoneno, status ="Activated",accounttype = "Volunteer"):
        User.__init__(self,firstname,familyname,email,username,password,status)
        self.accounttype = accounttype
        self.phoneno = phoneno

class Admin(User):
    '''Represents admin account'''
    def __init__(self,firstname,familyname,email,username, password, status = "Activated",accounttype = "Admin"):
        User.__init__(self,firstname,familyname,email,username,password,status)
        self.accounttype = accounttype
        print(f"Initialized Admin: {self.username}")
    



def home():
    print(pyfiglet.figlet_format("Welcome to EMS",font = "big"))
    print("Welcome to the E-Mergency Management System (EMS)")
    print("[1] Register as volunteer")
    print("[2] Login")
    print("[#] Exit the System")

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
        
        elif user_input == '#':
            print("Succesfully exited program")
            print("-------------------------------------------------------------------------------")
            break
        else:
            print("Please enter a valid option")

def register():
    
    while True:
        first_name = input("Please enter your first name: ")
        
        if len(first_name.strip()) != 0:
            break
        else:
            print("Please enter a first name")

    while True:
        family_name = input("Please enter your family name: ")
        if len(family_name.strip()) != 0:
            break
        else:
            print("Please enter a family name ")
    
    usernames = []
    
    emails = []


   
    regexs = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    while True:
        email_input = input("Please enter your email-address: ")
        with open("volunteers_db.csv") as file:
            reader = csv.reader(file,delimiter=",")
            next(reader)
            for row in reader:
                emails.append(row[7])
        
        if (re.fullmatch(regexs,email_input)):       
                if email_input not in emails:
                    break
                else:
                 print("Email is taken. Please enter another email")

        else:
            print("Email is invalid. Please enter a valid email") 
    
    
    while True:
        while True:
            user_input = input("Please enter a username: ")
            if len(user_input.strip()) != 0:
                break
            else:
                print("Username can not be 0 characters!")
        
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
        while True:
            password = input("Please enter a password: ")
            if len(password.strip()) !=0:
                break
            else:
                print("Password can not be 0 characters!")
        confirm_pass = input("Please confirm password: ")

        if password == confirm_pass:
            break
        else:
            print("Passwords do not match! Please re-enter password.")

    while True:

        phone_number = input("Please enter a valid UK  phone number (in the format 07... which has 10 or 11 digits: ")
        if (len(phone_number) == 11 or len(phone_number) == 10) and phone_number[0] == "0" and phone_number[1] == "7" and phone_number.isdigit():
            confirm_phone_number = input("Please confirm your phone number: ")
            if phone_number == confirm_phone_number:
                break
            else:
                print("Phone numbers do not match. Please re-enter")
        else:
            print("Phone number is not valid. Please enter a valid phone number")


    volunteer = Volunteer(first_name,family_name,email_input,user_input,password,phone_number)

    with open("volunteers_db.csv","a") as file2:
        writer = csv.writer(file2,delimiter=',',lineterminator='\n')
        writer.writerow((volunteer.firstname,volunteer.familyname,volunteer.username,volunteer.password,volunteer.phoneno,volunteer.status,volunteer.accounttype,volunteer.email))

    print("Account successfully created")
    print("-------------------------------------------------------------------------------")
    home()
    
def login_volunteer(inp):
    print("Logged in as volunteer")
    volunteer_home.volunteer_home(inp)
def login_admin():
    print("Logged in as admin")
    admin_home.admin_home()
    
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
    if login_input == '2':
        while True:
            user = input("Please enter your username: ")   
            if df['usernames'].eq(user).any():
                    break
            else:
                print("Username does not exist. Please re-enter correct username")

        for i in range(6):
                print("Please enter 'R' if you have forgotten your password")
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
                    home()
                    break
                
                elif password == 'R':
                    ForgotPassword(user)
                    home()
                    break

                else:
                    print(f"Incorrect password. You have {5 - i} attempts left before account is deactivated")

    elif login_input == '1':
        while True:
            user = input("Please enter your username: ")   
            if df['usernames'].eq(user).any():
                    break
            else:
                print("Username does not exist. Please re-enter correct username")
            
        while True:
            password = input("Please enter your password: ")

            validateInput = (len(df[(df.usernames == user) & (df.password == password)]) > 0)

            validateStatus = (len(df[(df.usernames == user) & (df.password == password) & (df.status == "Activated")]) > 0)

            if validateInput:
                return True

            else:
                print("Incorrect password")

def ForgotPassword(user):
    rnd_strng = string.ascii_letters + string.digits

    result = ''.join((random.choice(rnd_strng) for i in range(8)))

    userData = pd.read_csv("volunteers_db.csv")

    df = pd.DataFrame(userData).astype('str')
    df.loc[df["usernames"] == user,"token"] = result
    df.to_csv("volunteers_db.csv",index = False)
    
    mail_demo.get_password(user)


    user_token =  df.loc[(df['usernames'] == user)]['token'].values[0]
    while True:
            check_token = input("Please enter your reset token: ")

            if check_token == user_token:
               break
            else:
                print("Token is incorrect.Please try again!")

    while True:
        while True:
            new_password = input("Please enter your new password: ")
            if len(new_password.strip()) !=0:
                break
            else:
                print("New password can not be 0 characters!")
        confirm_new_pass = input("Please confirm new password: ")

        if new_password == confirm_new_pass:
            print("Password successfuly changed")
            df.loc[df["usernames"] == user,"password"] = new_password
            df.to_csv("volunteers_db.csv",index = False)
            break
        else:
            print("Passwords do not match. Please try again")

# home()


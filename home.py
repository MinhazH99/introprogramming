
class User:
    def __init__(self,name,username,password):
        self.name = name
        self.username - username
        self.password = password



def home():
    print("[1] Register as volunter")
    print("[2] Login as admin")
    print("[3] Login as volunteer")



    user_input = int(input("Please select option: "))

    if user_input == 1:
        register()
    elif user_input == 2:
        login_admin()
    elif user_input == 3:
        login_volunteer()

def register():
   
    
    # Check if user exist in data

    log = True
    while log == True:
        username = input("Please enter a username: ")
        with open("username_db.txt","r") as test:
            for row in test:
                data = row.split(",")
                if username == data[0]:
                    print("Username already exists")

                else:
                    log = False
        
                
            

    password = input("Please enter a password: ")
    confirm_pass = input("Please confirm password: ")

    db = open("username_db.txt","a")
    db.write(username + "," + password + "\n")
    db.close
    print("Account successfully created")
    
    
                   
def login_admin():
    login_user = input("Please enter your username: ")
    login_pass = input("Please enter your password: ")

    log = True
    while log == True:
        with open("username_db.txt","r") as info:
            for row in info:
                username,password = row.replace("\n","").split(",")

            if login_user == username and login_pass == password:
                log = True
                break
            else:
                log = False
                continue

    if log == True:
        print("Welcome!")
        #login_admin()


def login_volunteer():
    login_user = input("Please enter your username: ")
    login_pass = input("Please enter your password: ")

    log = True
    while log == True:
        with open("username_db.txt","r") as info:
            for row in info:
                username,password = row.replace("\n","").split(",")

            if login_user == username and login_pass == password:
                log = True
                break
            else:
                log = False
                continue

    if log == True:
        print("Welcome!")
        #login_volunteer()
    
            



home()


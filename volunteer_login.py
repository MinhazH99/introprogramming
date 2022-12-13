# One thing I'm not yet clear on is how volunteers would be created. I've not tackled that below,
# but I've used the __init method for the time being to create and test out dummy data
# Make repeating part into a function and call it

import pandas as pd
import csv

def editPersonalInfo(user):
    """
    Currently the way of rewriting files is written in a difficult-to-read way, and is a bit clumsy, but functional
    """
    username = user

    print("[1] Change First Name")
    print("[2] Change Second Name")
    print("[3] Change Phone Number")
    print("[4] Return to home screen")

    user_input = input("Please select an option: ")

    df = pd.read_csv("volunteers_db.csv")
    # print(df['firstname'].value_counts())
    # print(df['firstname'].value_counts()['Jane'])
    # print(df['familyname'].value_counts())
    # print(df['familyname'].value_counts()['Doe'])

    firstnames = []
    familynames = []
    phonenos = []
    
    #create lists of all existing first names, family names and phone numbers
    with open("volunteers_db.csv") as file:
        reader = csv.reader(file,delimiter=",")
        next(reader)
        for row in reader:
            firstnames.append(row[0])
            familynames.append(row[1])
            phonenos.append(row[4])
    
    # instructions for changing first name
    if user_input == '1':

        while True:

            current_firstname = input("Enter current first name: ").strip()
            if current_firstname in firstnames:

                new_firstname = input("Enter your first name: ").strip()
                new_firstname_verification = input("Re-enter your first name: ").strip()


                if new_firstname != new_firstname_verification: #add type verification here - no numbers
                    print("Names must match.")
                    
                else:
                    df.loc[(df["usernames"] == username) & (df["firstname"] == current_firstname),"firstname"]=f'{new_firstname}' #Use this in selecting_shifts
                    print("First name updated")
                    df.to_csv("volunteers_db.csv",index=False)
                    #Extra feature: ask reason for name change
                    #TO DO with extra feature: notify admin of reason for name change
                    break
           
                    
            else:
                print("First name not found")

    # instructions for changing family name
    elif user_input == '2':
        # reason = input("Enter your reason for changing names: ")
        while True:

            current_family_name = input("Enter current family name: ").strip()
            if current_family_name in familynames:

                new_family_name = input("Enter your family name: ").strip()
                new_family_name_verification = input("Re-enter your family name: ").strip()

              
                if new_family_name != new_family_name_verification: #add type verification here - no numbers
                    print("Names must match.")
                    
                else:
                    df.loc[(df["usernames"] == username) & (df["familyname"] == current_family_name),"familyname"]=f'{new_family_name}'
                    print("Family name updated")
                    df.to_csv("volunteers_db.csv",index=False)
                    #Extra feature: ask reason for name change
                    #TO DO with extra feature: notify admin of reason for name change
                    break
                
                    
            else:
                print("Family name not found")
            # TO DO: create a trigger to include the reason for a name change when sending a report to the administrator

    # instructions for changing phone number
    elif user_input == '3':
        
        while True:
            current_number = str(input("Enter current phone number: ")).strip()
            if current_number in phonenos:

                new_number = str(int(input("Enter your phone number without spaces: "))).strip()
                new_number_verification = str(int(input("Re-enter your phone number without spaces: "))).strip()

            

                if new_number != new_number_verification:
                    print("Numbers must match.")
                    
                else:
                    df.loc[(df["usernames"] == username) & (df["phoneno"] == current_number),"phoneno"]=f'{new_number}'
                    print("Phone number updated")
                    df.to_csv("volunteers_db.csv",index=False)
                    #Extra feature: ask reason for name change
                    #TO DO with extra feature: notify admin of reason for name change
                    break
                
                    
            else:
                print("Phone number not found")
            # TO DO: create a trigger to include the reason for a name change when sending a report to the administrator
        
        #TO DO: implement type/ format forcing
        #could make phone number unique by default, but for now written as if it's not

    # instructions for exiting
    elif user_input == '4':
        print("Exiting now.")
        # implement error-handling here

    else:
        print("Value not recognised.")
        # not yet implemented error-handling

user = 'volunteer1'
editPersonalInfo(user)
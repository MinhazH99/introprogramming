import sqlite3
import os
emergencyFilename = 'emergency_profile.txt'


def emegerncy_profile():
    while True:
        profile_menu()
        volunteer_option = str(input("Option : "))
        if volunteer_option in ["0", "1", "2", "3", "4", "5", "6"]:
            if volunteer_option == "0":
                answer = input("Are you sure to exit? Y/N \n")
                if answer == 'Y' or 'y':
                    print("Thanks for visiting our website!")
                    break
                else:
                    continue
            if volunteer_option == "1":
                create_profile()
            elif volunteer_option == "2":
                modify_profile()
            elif volunteer_option == "3":
                delete_profile()
            elif volunteer_option == "4":
                search_profile()
            elif volunteer_option == "5":
                create_multiple_profiles()
            elif volunteer_option == "6":
                show_profile()


def profile_menu():
    print("")
    print("Edit Emergency Profile Menu")
    print("1. Create New Emergency Profile")
    print("2. Edit Existing Emergency Profile")
    print("3. Delete Existing Emergency Profile")
    print("4. Search Emergency Profile")
    print("5. Create Multiple Emergency Profiles")
    print("6. Show All Emergency Profiles")
    print("0. Exit")

def create_profile():
    print("Create New Emergency Profile")
    profile_list = []
    while True:
        print("")
        refugee_name = str(input("Please enter the refugee's name: "))
        # If they don't enter anything for refugeeName or campCode, the function will end
        if not refugee_name:
            break
        camp_code = str(input("Please enter the code of camp that they are in: "))
        if not camp_code:
            break
        try:
            family_number = int(input("Please enter the numbers of his/her family in the camp: "))
        except: 
            print("The input is not a number, please enter a number")
            continue
        medical_condition = str(input("Please enter the Refugee's Medical condition if any: "))
        profile = {'refugee_name':refugee_name, 'camp_code':camp_code, 'family_number':family_number, 'medical_condition':medical_condition}
        profile_list.append(profile)
        answer = input("Do you want to create another emergency profile? Y/N \n")
        if answer == 'y':
            continue
        else:
            break
    save_profile(profile_list)
    print("The emergency profile(s) has been created.")

def modify_profile():
    show_profile()
    if os.path.exists(emergencyFilename):
        with open(emergencyFilename, 'r', encoding='utf-8') as rfile:
            profile_info = rfile.readlines()
    else:
        return
    searched_refugee_name = input("Please enter the name of the refugee that you're searching: ")
    with open(emergencyFilename, 'w', encoding='utf-8') as wfile:
        for refugee in profile_info:
            d = dict(eval(refugee))
            if d['refugee_name'] == searched_refugee_name:
                print("Please confirm the information of the refugee: ")
                while True:
                    try:
                        d['refugee_name'] = input("Please enter the refugee's name: ")
                        d['camp_code'] = input("Please enter the code of camp that they are in: ")
                        d['family_number'] = input("Please enter the numbers of his/her family in the camp: ")
                        d['medical_condition'] = input("Please enter the Refugee's Medical condition if any: ")
                    except:
                        print("Wrong input, please enter again")
                    else:
                        break
                wfile.write(str(d) + '\n')
                print("Successfully updated the profile of the refugee.")
            else:
                wfile.write(str(d) +'\n')
        answer = str(input("Continue to edit another emergency profile? Y/N \n"))
        # Bug to be fixed: when input is not y/Y, will still execute modify_profile()
        if answer == 'Y' or 'y':
            modify_profile()
            

def delete_profile():
    while True:
        refugee_name = str(input("Please enter the name of the refugee that you want to delete : "))
        if refugee_name != '':
            if os.path.exists(emergencyFilename):
                with open (emergencyFilename, 'r', encoding='utf-8') as rfile:
                    profile_info = rfile.readlines()
            # If file doesn't exist, set it to null
            else: 
                profile_info = []
            flag = False # Tag if deleted it or not, default: not deleted
            if profile_info:
                with open(emergencyFilename, 'a+', encoding='utf-8') as wfile:
                    d = {}
                    for profile in profile_info:
                        dict(eval(profile))
                        if d['refugee_name'] != refugee_name:
                            wfile.write(str(d) +'\n')
                        else:
                            flag = True
                    if flag:
                        print(f"Successfullt deleted the emergency profile of {refugee_name}")
                    else:
                        print(f"The emergency profile of {refugee_name} not found.")
            else:
                print("No emergency profile found.")
                break
            show_profile()
            answer = input("Continue to delete other emergency profile? Y/N")
            if answer == 'Y' or 'y':
                continue
            else:
                break










def search_profile():
    pass

def create_multiple_profiles():
    pass

def show_profile():
    pass

def save_profile(list):
    try:
        profile_txt=open(emergencyFilename, 'a', encoding='utf-8')
    except:
        profile_txt=open(emergencyFilename, 'w', encoding='utf-8')
    for item in list:
        profile_txt.write(str(item)+'\n')
    profile_txt.close()

emegerncy_profile()
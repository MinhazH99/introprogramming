import os
import csv
import sys
import pandas as pd
emergencyFilename = 'emergency_profile.csv'


def emergency_profile():
    while True:
        profile_menu()
        volunteer_option = str(input("Option : "))
        if volunteer_option in ["0", "1", "2", "3", "4", "5", "6"]:
            if volunteer_option == "0":
                answer = input("Are you sure to exit? Y/N \n")
                if answer == 'Y' or answer == 'y':
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
                show_all_profile()


def profile_menu():
    print("")
    print("Edit Emergency Profile Menu")
    print("[1] Create New Emergency Profile")
    print("[2] Edit Existing Emergency Profile")
    print("[3] Delete Existing Emergency Profile")
    print("[4] Search Emergency Profile")
    print("[5] Show All Emergency Profiles")
    print("[0] Exit")

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
        if answer == 'y' or answer == 'Y':
            continue
        else:
            break

    with open(emergencyFilename, "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['refugee_name', 'camp_code', 'family_number', 'medical_condition'])
        writer.writeheader()
        for profile in profile_list:
            writer.writerow(profile)
    print("The emergency profile(s) has been created.")

def csv_modify_profile():
    df = pd.read_csv(emergencyFilename)
    searched_refugee_name = input("Please enter the name of the refugee that you're searching: ")


def modify_profile():
    if os.path.exists(emergencyFilename):
        with open(emergencyFilename, 'r', encoding='utf-8') as rfile:
            profile_info = rfile.readlines()
    else:
        return
    with open(emergencyFilename, "r",  encoding='utf-8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
        
    searched_refugee_name = input("Please enter the name of the refugee that you're searching: ")
    with open(emergencyFilename, 'a+', encoding='utf-8') as wfile:
        for refugee in profile_info:
            d = dict(eval(refugee))
            if d['refugee_name'] == searched_refugee_name:
                print("Found the refugee's profile. Please modify the information of the refugee: ")
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
                # If the refugee's profile is not found, create a new profile for the refugee. 
                wfile.write(str(d) +'\n')
        answer = str(input("Continue to edit another emergency profile? Y/N \n"))
        # Bug to be fixed: when input is not y/Y, will still execute modify_profile()
        if answer == 'Y' or answer== 'y':
            modify_profile()


def txt_delete_profile():
    while True:
        delete_refugee_name = input("Please enter the name of the refugee that you want to delete : ")
        if delete_refugee_name != '':
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
                        dict(eval(profile))  # Convert String to dictionary
                        # If the refugee is not found, create a new profile for the refugee 
                        if d['refugee_name'] != delete_refugee_name: 
                            wfile.write(str(d) +'\n')
                        else:
                            flag = True
                    if flag:
                        print(f'Successfullt deleted the emergency profile of {delete_refugee_name}')
                    else:
                        print(f'The emergency profile of {delete_refugee_name} is not found.')
            else:
                print("No emergency profile found.")
                break
            answer = input("Continue to delete other emergency profile? Y/N \n")
            if answer == 'Y' or answer == 'y':
                continue
            else:
                break

def delete_profile():
    while True:
        delete_refugee_name = str(input("Please enter the name of the refugee that you want to delete : "))
        df = pd.read_csv(emergencyFilename, header=0)
        #if delete_refugee_name in pd.Series.to_string(df['refugee_name']):   -> Why not
        # Do we need to consider refugees have the same name?
        delete_profile_result = df[(df['refugee_name'] == delete_refugee_name)]
        if len(delete_profile_result) != 0: 
            #df = df.drop(df.index[df['A'] == 2]) ## 删除A列数值为2的行
            #❌Not working
            df.drop(df.index[df['refugee_name'] == delete_refugee_name], inplace=True)
            answer = input(f"Deleted {delete_refugee_name}'s profile successfully. Continue to delete other emergency profile? Y/N \n")
            if answer == 'Y' or answer == 'y':
                continue
            else:
                break
        else:
            print("Refugee not found. ")
            return

def search_profile():
    keyword = ""
    while True:
        keyword = input("Please enter the refugee's name: ")
        df = pd.read_csv(emergencyFilename, header=0)
        # profile_search_result = df[(keyword in pd.Series.to_string(df['refugee_name']))]   -> not working
        profile_search_result = df[(df['refugee_name'] == keyword)]
        if len(profile_search_result) != 0:
            print("Below is the search result(s): ")
            print(profile_search_result)
            answer = input("Continue to search emergency profile? Y/N \n")
            if answer == 'Y' or answer == 'y':
                continue
            else:
                break
        else:
            print("Emergency profile not found.")
            return

def show_all_profile():
    if os.path.exists(emergencyFilename):
        print("")
        print("Summary of all emergency profiles:")
        df = pd.read_csv(emergencyFilename, header=0)
        print(df)
    else:
        print("No result found. ")

emergency_profile()
#delete_profile()
#search_profile()
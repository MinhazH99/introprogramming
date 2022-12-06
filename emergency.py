import os
import csv
import sys
import pandas as pd
emergencyFilename = 'emergency_profile.csv'


def emergency_profile():
    while True:
        profile_menu()
        volunteer_option = str(input("Option: "))
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
        for profile in profile_list:
            writer.writerow(profile)
    print("The emergency profile(s) has been created.")

def modify_profile():
    refugee_name_list = []
    with open(emergencyFilename, "r",  encoding='utf-8', errors='ignore') as rfile:
        reader = csv.reader(rfile)
        for row in reader:
            refugee_name_list.append(row[0])
    
    show_all_profile()
    searched_refugee_name = input("Please enter the name of the refugee's profile that you want to modify: ")

    if searched_refugee_name in refugee_name_list:
        print("Found the refugee's profile. Please modify the information of the refugee: ")
        while True:
            try:
                refugee_name = input("Please enter the refugee's name: ")
                camp_code = input("Please enter the code of camp that they are in: ")
                family_number = input("Please enter the numbers of his/her family in the camp: ")
                medical_condition = input("Please enter the Refugee's Medical condition if any: ")
            except:
                print("Wrong input, please enter again")
            else:
                break
        df = pd.read_csv('emergency_profile.csv')
        df.loc[df['refugee_name'] == searched_refugee_name] = [refugee_name, camp_code, family_number, medical_condition]
        df.to_csv('emergency_profile.csv', index = False)
        print("Successfully updated the profile of the refugee.")
    else:
        print("Emergency profile not found. ")
            
    answer = str(input("Continue to edit another emergency profile? Y/N \n"))
    if answer == 'Y' or answer== 'y':
        modify_profile()
    
        
def delete_profile():
    while True:
        delete_refugee_name = str(input("Please enter the name of the refugee that you want to delete : "))
        df = pd.read_csv('emergency_profile.csv')
        # Do we need to consider refugees have the same name?
        delete_profile_result = df[(df['refugee_name'] == delete_refugee_name)]
        if len(delete_profile_result) != 0: 
            df.drop(df.index[df['refugee_name'] == delete_refugee_name], inplace = True)
            df.to_csv('emergency_profile.csv', index = False)
            answer = input(f"Deleted {delete_refugee_name}'s emergency profile successfully. Continue to delete other emergency profile? Y/N \n")
            if answer == 'Y' or answer == 'y':
                continue
            else:
                break
        else:
            print("Emergency profile not found. ")
            return

def search_profile():
    keyword = ""
    while True:
        keyword = input("Please enter the refugee's name: ")
        df = pd.read_csv(emergencyFilename)
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
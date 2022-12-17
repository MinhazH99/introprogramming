import os
import csv
import sys
import pandas as pd
from tabulate import tabulate
from datetime import date

#to avoid FutureWarning about the coming deprecation of the numeric_only method for Pandas dataframes
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def get_camp_list():
    '''Returns a list of all camps in CampDetails.csv'''
    df = pd.read_csv('CampDetails.csv')
    camp_list = []
    for ind in df.index:
        camp_list.append(df.loc[ind]["Camp ID"])
    return camp_list

def update_refugee_count():
    '''Function to update the number of volunteers in each camp'''
    emergency_df = pd.read_csv('emergency_profile.csv')
    camps_df = pd.read_csv('CampDetails.csv')
    camp_list = get_camp_list() #store list of all camps
    refugee_count_list = []
    for camp in camp_list:
        try:
            camp_df = emergency_df[emergency_df['camp_id'] == camp]
            refugee_count_list.append(int(camp_df.sum()['family_number']))
        except KeyError:
            refugee_count_list.append(0) #if the camp does not appear in the emergency_profile database, it has no refugees
    refugee_count_dict = {camp_list[i]: refugee_count_list[i] for i in range(len(camp_list))} #dictionary of camp IDs and no. refugees at each 
    for key, value in refugee_count_dict.items():
        camps_df.loc[camps_df['Camp ID'] == f'{key}', 'No. Refugees'] = f'{str(value)}' #update number of refugees at each camp
    camps_df.to_csv("CampDetails.csv",index=False) #store the updated counts

def emergency_profile():
    while True:
        profile_menu()
        volunteer_option = str(input("Option: "))
        if volunteer_option in ["0", "1", "2", "3", "4", "5"]:
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
        else:
            print("Wrong input, please enter a number from 0 to 5")


def profile_menu():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------")
    print("Refugee's Emergency Profile Menu")
    print("[1] Create New Emergency Profile")
    print("[2] Edit Existing Emergency Profile")
    print("[3] Delete Existing Emergency Profile")
    print("[4] Search Emergency Profile")
    print("[5] Show All Emergency Profiles")
    print("[0] Exit")


def create_profile():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------")
    print("Create New Emergency Profile")
    profile_list = []
    while True:
        print("")
        input_refugee_name = str(input("Please enter the refugee's name: "))
        # If they don't enter anything for refugeeName or camp_id the function will end
        if not input_refugee_name:
            break

        # Check if the input name already exists in our profile, if so, add a number after the name.
        # For example, if "chris" already exists in profile, put "chris1" as the refugee's name, then "chris2", "chris3" and so on.
        df = pd.read_csv('emergency_profile.csv')
        name_result = df[(df['refugee_name'].str.startswith(input_refugee_name))]
        
        # Firstly, check if there's name starts with input_refugee_name
        if name_result.empty == False:
            count = 1
            for i in range(len(name_result)):
                # Secondly, count how many of them ends with a number
                if name_result['refugee_name'].values[i][-1].isdigit() == True:
                    count += 1
                # If there's no result ends with a number, then refugee_name = input_refugee_name
                else:
                    refugee_name = input_refugee_name
            # Lastly, concatenate the input_refugee_name with the count number. 
            refugee_name = input_refugee_name + str(count)
        else:
            # If there's no name starts with input_refugee_name, then refugee_name = input_refugee_name
            refugee_name = input_refugee_name
    

        # While loop for camp_id validation
        while True:
            camp_id = str(input("Please enter the ID of camp that they are in: "))
            if not camp_id:
                break
            # Validating that camp_id exits in CampDetails.csv:
            df = pd.read_csv('CampDetails.csv')
            id_result = df[(df['Camp ID'] == camp_id)]
            if len(id_result) != 0:
                # While loop for family_number validation
                while True:
                    # Validating that family_number input is a number
                    try:
                        family_number = int(input("Please enter the numbers of his/her family in the camp (enter 0 if there's no family member): "))
                    except: 
                        print("The input is not a number, please enter again")
                        continue
                    # Medical condition can be null.
                    medical_condition = str(input("Please enter the Refugee's Medical condition if any: "))
                    # Food requirement can be null.
                    food_requirement = str(input("Please enter the Refugee's food requirement if any: "))
                    # Food requirement can be null.
                    space_requirement = str(input("Please enter the Refugee's space requirement if any: "))
                    create_time = date.today().strftime("%Y-%m-%d")
                    break
                    
                profile = {'refugee_name':refugee_name, 'camp_id':camp_id, 'family_number':family_number, 'medical_condition':medical_condition,
                 'food_requirement':food_requirement, 'space_requirement':space_requirement, 'create_time':create_time}
                profile_list.append(profile)
                break
            else: 
                print("The camp ID is invalid, please enter again.")
                continue
        answer = input("\nSuccessfully created the profile(s) of the refugee.\nDo you want to create another emergency profile? Y/N \n")
        if answer == 'y' or answer == 'Y':
            continue
        else:
            print("\nHere's the profile(s) you've created just now:")
            print(tabulate(pd.DataFrame(profile_list).fillna("None"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
            break

    # If volunteer doesn't input the refugee's name, the info won't be written to the csv file. 
    if profile_list:
        with open("emergency_profile.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['refugee_name', 'camp_id', 'family_number', 'medical_condition', 'food_requirement', 'space_requirement', 'create_time'])
            for profile in profile_list:
                writer.writerow(profile)
                update_refugee_count()
            print("The emergency profile(s) has been created.")


def modify_profile():
    show_all_profile()
    modify_refugee_name = str(input("Please enter the name of the refugee's profile that you want to modify: "))
    df = pd.read_csv('emergency_profile.csv')
    result = df.loc[df['refugee_name'].str.contains(modify_refugee_name, case=False)]
    
    if result.empty == False:
        print("\nHere's the summary of the refugee's profile(s): ")
        # Show the user all the emergency profile that contains the input first
        print(tabulate(result.fillna("None"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
        exact_searched_refugee_name = str(input("Please ensure modification by entering the exact refugee name that you want to modify: "))
        exact_result = df.loc[df['refugee_name'] == exact_searched_refugee_name]
        if exact_result.empty == False:
            while True:
                print("[1]Refugee Name [2]Camp ID [3]Family Number [4]Medical Condition [5]Food Requirement [6]Space Requirement [0]Finish Edit")
                user_input = str(input("Please select an option: "))
                if user_input in ["0", "1", "2", "3", "4", "5", "6"]:
                    if user_input == "0":
                        print(f"Finished editing {exact_searched_refugee_name}'s profile.")
                        break
                    if user_input == "1":
                        change = "refugee_name"
                        update_content = str(input("Please update refugee name: "))
                    elif user_input == "2":
                        change = "camp_id"
                        content_input = str(input("Please update camp ID: "))
                        df = pd.read_csv('CampDetails.csv')
                        if not df[(df['Camp ID'] == content_input)].empty:
                            update_content = content_input
                        else:
                            print("Invalid camp ID. Please enter again. ")
                            continue
                    elif user_input == "3":
                        change = "family_number"
                        try:
                            update_content = int(input("Please update refugee's family number: "))
                        except:
                            print("Please enter a number(enter 0 if there's no family member).")
                    elif user_input == "4":
                        change = "medical_condition"
                        update_content = str(input("Please update refugee's medical condition: "))
                    elif user_input == "5":
                        change = "food_requirement"
                        update_content = str(input("Please update refugee's food requirement: "))
                    elif user_input == "6":
                        change ="space_requirement"
                        update_content = str(input("Please update refugee's space requiremen: "))
                        
                    # Update the change to emergency_profile.csv
                    df = pd.read_csv('emergency_profile.csv')
                    df.loc[df['refugee_name'] == exact_searched_refugee_name, change] = [update_content]
                    df.to_csv('emergency_profile.csv', index = False)
                    print("Successfully updated the profile. Do you want to keep editing this emergency profile?")
                else:
                    print("Wrong input, please enter a number from 0 to 6.")
                    break
        else:
            print("Refugee name not found.")
                
    answer = str(input("Continue to edit emergency profile? Y/N \n"))
    if answer == 'Y' or answer== 'y':
        modify_profile()
        

def delete_profile():
    while True:
        print("\n----------------------------------------------------------------------------------------------------------------------------------------")
        delete_refugee_name = str(input("Please enter the name of the refugee that you want to delete : "))
        df = pd.read_csv('emergency_profile.csv')
        # Show every emergency profile of the name that the keyword contains
        contains_keyword = df[df['refugee_name'].str.contains(delete_refugee_name, case=False)]
        if len(contains_keyword) != 0: 
            print(tabulate(contains_keyword.fillna("None"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement"], tablefmt='fancy_grid', showindex=False))
            # 
            exact_delete_refugee_name = input("Please ensure deletion by entering the exact refugee name that you want to delete: ")
            df.drop(df.index[df['refugee_name'] == exact_delete_refugee_name], inplace = True)
            df.to_csv('emergency_profile.csv', index = False)
            update_refugee_count()
            answer = input(f"Deleted {delete_refugee_name}'s emergency profile successfully. Continue to delete other emergency profile? Y/N \n")
            if answer == 'Y' or answer == 'y':
                continue
            else:
                break
        else:
            print("Emergency profile not found. ")
            return


def search_profile():
    while True:
        print("\n----------------------------------------------------------------------------------------------------------------------------------------")
        keyword = input("Please enter the refugee's name: ")
        # If there's no input, go back to profile main menu
        if not keyword:
            print("There's no input, coming back to Refugee's Emergency Profile Menu...")
            break
        # Find keyword in csv file
        user_data = pd.read_csv("emergency_profile.csv")
        df = pd.DataFrame(user_data).astype("str")
        contains_keyword = df[df['refugee_name'].str.contains(keyword, case=False)]
        if len(contains_keyword) != 0: 
            print("Below is the search result: ")
            # Display the result(s) found in csv file sorting by create_time.
            contains_keyword['create_time'] = pd.to_datetime(contains_keyword['create_time'])
            print(tabulate(contains_keyword.sort_values(by='create_time').fillna("None"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
            answer = input("Continue to search emergency profile? Y/N \n")
            if answer == 'Y' or answer == 'y':
                continue
            else:
                break
        else:
            print("Emergency profile not found.")
            return


def show_all_profile():
    # Check if emergency_profile.csv exists, if so, print all profiles; if not, print "no result found"
    if os.path.exists("emergency_profile.csv"):
        print("\n----------------------------------------------------------------------------------------------------------------------------------------")
        print("Summary of all emergency profiles:")
        df = pd.read_csv("emergency_profile.csv")
        # Sort the result by create_time
        df['create_time'] = pd.to_datetime(df['create_time'])
        print(tabulate(df.sort_values(by='create_time'), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
    else:
        print("No result found. ")


# To test the code
# emergency_profile()

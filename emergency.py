import os
import csv
import sys
import pandas as pd
from tabulate import tabulate
from datetime import date
import volunteer_home

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

def emergency_profile(user):
    while True:
        profile_menu()
        volunteer_option = str(input("Option: "))
        if volunteer_option in ["0", "1", "2", "3", "4", "5"]:
            if volunteer_option == "0":
                answer = input("Are you sure to exit? Y/N \n")
                if answer == 'Y' or answer == 'y':
                    #print("\nThanks for visiting our website!")
                    volunteer_home.volunteer_home(user)
                    print("-------------------------------------------------------------------------------")
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
    print("-------------------------------------------------------------------------------")
    print("Refugee's Emergency Profile Menu")
    print("[1] Create New Emergency Profile")
    print("[2] Edit Emergency Profile")
    print("[3] Delete Existing Emergency Profile")
    print("[4] Search Emergency Profile")
    print("[5] Show All Emergency Profiles")
    print("[0] Exit")


def create_profile():
    if os.path.exists("emergency_profile.csv"):
        print("-------------------------------------------------------------------------------")

        print("Create New Emergency Profile\n")
        profile_list = []
        while True:
            # Check if the input is null
            flag = True
            while flag:
                input_refugee_name = str(input("Please enter the refugee's name: "))
                if len(input_refugee_name.strip()) != 0:
                    flag = False
                    break
                else: 
                    print("Refugee's name can not be 0 characters!")
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
                # Check if the input is null
                flag = True
                while flag:
                    camp_id = str(input("Please enter the ID of camp that they are in: "))
                    if len(camp_id.strip()) != 0:
                        flag = False
                        break
                    else: 
                        print("Camp ID can not be 0 characters!")
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
                print("\nHere's the profile(s) you've just created:")
                print(tabulate(pd.DataFrame(profile_list).fillna("N/A"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
                break
    else:
        print("No profiles have been made yet. ")

    # Write emergency profile that's just created to emergency_profile.csv
    if profile_list:
        with open("emergency_profile.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['refugee_name', 'camp_id', 'family_number', 'medical_condition', 'food_requirement', 'space_requirement', 'create_time'])
            for profile in profile_list:
                writer.writerow(profile)
                update_refugee_count()


def modify_profile():
    if os.path.exists("emergency_profile.csv"):
        print("-------------------------------------------------------------------------------")
        show_all_profile()
        while True:
            modify_refugee_name = str(input("Please enter the name of the refugee's profile that you want to modify: "))
            if len(modify_refugee_name.strip()) != 0:
                break
            else: 
                print("Name can not be 0 characters!")
        df = pd.read_csv('emergency_profile.csv')
        result = df.loc[df['refugee_name'].str.contains(modify_refugee_name, case=False,na=False)]

        
        if len(result) != 0:
            print("\nHere's the summary of the refugee's profile(s): ")
            # Show the user all the emergency profile that contains the input first
            result = df.loc[df['refugee_name'].str.contains(modify_refugee_name, case=False,na=False)]
            print(tabulate(result.fillna("N/A"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
            exact_searched_refugee_name = str(input("Please ensure modification by entering the exact refugee name that you want to modify: "))
            exact_result = df.loc[df['refugee_name'] == exact_searched_refugee_name]
            if len(exact_result) != 0:
                while True:
                    print("-------------------------------------------------------------------------------")
                    print("What do you want to modify?")
                    print("[1] Refugee Name\n[2] Camp ID \n[3] Family Number \n[4] Medical Condition \n[5] Food Requirement \n[6] Space Requirement \n[0] Finish Edit")
                    user_input = str(input("\nPlease select an option: "))
                    if user_input in ["0", "1", "2", "3", "4", "5", "6"]:
                        if user_input == "0":
                            print(f"Finished editing {exact_searched_refugee_name}'s profile.\n")
                            break

                        if user_input == "1":
                            while True:
                                change = "refugee_name"
                                update_content = str(input("Please update refugee name: "))
                                if len(update_content.strip()) != 0:
                                    break
                                else:
                                    print("Name can not be 0 characters!")
    
                        elif user_input == "2":
                            # Check if the camp id is null and if it is valid
                            while True:
                                change = "camp_id"
                                content_input = str(input("Please update camp ID: "))
                                df = pd.read_csv('CampDetails.csv')
                                if len(content_input.strip()) != 0 and (not df[(df['Camp ID'] == content_input)].empty):
                                    update_content = content_input
                                    break
                                else:
                                    print("Camp ID is not valid.")

                        elif user_input == "3":
                            change = "family_number"
                            while True:
                                try:
                                    update_content = int(input("Please update refugee's family number: "))
                                    if update_content or update_content == 0:
                                        content_input = update_content
                                        break
                                    else:
                                        print("Please enter a number(enter 0 if there's no family member).")
                                except:
                                    print("Please enter a number")
                                    
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
                        print("Successfully updated the profile. Keep editing this emergency profile, enter 0 to finish editing.\n")
                    else:
                        print("Wrong input, please enter a number from 0 to 6.")
                        continue
            else:
                print("Refugee profile not found.")
        else:
            print("Refugee profile not found.")
                
        answer = str(input("Continue to edit emergency profile? Y/N \n"))
        if answer == 'Y' or answer== 'y':
            modify_profile()
    else: 
        print("No profiles have been made yet. ")

def delete_profile():
    if os.path.exists("emergency_profile.csv"):
        print("-------------------------------------------------------------------------------")
        while True:
            while True:
                delete_refugee_name = str(input("Please enter the name of the refugee that you want to delete : "))
                if len(delete_refugee_name.strip()) != 0:
                    break
                else: 
                    print("Name can not be 0 characters!")
            
            df = pd.read_csv('emergency_profile.csv')
            # Show every emergency profile of the name that the keyword contains
            contains_keyword = df[df['refugee_name'].str.contains(delete_refugee_name, case=False)]
            if len(contains_keyword) != 0: 
                print(tabulate(contains_keyword.fillna("N/A"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
                flag = True
                while flag:
                    exact_delete_refugee_name = input("Please ensure deletion by entering the exact refugee name that you want to delete: ")
                    deletedf = contains_keyword.loc[contains_keyword['refugee_name'] == exact_delete_refugee_name]

                    if len(exact_delete_refugee_name.strip()) == 0:
                        print("Name can not be 0 characters!")
                    elif(len(deletedf) == 0):
                        print("No matching result, please enter again. ")
                    else:
                        break
                        
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
    else: 
        print("No profiles have been made yet. ")


def search_profile():
    if os.path.exists("emergency_profile.csv"):
        print("-------------------------------------------------------------------------------")
        while True:
            print("-------------------------------------------------------------------------------")
            keyword = input("Please enter the refugee's name: ")
            # If there's no input, go back to profile main menu
            if not keyword:
                print("There's no input, returning to main menu...")
                break
            # Find keyword in csv file
            user_data = pd.read_csv("emergency_profile.csv")
            df = pd.DataFrame(user_data).astype("str")
            contains_keyword = df[df['refugee_name'].str.contains(keyword, case=False)]
            if len(contains_keyword) != 0: 
                print("Below is the search result: ")
                # Display the result(s) found in csv file sorting by create_time.
                print(tabulate(contains_keyword.sort_values(by='create_time').fillna("N/A"), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
                answer = input("Continue to search emergency profile? Y/N \n")
                if answer == 'Y' or answer == 'y':
                    continue
                else:
                    break
            else:
                print("Emergency profile not found.")
                return
    else: 
        print("No profiles have been made yet. ")


def show_all_profile():
    # Check if emergency_profile.csv exists, if so, print all profiles; if not, print "no result found"
    if os.path.exists("emergency_profile.csv"):
        print("-------------------------------------------------------------------------------")
        df = pd.read_csv("emergency_profile.csv")
        if len(df) == 0:
            print("No profiles have been made yet. ")
        else:
            # Sort the result by create_time
            print("Summary of all emergency profiles:")
            df['create_time'] = pd.to_datetime(df['create_time'])
            print(tabulate(df.sort_values(by='create_time'), headers=["Refugee Name", "Camp ID", "Family Number", "Medical Condition", "Food Requirement", "Space Requirement", "Create Time"], tablefmt='fancy_grid', showindex=False))
    else:
        print("No profiles have been made yet. ")


# To test the code
# emergency_profile("volunteer2")

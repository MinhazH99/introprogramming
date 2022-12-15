import os
import csv
import sys
import pandas as pd
from tabulate import tabulate
from datetime import date


def report():
    while True:
        report_menu()
        volunteer_option = str(input("Option: "))
        if volunteer_option in ["0", "1", "2", "3", "4"]:
            if volunteer_option == "0":
                answer = input("Are you sure to exit? Y/N \n")
                if answer == 'Y' or answer == 'y':
                    print("Thanks for visiting our website!")
                    break
                else:
                    continue
            if volunteer_option == "1":
                create_report()
            elif volunteer_option == "2":
                delete_report()
            elif volunteer_option == "3":
                view_my_report()
            elif volunteer_option == "4":
                view_all_report()
        else:
            print("Wrong input, please enter a number from 0 to 4")


def report_menu():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------")
    print("Report")
    print("[1] Create a New Report")
    print("[2] Delete a Report")
    print("[3] View My Reports")
    print("[4] View All Report")
    print("[0] Exit")


def create_profile():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------")
    print("Create a New Report")
    create_report = []
    # volunteer,title,category,camp_id,message,report_time,severity
    while True:
        print("")
        # Not sure how to get current volunteer's username yet, set a dummy data.
        volunteer = "volunteer1"
        title = str(input("Please enter the report title: "))
        # If they don't enter anything, the function will end
        if not title:
            break
        
        # For example, if "chris" already exists in profile, put "chris1" as the refugee's name, then "chris2", "chris3" and so on.
        df = pd.read_csv('emergency_profile.csv')
        category = df[(df['refugee_name'].str.startswith(input_refugee_name))]
        
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
            print("The emergency profile(s) has been created.")
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


def create_report():
    print("\n----------------------------------------------------------------------------------------------------------------------------------------")
    print("Create a New Report")
    report_list = []
    # volunteer,title,category,camp_id,message,report_time,severity
    while True:
        print("")
        # Not sure how to get current volunteer's username yet, set a dummy data.
        volunteer = "volunteer1"
        while True:
            camp_id = str(input("Please enter the camp id that you want to report: "))
            # if there's no input, ask again 
            if not camp_id:
                continue
            # Validating that camp_id exits in CampDetails.csv:
            df = pd.read_csv('CampDetails.csv')
            id_result = df[(df['Camp ID'] == camp_id)]
            if len(id_result) != 0:
                # While loop for category
                while True:
                    category_choice = str(input("Which category does the report belong to? [1]Harassment [2]Resources [3]Equipment [4]Other: "))
                    if not category_choice:
                        continue 
                    match category_choice:
                        case "1":
                            category = "Harassment"
                        case "2":
                            category = "Resources"
                        case "3":
                            category = "Equipment"
                        case "4":
                            category = "Other"
                        case _:
                            print("Wrong input, please enter 1, 2, 3, or 4.")
                            continue
                    # Title is compolsury, while message can be null. 
                    title = str(input("Please enter the report title: "))
                    if not title:
                        continue
                    message = str(input("Please enter the report content: "))
                    # volunteer,camp_id,category,title,message,report_time,severity
                    report_time = date.today().strftime("%Y-%m-%d")
                    break
                report = {'volunteer':volunteer, 'camp_id':camp_id, 'category':category, 'title':title, 'message':message, 'report_time':report_time}
                report_list.append(report)
                break
            else: 
                print("The camp ID is invalid, please enter again.")
                continue
        answer = input("\nSuccessfully created the report.\nDo you want to create another report? Y/N \n")
        if answer == 'y' or answer == 'Y':
            continue
        else:
            print("\nHere's the report(s) you've created just now:")
            print(tabulate(pd.DataFrame(report_list).fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Time"], tablefmt='fancy_grid', showindex=False))
            break


    # If volunteer doesn't input the refugee's name, the info won't be written to the csv file. 
    if report_list:
        with open("report.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['volunteer', 'camp_id', 'category', 'title', 'message', 'report_time', 'severity'])
            for report in report_list:
                writer.writerow(report)
            print("The report(s) has been created.")


                        
      
def delete_report():
    pass

def view_my_report():
    pass

def view_all_report():
    pass
create_report()
import os
import csv
import sys
import pandas as pd
from tabulate import tabulate
from datetime import date
# Not sure how to get current volunteer's username yet, set a dummy data.
global volunteer
volunteer = "volunteer1"


def report():
    """
    Extra feature: Volunteer can report issues (harassment, resources, equipment, and other) happening in camps to admin.
    Admin will receive the report and grade the severity of the issue. 
    """
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
                    report_date = date.today().strftime("%Y-%m-%d")
                    break
                report = {'volunteer':volunteer, 'camp_id':camp_id, 'category':category, 'title':title, 'message':message, 'report_time':report_date, 'severity':'Not graded yet'}
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
            df = pd.DataFrame(report_list).fillna("None")
            df.loc[df['severity'].isnull(), 'severity'] = "Not graded yet"
            print(tabulate(df, headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Time", "Severity"], tablefmt='fancy_grid', showindex=False))
            break

    # Put the report info into report.csv file. 
    if report_list:
        with open("report.csv", "a", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['volunteer', 'camp_id', 'category', 'title', 'message', 'report_time', 'severity'])
            for report in report_list:
                writer.writerow(report)
            print("The report(s) has been created.")

                        
      
def delete_report():
    while True:
        print("\n----------------------------------------------------------------------------------------------------------------------------------------")
        delete_report_title = str(input("Please enter the title of the report that you want to delete : "))
        df = pd.read_csv('report.csv')

        # Search every report from the volunteer that contains the keyword
        contains_keyword = df.loc[(df['title'].str.contains(delete_report_title, case=False)) & (df['volunteer'] == volunteer)]
        if len(contains_keyword) != 0: 
            # Print out the search result
            print(tabulate(contains_keyword.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Report Time"], tablefmt='fancy_grid', showindex=True))
            
            exact_delete_report_title = input("Please ensure deletion by entering the full title of the report that you want to delete, enter exit to search the report title again: ")
            # df.drop(df.index[df['title'] == exact_delete_report_title], inplace = True)
            df.drop(df.index[df['title'] == exact_delete_report_title], inplace = True)
            df.to_csv('report.csv', index = False)
            if df.drop(df.index[df['title'] == exact_delete_report_title], inplace = True) != None:
                answer = input("Deleted the report successfully. Continue to delete another report? Y/N \n")
                if answer == 'Y' or answer == 'y':
                    continue
                else:
                    break
            else:
                print("Nothing deleted, going back to search the report title again...")
        else:
            print("Report not found. ")
            return

def view_my_report():
    # Check if report.csv exists, if so, print all reports; if not, print "no result found"
    if os.path.exists("report.csv"):
        print("\n----------------------------------------------------------------------------------------------------------------------------------------")
        print("Summary of your reports:")
        df = pd.read_csv("report.csv", header=0)
        my_report = df.loc[df['volunteer'] == volunteer]
        my_report.loc[df['severity'].isnull(), 'severity'] = "Not graded yet"
        print(tabulate(my_report.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))
    else:
        print("No result found. ")

def view_all_report():
    # Check if report.csv exists, if so, print all reports; if not, print "no result found"
    if os.path.exists("report.csv"):
        print("\n----------------------------------------------------------------------------------------------------------------------------------------")
        print("Summary of all reports:")
        df = pd.read_csv("report.csv", header=0)
        df.loc[df['severity'].isnull(), 'severity'] = "Not graded yet"
        print(tabulate(df.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))
    else:
        print("No result found. ")
report()

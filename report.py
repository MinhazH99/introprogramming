import os
import csv
import sys
import pandas as pd
from tabulate import tabulate
from datetime import date
import volunteer_home


def report_func(user):
    """
    Extra feature: Volunteer can report issues (harassment, resources, equipment, and other) 
    happening in the camps that they assigned to to admin.
    Admin will receive the report and grade the severity of the issue. 
    """

    while True:
        report_menu()
        volunteer_option = str(input("Option: "))
        if volunteer_option in ["1", "2", "3", "4", "5"]:
            if volunteer_option == "1":
                create_report(user)
            elif volunteer_option == "2":
                delete_report(user)
            elif volunteer_option == "3":
                view_my_report(user)
            elif volunteer_option == "4":
                view_all_report(user)
            elif volunteer_option == "5":
                volunteer_home.volunteer_home(user)
                break
        else:
            print("Wrong input, please enter a number from 1 to 5")


def report_menu():
    print("-------------------------------------------------------------------------------")
    print("Report Menu")
    print("[1] Create a new report")
    print("[2] Delete my report")
    print("[3] View my reports")
    print("[4] View all reports")
    print("[5] Return to Volunteer Home Page")


def create_report(user):
    print("-------------------------------------------------------------------------------")
    print("Create a New Report")
    volunteer = user
    report_list = []
    while True:
        print("")
        while True:
            # Volunteers can only report issues for the camps they assigned in
            df = pd.read_csv('shifts.csv', header = 0)
            volunteerdf = df.loc[df['username'] == volunteer, 'campid']
            showdf = pd.DataFrame(volunteerdf, columns=['campid'])
            if len(volunteerdf) == 0:
                print("You are not currently working any shifts, and cannot make a report.\n")
                return

            else:
                # print(showdf)
                print(tabulate(showdf,headers=["Camp ID"],tablefmt='fancy_grid',showindex=False))
                camp_id = str(input("Please enter the camp id that you want to report (See above for list of camps ID's): "))
                # if there's no input, ask again 
                if not camp_id:
                    continue
                # Validating that camp input belongs to volunteer's assigned camps:
                id_result = df[(df['campid'] == camp_id) & (df['username'] == volunteer)]
                if len(id_result) != 0:
                    # While loop for category
                    while True:
                        category_choice = str(input("Which category does the report belong to? \n[1] Harassment \n[2] Resources \n[3] Equipment \n[4] Other: \nnPlease select an option: "))
                        if category_choice == '1':
                            category = "Harassment"
                            break

                        elif category_choice == '2':
                            category = "Resources"
                            break
                        
                        elif category_choice =='3':
                            category = "Equiment"
                            break

                        elif category_choice == '4':
                            category = "Other"
                            break

                        else:
                            print("Wrong input. Please enter 1,2,3,or 4")

                    while True:   
                        title = str(input("Please enter the report title: "))
                        if len(title) != 0:
                            break
                        else:
                            print("Please enter a title")
                    while True:       
                        message = str(input("Please enter the report description: "))
                        if len(message) != 0:
                            break
                        else:
                            print("Please provide a description of the report")
                    
                    report_date = date.today().strftime("%Y-%m-%d")
                        
                    report = {'volunteer':volunteer, 'camp_id':camp_id, 'category':category, 'title':title, 'message':message, 'report_time':report_date, 'severity':'Not Graded Yet'}
                    report_list.append(report)
                    answer = input("\nSuccessfully created the report.\nDo you want to create another report? Y/N \n")
                    if answer == 'y' or answer == 'Y':
                        continue
                    else:
                        print("\nHere's the report(s) you've created just now:")
                        df = pd.DataFrame(report_list).fillna("N/A")
                        print(tabulate(df, headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Time", "Severity"], tablefmt='fancy_grid', showindex=False))
                        break
                    #break
                else: 
                    print("The camp ID is invalid, please enter again.")
                    continue
            
           

        # Put the report info into report.csv file. 
        if report_list:
            with open("report.csv", "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['volunteer', 'camp_id', 'category', 'title', 'message', 'report_time', 'severity'])
                for report in report_list:
                    writer.writerow(report)
                print("The report(s) has been created.")
                break

                        
      
def delete_report(user):
    volunteer = user
    while True:
        if os.path.exists("report.csv"):
            df = pd.read_csv("report.csv", header=0)
            my_report = df.loc[df['volunteer'] == volunteer]
            if my_report.empty:
                print("You have not made any reports yet.\n")
                break
            else:
                print("Summary of your reports:")
                print(tabulate(my_report.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=True))
                print("-------------------------------------------------------------------------------")
                
                flag = True
                while flag:
                    try:
                        delete_index = int(input("\nEnter the number of the report that you wish to delete: ")) 
                        total_lines = len(df)
                        if delete_index > (total_lines-1):
                            #if the index is too big, the loop will not break and the user will have to input another value
                            print("This number is greater than the number of reports.")
                        elif delete_index <= -1:
                            #If the index is negative, the loop will also not break
                            print("Negative numbers are not allowed.")
                        elif delete_index >= 0:
                            #the loop will only break if the index is valid
                            flag = False
                            report_df = pd.read_csv('report.csv')
                            selected_rows = report_df[report_df.index == delete_index]
                            if len(selected_rows) == 0:
                                print("No reports.")
                            else:
                                report_df.drop(delete_index, inplace = True)
                                report_df.to_csv('report.csv', index = False)
                                print("\nSuccessfully deleted the report.\n")
                    except ValueError:
                        print("That is not a valid input.\n")

            break

        else:
            print("No reports have been made yet. \n")


def view_my_report(user):
    volunteer = user
    # Check if report.csv exists, if so, print the current volunteer's reports; if not, print "no result found"
    if os.path.exists("report.csv"):
        print("-------------------------------------------------------------------------------")
        
        df = pd.read_csv("report.csv", header=0)
        my_report = df.loc[df['volunteer'] == volunteer]
        #my_report.loc[df['severity'].isnull(), 'severity'] = "Not graded yet"
        if my_report.empty:
            print("You have not made any reports yet.")
        else:
            print("Summary of your reports:")
            my_report.sort_values(by='report_date')
            print(tabulate(my_report.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))

    else:
        print("No reports have been made yet. ")

def view_all_report(user):
    # Check if report.csv exists, if so, print all reports; if not, print "no result found"
    if os.path.exists("report.csv"):
        print("-------------------------------------------------------------------------------")
        print("Summary of all reports:")
        df = pd.read_csv("report.csv", header=0)
        
        if df.empty:
            print("No reports have been made yet.")
        else:
            # Display the table by ascending time order
            print(tabulate(df.sort_values(by='report_date'), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))

    else:
        print("No reports have been made yet. ")



# report_func("volunteer1")

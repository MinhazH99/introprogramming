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
    report_menu()
    volunteer_option = str(input("Option: "))
    while True:
        if volunteer_option in ["0", "1", "2", "3", "4"]:
            if volunteer_option == "0":
                volunteer_home.volunteer_home(user)
                break
            if volunteer_option == "1":
                create_report(user)
                break
            elif volunteer_option == "2":
                delete_report(user)
                break
            elif volunteer_option == "3":
                view_my_report(user)
                break
            elif volunteer_option == "4":
                view_all_report(user)
                break
        else:
            print("Wrong input, please enter a number from 0 to 4")
            volunteer_option = str(input("Option: "))
    # report(user)


def report_menu():
    print("-------------------------------------------------------------------------------")
    print("Report Menu")
    print("[1] Create a New Report")
    print("[2] Delete a Report")
    print("[3] View My Reports")
    print("[4] View All Reports")
    print("[0] Exit")


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
            #volunteerdf = df.loc[df['username'] == volunteer, 'campid'].value_counts().index.values
            volunteerdf = df.loc[df['username'] == volunteer, 'campid']
            showdf = pd.DataFrame(volunteerdf, columns=['Camp ID'])
            print(showdf)
            if volunteerdf.empty:
                print("You are not currently working any shifts, and cannot make a report.\n")
                return
            else:
                
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
                        category_choice = str(input("Which category does the report belong to? \n[1] Harassment \n[2] Resources \n[3] Equipment \n[4] Other: "))

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
                        message = str(input("Please enter the report content: "))
                        if len(message) != 0:
                            break
                        else:
                            print("Please provide a description of the report")
                    
                    report_date = date.today().strftime("%Y-%m-%d")
                        
                    report = {'volunteer':volunteer, 'camp_id':camp_id, 'category':category, 'title':title, 'message':message, 'report_time':report_date, 'severity':'Not graded yet'}
                    report_list.append(report)
                    answer = input("\nSuccessfully created the report.\nDo you want to create another report? Y/N \n")
                    if answer == 'y' or answer == 'Y':
                        continue
                    else:
                        print("\nHere's the report(s) you've created just now:")
                        df = pd.DataFrame(report_list).fillna("None")
                        print(tabulate(df, headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Time", "Severity"], tablefmt='fancy_grid', showindex=False))
                        report_func(user)
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

                        
      
def delete_report(user):
    volunteer = user
    while True:
        if os.path.exists("report.csv"):
            
            df = pd.read_csv("report.csv", header=0)
            my_report = df.loc[df['volunteer'] == volunteer]
            #my_report.loc[df['severity'].isnull(), 'severity'] = "Not graded yet"
            if my_report.empty:
                print("You have not made any reports yet.")
                break
            else:
                print("Summary of your reports:")
                print(tabulate(my_report.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))
                print("-------------------------------------------------------------------------------")
                
                delete_report_title = str(input("Please enter the title of the report that you want to delete: "))
                df = pd.read_csv('report.csv')

                # Search every report from the volunteer that contains the keyword
                contains_keyword = df.loc[(df['title'].str.contains(delete_report_title, case=False)) & (df['volunteer'] == volunteer)]
                if len(contains_keyword) != 0: 
                    # Print out the search result
                    print(tabulate(contains_keyword.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Report Time"], tablefmt='fancy_grid', showindex=True))
                    var = 0
                    while var == 0:
                        try:
                            drop_index = int(input("Please enter the index of the report you want to delete: "))
                            #exact_delete_report_title = input("Please ensure deletion by entering the full title of the report that you want to delete, enter exit to search the report title again: ")
                            # df.drop(df.index[df['title'] == exact_delete_report_title], inplace = True)
                            if drop_index in contains_keyword.index:
                                var = 1
                                df.drop(drop_index, inplace = True)
                                df.to_csv('report.csv', index = False)
                                #if df.drop(df.index[df['title'] == exact_delete_report_title], inplace = True) != None:
                                #if df.drop(drop_index, inplace = True) != None:
                                answer = input("Deleted the report successfully. Continue to delete another report? Y/N \n")
                                if answer == 'Y' or answer == 'y':
                                    continue
                                else:
                                    report_func(user)
                                    break
                    
                            else:
                                print("That is not a valid index.\n")
                                continue
                        except ValueError:
                            print("That is not a valid input.\n")
                    #else:
                        #print("Nothing deleted, going back to search the report title again...")
                else:
                    print("Report not found. ")
                    return
        else:
            print("No reports have been made yet. ")

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
            print("Returning to home screen")
            report_func(user)
        else:
            print("Summary of your reports:")
            print(tabulate(my_report.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))
            while True:
                askUserInput = input("Please enter # to return to report menu")
                if askUserInput == '#':
                    print("Returning to home screen")
                    report_func(user)
                    break
    else:
        print("No reports have been made yet. ")
        print("Returning to home screen")
        report_func(user)


def view_all_report(user):
    # Check if report.csv exists, if so, print all reports; if not, print "no result found"
    if os.path.exists("report.csv"):
        print("-------------------------------------------------------------------------------")
        print("Summary of all reports:")
        df = pd.read_csv("report.csv", header=0)
        #df.loc[df['severity'].isnull(), 'severity'] = "Not graded yet"
        if df.empty:
            print("No reports have been made yet.")
            print("Returning to home screen")
            report_func(user)
        else:
            print(tabulate(df.fillna("None"), headers=["Volunteer Name", "Camp ID", "Category", "Title", "Message", "Report Date", "Severity"], tablefmt='fancy_grid', showindex=False))
            while True:
                askUserInput = input("Please enter # to return to report menu")
                if askUserInput == '#':
                    print("Returning to home screen")
                    report_func(user)
                    break
    else:
        print("No reports have been made yet. ")
        print("Returning to home screen")
        report_func(user)
# report("volunteer2")

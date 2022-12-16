from datetime import datetime as dt
import datetime
import pandas as pd
import numpy as np
import csv
import os.path
import random
from tabulate import tabulate
import sys
import subprocess


#automatically install tabulate
subprocess.Popen(['pip3', 'install', 'secure-smtplib'])
subprocess.Popen(['pip3', 'install', 'Tabulate'])

plan_list = [] #empty list to add emergency plans to
#Dictionary with a list of natural disasters and corresponding 5 or 6-letter codes
disasters_dictionary = {
    "AVALANCHE": "AVLNCH",
    "BLIZZARD": "BLZZRD",
    "DROUGHT": "DROUHT",
    "EARTHQUAKE": "EARTHQ",
    "FLOOD": "FLOOD",
    "FLOODS": "FLOODS",
    "FOREST FIRES": "FORFIR",
    "HAILSTORM": "HAILST",
    "HEATWAVE": "HEATWV",
    "HURRICANE": "HRRCNE",
    "LANDSLIDE": "LNDSLD",
    "MUDSLIDE": "MUDSLD",
    "SANDSTORM": "SANDST",
    "SINKHOLE": "SKHOLE",
    "STORM": "STORM",
    "TORNADO": "TRNADO",
    "TSUNAMIS": "TSUNMI",
    "VOLCANIC ERUPTION": "VOLCNC",
    "WILDFIRES": "WLDFIR"
    }

class CreatePlan:
    def __init__(self, e_type, desc, geo_area, start_date):
        self.e_type = e_type
        self.desc = desc
        self.geo_area = geo_area
        self.start_date = start_date

    def get_e_type(self):
        plan_list.append(self.e_type) #appends the emergency type to the plan list
        
    def get_desc(self):
        plan_list.append(self.desc) #appends the emergency description to the plan list

    def get_geo_area(self):
        plan_list.append(self.geo_area) #appends the geographical area to the list

    def get_start_date(self):
        plan_list.append(self.start_date) #appends the start date to the list

    def get_status(self):
        plan_list.append("Open") #sets the default status of the plan to open


#Function to check whether the start date of the plan is valid
def check_date():
    # a = 0
    while True:
        
        try:
            #global start_date #sets start date to global
            start_date = input("Enter the date on which this occurred in the format yyyy-mm-dd: ")
            datetime.datetime.strptime(start_date, '%Y-%m-%d') #checks whether it is in the correct format, and if it is a valid date

            # a = 1
            return start_date

            
        except Exception:
            print("Not a valid date. ")



def view_plan():
    file_exists = os.path.exists("EmergencyPlans.csv") #checks whether the emergency plans csv file exists
    if file_exists == True:
        print("Summary of all Emergency Plans:\n")
        #if the plan exists, the data is read into a pandas dataframe, converted to a string and printed
        df = pd.read_csv("EmergencyPlans.csv")
        
        print(tabulate(df, headers = 'keys', tablefmt = 'fancy_grid'))
    else:
        #if the file does not exist the program will let the user know and go back to the main function
        print("There are currently no plans to view.\nPlease create a plan first.") 
        
#does the same as the view_plan function, except for the camp details file
def view_camps():
    camp_file_exists = os.path.exists("CampDetails.csv")
    if camp_file_exists == True:
        var = 1
        while var == 1:
            camp_opt = input("Enter:\n[1] to view the camp details for a specific Emergency Plan\n[2] to view all the camp details\n")
            if camp_opt == '1':
                var = 2
                view_plan()
                while var == 2:
                    try:
                        plan_index = int(input("\nEnter the number of the plan whose camps you wish to view: "))    
                        total_lines = sum(1 for line in open("EmergencyPlans.csv"))-1
                        if plan_index > (total_lines-1):
                            #if the plan index is too big, the loop will not break and the user will have to input another value
                            print("This number is greater than the number of plans.")
                        elif plan_index <= -1:
                            #If the plan index is negative, the loop will also not break
                            print("Negative numbers are not allowed.")
                        elif plan_index >= 0:
                            #the loop will only break if the plan index is valid
                            var = 3
                            camp_df = pd.read_csv("CampDetails.csv")
                            selected_rows = camp_df[camp_df['Emergency Plan Index'] == plan_index]
                            print("Refugee camps for selected plan:\n")
                            print(tabulate(selected_rows, headers = 'keys', tablefmt = 'fancy_grid'))
                            
                    except ValueError:
                        print("That is not a valid input.\n")
            
            elif camp_opt == '2':
                var = 0
                print("Summary of all refugee camps:\n")

                camp_df = pd.read_csv("CampDetails.csv")
                #print(camp_df.to_string())
                print(tabulate(camp_df, headers = 'keys', tablefmt = 'fancy_grid'))
                
            else:
                print("That is not a valid input.\n")
        
    else:
        print("There are currently no camp details to view.\nPlease assign a number of camps to an emergency plan first.")

def view_volunteers():
    volunteer_file_exists = os.path.exists("volunteers_db.csv")
    if volunteer_file_exists == True:
        var = 1
        while var == 1:
            vol_opt = input("Enter:\n[1] to view the volunteers for a specific Emergency Plan\n[2] to view all the volunteer details\n")
            if vol_opt == '1':
                var = 2
                view_plan()
                while var == 2:
                    try:
                        plan_index = int(input("\nEnter the number of the plan whose volunteers you wish to view: "))    
                        total_lines = sum(1 for line in open("EmergencyPlans.csv"))-1
                        if plan_index > (total_lines-1):
                            #if the plan index is too big, the loop will not break and the user will have to input another value
                            print("This number is greater than the number of plans.")
                        elif plan_index <= -1:
                            #If the plan index is negative, the loop will also not break
                            print("Negative numbers are not allowed.")
                        elif plan_index >= 0:
                            #the loop will only break if the plan index is valid
                            var = 3
                            vol_df = pd.read_csv("volunteers_db.csv")
                            selected_rows = vol_df[vol_df['emergencyplanindex'] == plan_index]
                            if selected_rows.empty:
                                print("There are currently no volunteers associated with this plan index.")
                            else:

                                print("Volunteers for selected plan:\n")
                                print(tabulate(selected_rows, headers = 'keys', tablefmt = 'fancy_grid'))
                            
                    except ValueError:
                        print("That is not a valid input.\n")
            
            elif vol_opt == '2':
                var = 0
                vol_df = pd.read_csv("volunteers_db.csv")
                if vol_df.empty:
                    print("There are currently no volunteers associated with any plan")
                else:
                    print("Summary of all volunteers:\n")
                    print(tabulate(vol_df, headers = 'keys', tablefmt = 'fancy_grid'))

                    
            else:
                print("That is not a valid input.\n")
        
    else:
        #if the file does not exist the program will let the user know and go back to the main function
        print("There are currently no volunteers assigned to camps.\n") 
  
        
#This function takes the natural disaster as a parameter
def search_dict(nat_disaster):
    #This searches the dictionary to check if the natural disaster is present
    if nat_disaster.upper() in disasters_dictionary:
        #if the natural disaster is in the dictionary, the corresponding 5/6 letter code is returned
        dis_code = disasters_dictionary[nat_disaster.upper()]
        return dis_code
    else:
        loop = 0
        print("Disaster not found.")
        while loop == 0:
            #the user needs to input a 5 or 6 letter code, and the loop will not break unless this is satisfied
            dis_code = input("Please input a 5 or 6 letter code for this disaster: ")
            if dis_code.isalpha() and len(dis_code) == (5 or 6):
                loop = 1
                #the code is returned for use in another function
                return dis_code
            else:
                print("Not a valid input.\n")

#This is a function for editing the number of camps associated with a plan
#It takes the inputted number of camps, the 5 or 6 letter code, the emergency plan index,
#the natural disaster name, and the current number of camps as paramaters
                
def edit_camp(no_camps, code, index, nat_disaster, current_no_camps):

    
    #This reads the Camp Details file, and counts the number of rows where the emergency plan index
    # is the same as the one in the paramater
    camp_df = pd.read_csv("CampDetails.csv")
    selected_rows = camp_df[camp_df['Emergency Plan Index'] == index]
    num_rows = len(selected_rows)
    #This lets the user know how many camps there currently are, if the number of camps is greater than 0
    print("There are currently " + str(current_no_camps)+ " camps for this plan.\n")
    opt = input("Enter:\n[1] if you would like to change the number of plans\n[2] to quit\n")
    var = 0
    while var == 0:
        #This if statement checks if the user wants to change the number of plans
        if opt == '1':
            
            #the csv file with the emergency plans is read
            df = pd.read_csv("EmergencyPlans.csv")
            if int(no_camps) == num_rows:
                print("The new number of camps cannot be the same as the previous number.\nPlease enter a different number in the edit plans section")
                
                
            #if the new number of camps is greater, it will generate new camp ids
            elif int(no_camps) > num_rows:
                var = 1
                df.loc[index,'No. Camps Available']=str(no_camps) #Adds number of camps to plan
                df.to_csv("EmergencyPlans.csv", index = False)
                #the difference between the new and old number is calculated
                diff = int(no_camps) - num_rows
                for camp in range(0, diff):
                    #the Camp details file is read for each number, to check that the new camp IDs are unique
                    camp_df = pd.read_csv("CampDetails.csv")
                    camp_list = [] #empty list for the camp details
                    camp_total = [] #empty list to add the camp list to
                    
                    num = 1
                    #num is used to generate various new camp IDs.
                    camp_id = code.upper() + search_dict(nat_disaster) +str(index) + "_" +str(num)
                    #Camp ID is generated from concatenated strings
                    if camp_id in camp_df['Camp ID'].unique():
                        #if the camp ID is already in the dataframe
                        # a while loop is used to increment num, until the camp ID is not already taken
                        while camp_id in camp_df['Camp ID'].unique():
                            num += 1
                            camp_id = code.upper() + search_dict(nat_disaster) +str(index) + "_" +str(num)
                        #Once the program breaks out of the while loop, the details are appended to the camp list
                        camp_list.append(camp_id)
                        camp_list.append("0")
                        camp_list.append("0")
                        camp_list.append(index)
                        ##the camp list is added to the camp total list, so that a numpy array can be generated
                        camp_total.append(camp_list)
                        camp_np = np.array(camp_total)
                        #the numpy array is converted to a dataframe, and appeneded to the bottom of the Camp Details csv file
                        camp_row = pd.DataFrame(camp_np)
                        camp_row.to_csv("CampDetails.csv", mode="a", index = False, header = False)

                    else:
                        #if the camp ID is already unique, num is still incremented for the next ID
                        #The camp details are appended in the same way as before
                        num += 1
                        camp_list.append(camp_id)
                        camp_list.append("0")
                        camp_list.append("0")
                        camp_list.append(index)
                        
                        camp_total.append(camp_list)
                        camp_np = np.array(camp_total)
                        
                        camp_row = pd.DataFrame(camp_np)
                        camp_row.to_csv("CampDetails.csv", mode="a", index = False, header = False)
                        
            else:
                var = 1
                df.loc[index,'No. Camps Available']=str(no_camps) #Adds number of camps to plan
                df.to_csv("EmergencyPlans.csv", index = False)
                #displays all the refugee camps for the selected emergency plan, so that the user can select the one they want to delete
                print("Refugee camps for selected plan:\n")
                print(tabulate(selected_rows, headers = 'keys', tablefmt = 'fancy_grid'))
                loop = 0
                #difference between desired and current number of camps is calculated
                diff = num_rows - int(no_camps)
                while loop < diff:
                    delete_id = input("Please enter the camp ID of the camp you want to delete: ")
                    #if the camp ID entered is in the selected rows dataframe, the row will be dropped
                    #The csv file is then updated without the enetered Camp ID row
                    if delete_id.upper() in camp_df['Camp ID'].unique():
                        loop += 1
                        camp_df.drop(camp_df[camp_df['Camp ID'] == delete_id.upper()].index, inplace = True)
                        camp_df.to_csv("CampDetails.csv", mode="w", index = False, columns = ['Camp ID','No. Volunteers', 'No. Refugees', 'Emergency Plan Index'])
                        
                    else:
                        print("That is not a valid camp ID.\n")

        elif opt == '2':
            #breaks out of while loop, and returns to main menu
            var = 1
        else:
            #doesnt break out of the loop as the input is invalid
            print("That is not a valid option")
    
       
#function to add camp IDs to the camp details file, if the current number of camps is 0
            
def add_to_camp(no_camps, code, index, nat_disaster):
    #generates camp IDs from 1 to the number of camps desired, and adds this to the file
    for camp in range(1, no_camps+1):
        camp_list = []
        camp_total = []
        num_camp_lines = sum(1 for line in open("CampDetails.csv","r"))
        
        camp_id = code.upper() + search_dict(nat_disaster) +str(index) + "_" +str(camp)
        camp_list.append(camp_id)
        camp_list.append("0")
        camp_list.append("0")
        camp_list.append(index)

        camp_total.append(camp_list)
        camp_np = np.array(camp_total)
        #if there are currently no lines in the Camp Details file, the column names are included when appeding to the file
        #otherwise, the row is just added by itself
        if num_camp_lines == 0:
            camp_row = pd.DataFrame(camp_np, columns = ['Camp ID','No. Volunteers', 'No. Refugees', 'Emergency Plan Index'])
         
            camp_row.to_csv("CampDetails.csv", mode="a", index = False)
              
        else:
            camp_row = pd.DataFrame(camp_np)
            
            camp_row.to_csv("CampDetails.csv", mode="a", index = False, header = False)
    
#A function to check whether the area code inputted by the user is valid
def check_area_code(area_name):
    #if the length of the area is greater than 3, it will ask the user for a code
    # otherwise the code is the same as the name, e.g USA  
    if len(area_name) > 3:
        loop_var = 0
        while loop_var == 0:
            area_code = input("Please input a 3 letter code for the area: " + str(area_name)+"\n")
            #if the code contains only letters, and has a length of 3, the code is returned
            #otherwise, the program will keep asking for a code until the input is valid
            if area_code.isalpha() and len(area_code) == 3:
                loop_var = 1
                
                return area_code
                
   
            else:
                print("The area code can only contain 3 letters.\n")
        
    else:
        area_code = area_name
        return area_code

#This function opens a new file Camp details if it does not currently exist
# It is called if the number of camps on a plan the user wants to edit is 0
def camp_details(index):
    new_camp_file = open("CampDetails.csv", "a")
    
    new_camp_file.close()
    
    #The area name, disaster type and number of camps are read and passed to the add to camp function as parameters
    df = pd.read_csv("EmergencyPlans.csv")
    area = df.loc[index, 'Geographical Area']
    disaster = df.loc[index, 'Emergency Type']
    num_camps = df.loc[index,'No. Camps Available']
    area_code = df.loc[index, 'Area Code']
               
    add_to_camp(num_camps, area_code, index, disaster)
    print("Refugee camps have successfully been created for plan " + str(index) + " and can now be viewed.")                  
        
#This function is called if the user wants to edit the emergency plan details

def retrieve_data():
    #The function first checks if any plans exist using the view plan function
    #If there are any plans to edit, the function will output all of them, otherwise it will return to the main menu
    file_exists = os.path.exists("EmergencyPlans.csv") #checks whether the emergency plans csv file exists
    if file_exists == True:
    #the plans are read and stored in a pandas dataframe
        df = pd.read_csv("EmergencyPlans.csv")
        print("Summary of all Emergency Plans:\n")
        #if the plan exists, the data is read into a pandas dataframe, converted to a string and printed
        
        print(tabulate(df, headers = 'keys', tablefmt = 'fancy_grid'))
        
        var = 0
        while var == 0:
            #while loop and try-except is used to ensure the user enters a valid user input
            try:
                plan_index = int(input("\nEnter the number of the plan you wish to edit: "))            
                #The number of lines in the emergency plans file is calculated, -1 because of the line with column names
                total_lines = sum(1 for line in open("EmergencyPlans.csv"))-1
                if plan_index > (total_lines-1):
                    #if the plan index is too big, the loop will not break and the user will have to input another value
                    print("This number is greater than the number of plans.")
                elif plan_index <= -1:
                    #If the plan index is negative, the loop will also not break
                    print("Negative numbers are not allowed.")
                elif plan_index >= 0:
                    #the loop will only break if the plan index is valid
                    var = 1
                
                    while var == 1:
                        #user is presented with options about how they want to edit the plan
                        print("\nEnter:\n[1] to add/edit a closing date\n[2] to add/edit the number of camps\n[3] to close the emergency plan")
                        decision = input("[4] to edit a different plan\n[5] to quit\n")
                        if decision == '1':
                            #the user is adding a close date
                            #a while loop similar to that in the check date function is used to check whether the date is valid
                            #an additional comparison with the start date is carried out, to ensure that the close date is after the start date
                            var = 2
                            while var == 2:
                                try:
                                    #reads and stores the starting date from the dataframe
                                    starting_date = df.loc[plan_index, 'Start Date']
                                    closing_date = input("Enter the date on which this plan was closed in the format yyyy-mm-dd: ")
                                    
                                    datetime.datetime.strptime(closing_date, "%Y-%m-%d")
                                    if starting_date >= closing_date:
                                        print("\nThe start date cannot be after or equal to the close date.\n")
                                    else:
                                        #if the close date is valid and after the start date, it is added to the emergency plan in the csv file
                                        df.loc[plan_index, 'Close Date'] = str(closing_date)
                                        df.to_csv("EmergencyPlans.csv", index = False)
                                        var = 3
                                        print("The closing date '" + str(closing_date) + "' has been added to plan " + str(plan_index)+"\n")

                                except Exception:
                                    print("Not a valid date.\n")

                        elif decision == '2':
                            var = 2
                            while var == 2:
                                try:
                                    num_camps = input("Enter the number of camps available for this emergency: ")
                                    #uses while and try except to ensure that the user enters a positive number for the number of camps
                                    if int(num_camps) <= 0:
                                        print("That is not a valid number.\n")
                                    else:
                                        current_camps = df.loc[plan_index,'No. Camps Available']
                                        #current number of camps is read, and while loop is broken in both cases below
                                        if current_camps == 0:
                                            #if the current number of camps is 0, it will execte the add to camps function
                                            df.loc[plan_index,'No. Camps Available']=str(num_camps) #Adds number of camps to plan
                                            df.to_csv("EmergencyPlans.csv", index = False)
                                            var = 3
                                            camp_details(plan_index)
                                            
                                        else:
                                            #if the number is greater than 0, key data is read from the csv file, and passed as paramaters to the edit camp function
                                            df = pd.read_csv("EmergencyPlans.csv")
                                            area = df.loc[plan_index, 'Geographical Area']
                                            disaster = df.loc[plan_index, 'Emergency Type']
                                            area_code = df.loc[plan_index, 'Area Code']

                                            edit_camp(num_camps, area_code, plan_index, disaster, current_camps)
                                            print("The number of refugee camps has been changed for plan " + str(plan_index))
                                            var = 3
            
                                except ValueError:
                                    print("Not a valid input.\n")
                                                    
                        elif decision == '3':
                            #Changes the status on the desired row to closed and breaks loop
                            var = 2
                            df.loc[plan_index,'Status']="Closed" 
                            df.to_csv("EmergencyPlans.csv", index = False)
                            curr_date = dt.today().strftime('%Y-%m-%d')
                            close = df.loc[plan_index, 'Close Date']
                            if close == " ":
                                #if the closing date is blank, today's date is automatically added 
                                df.loc[plan_index, 'Close Date'] = str(curr_date)
                                df.to_csv("EmergencyPlans.csv", index = False)
                                print("The plan is now closed.")
                                print("The closing date " + str(curr_date) + " has been automatically added, as no closing date was present before.\n")
                            else:

                                print("The plan is now closed.")

                        elif decision == '4':
                            #returns to start of function to enter a different plan index to edit
                            var = 0
                        elif decision == '5':
                            #breaks out of loop and returns to main menu
                            var = 2
                            
                        else:
                            #Program does not accept any other input
                            print("Not a valid input")
            except ValueError:
                print("That is not a valid input")
    else:
        #if the file does not exist the program will let the user know and go back to the main function
        print("There are currently no plans to edit.\nPlease create a plan first.") 
    

def view_report():
    report_file_exists = os.path.exists("report.csv")
    if report_file_exists == True:
        print("Summary of all Reports:\n")
        #if the plan exists, the data is read into a pandas dataframe, converted to a string and printed
        df = pd.read_csv("report.csv")
        
        print(tabulate(df, headers = 'keys', tablefmt = 'fancy_grid'))
    else:
        print("No reports have been made yet.\n")

def add_severity(df, r_index):
    while True:
        severity = input("Enter:\n[1] Critical\n[2] Major\n[3] Moderate \n[4] Minor \n[5] Cosmetic\n")
        if severity == '1':
            df.loc[r_index,'severity']="Critical" 
            df.to_csv("report.csv", index = False)
            return
        elif severity == '2':
            df.loc[r_index,'severity']="Major" 
            df.to_csv("report.csv", index = False)
            return
        elif severity == '3':
            df.loc[r_index,'severity']="Moderate" 
            df.to_csv("report.csv", index = False)
            return
        elif severity == '4':
            df.loc[r_index,'severity']="Minor" 
            df.to_csv("report.csv", index = False)
            return
        elif severity == '5':
            df.loc[r_index,'severity']="Cosmetic" 
            df.to_csv("report.csv", index = False)
            return
        else:
            print("Not a valid input.\n")

def assign_severity():
    report_file_exists = os.path.exists("report.csv")
    if report_file_exists == True:
        rep_df = pd.read_csv("report.csv")
        print(tabulate(rep_df,headers = 'keys', tablefmt = 'fancy_grid'))
        while True:
            
            try:
                report_index = int(input("\nEnter the number of the report you wish to assign a severity to: ")) 
                
                total_lines = sum(1 for line in open("EmergencyPlans.csv"))-1
                if report_index > (total_lines):
                    #if the plan index is too big, the loop will not break and the user will have to input another value
                    print("This number is greater than the number of plans.")
                elif report_index <= -1:
                    #If the plan index is negative, the loop will also not break
                    print("Negative numbers are not allowed.")
                elif report_index >= 0:
                    #the loop will only break if the plan index is valid
                    val = pd.isnull(rep_df.loc[report_index,'severity'])

                    if val == True:
                        add_severity(rep_df, report_index)
                        break
                        
                    else:
                        print("This report already has the severity level: ",rep_df.loc[report_index,'severity'])
                        opt = input("\nEnter:\n[1] to change the severity level\n[2] to quit\n")
                        if opt == '1':
                            add_severity(rep_df, report_index)
                            break
                        elif opt == '2':
                            break
                        
                        else:
                            print("Not a valid input.")


            except ValueError:
                print("That is not a valid input.\n")
    else:
        print("There are currently no reports to assign a severity to.")

#function for the main menu
def adminFeatures():       
    b = 0
    while b == 0:
        print("\nEnter:\n[1] to create a plan\n[2] to view a plan\n[3] to edit a plan\n[4] to view camp details\n[5] to view volunteer details")   
        option = input("[6] to view reports made by volunteers\n[7] to assign a severity level to a report\n[8] to quit\n")
        if option == '1':
            #the plan list is cleared, so that a new plan can be created
            plan_list.clear()
            total = []
            #asks the user to input various details about the new plan
            e_type = input("Enter the emergency type: ")
            desc = input("Enter a description of the emergency: ")
            geo_area = input("Enter the affected geographical area(s)\nPlease separate areas using commas: ")
            #jumps to the check date function
            #check_date()
            b = 0
            disaster = CreatePlan(e_type, desc, geo_area, check_date())
            #appends all the properties to the plan list
            disaster.get_e_type()
            disaster.get_geo_area()
            
            disaster.get_start_date()
            disaster.get_desc()
            plan_list.append(check_area_code(geo_area))#Adds a 3 letter code for the geographic area
            plan_list.append("0") #default number of camps is 0
            plan_list.append(" ") #close date is blank initially
            disaster.get_status()
            
            total.append(plan_list)
            #plan list is added to total list so that a numpy array, and dataframe can be created as a result
            total_np = np.array(total)
            #opens the file emergency plans, and counts the number of lines
            new_file = open("EmergencyPlans.csv", "a")

            num_lines = sum(1 for line in open("EmergencyPlans.csv","r"))
            new_file.close()
            #if the number of lines is 0, the column names are added
            if num_lines == 0:
                num_lines = 1
                row = pd.DataFrame(total_np, columns = ['Emergency Type', 'Geographical Area', 'Start Date', 
                                                        'Description', 'Area Code', 'No. Camps Available', 'Close Date', 'Status'])
             
                row.to_csv("EmergencyPlans.csv", mode="a", index = False)
                
            else:
                row = pd.DataFrame(total_np)
                
                row.to_csv("EmergencyPlans.csv", mode="a", index = False, header = False)
                          

        elif option == '2':
           
            view_plan()
            
        elif option == '3':
            
            retrieve_data()
            
        elif option == '4':
            
            view_camps()
            
        elif option == '5':
            
            view_volunteers()
            
        elif option == '6':
            view_report()

        elif option == '7':

            assign_severity()
        elif option == '8':
            b = 1
        else:
            #loop is not broken and user is asked for input again
            print("Not a valid input. Please try again.\n ")
# adminFeatures()
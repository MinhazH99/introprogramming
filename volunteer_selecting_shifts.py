import pandas as pd
from datetime import date, timedelta
import csv

# #Creating CSV files for day and night shifts - would make empty fields, most likely,
# #or just populate with available dates, or null values or something
# #explore dataframes
# #using approach from - https://www.geeksforgeeks.org/writing-csv-files-in-python/

#If we wanted auto-generation of possible shifts (could get complicated):

#Unsuccessful attempt at unction to generate the next 30 days

# def daterange(date1, date2):
#     coming_dates = []
#     for n in range(int((date2 - date1).days) + 1):
#         print(int((date2 - date1).days) + 1)
#         date_to_add = date1 + timedelta(n)
#         print(date_to_add)
#         print([date_to_add])
#         coming_dates += [date_to_add]
#         return coming_dates
    

#if [1]:

#TODO: Get range of next 30 days

#TODO: If signing up for more than one shift on same day: raise error "No two consecutive shifts" - watch out, for overnight shifts more complexity
#Shouldn't be too bad - start time of one shift is end time of previous, i.e. relationship between current and previous/ current and next row always holds,
#except for first and last rows


#command to check whether *any* row in dataframe has this row already
# day_shifts_df = pd.read_csv('day_shifts.csv')
# print(day_shifts_df.loc[[0, 1]])

# night_shifts_df = pd.read_csv('day_shifts.csv')

# print( ((day_shifts_df['Date'] == '2022-11-28')
# & (day_shifts_df['Time'] ==  '09:00 - 19:00')
# & (day_shifts_df ['Volunteer username'] == 'Volunteer1')).any())


#for the time being, getting username of user manually
#once integrated with login, should be retrieved automatically

#get usernames from existing test_file.csv - make this a class variable/ global variable?

# class selectShifts:
#     """Class containing methods for users to view and add shifts (at present, no option to remove them).
#     Also contains utility methods for use within these main methods."""


#     #for raising exceptions - could probably achieve using datetime function instead
#     valid_days = [i for i in range(1,32)]
#     valid_months = [i for i in range(1,13)]
#     valid_years = [2022, 2023]

def list_of_existing_users():
    '''Gets list of existing users from test_file.csv'''
    username_list = []
    test_file = open('test_file.csv', 'r')
    for line in test_file:
        part = line.split(',') # creates list of strings separated by / from the line
        a = part[3]
        username_list += [a]
    return username_list



#Use the following function to select editing of day shifts or night shifts. 
#Based on that choice, affects the files edited by availability_funcs

def select_shift_type():
    shift_type = {'Day shifts': 0, 'Night shifts': 1, 'Exit': 2}
    action = int(input(f"Edit day shifts or night shifts?:\n\
    Day shifts: [{shift_type['Day shifts']}]\n\
    Night shifts: [{shift_type['Night shifts']}]\n\
    Exit: [{shift_type['Exit']}] \n"))
    
    if action == 0:
        choice = 'day'
    elif action == 1:
        choice = 'night'
    elif action == 2:
        print('Goodbye')
    else: #error handling
        pass
    shifts_df = pd.read_csv(f'{choice}_shifts.csv')
    # print(f"Opening '{choice}_shifts.csv'")
    return shifts_df

def write_to_day_file(dt, username):
    '''Function for writing to day_shifts.csv, since the number of columns differs between the two'''
    filename = "day_shifts.csv"
    with open(filename, 'a+') as csvfile: #closes file after use
        #creating a CSV write object-
        csvwriter = csv.writer(csvfile)
        #writing the fields
        new_day_shift = [f'{dt}', '09:00 - 19:00', f'{username}']
        csvwriter.writerow(new_day_shift)
        print("New shift successfully selected!")

#Currently not working 0 not sure of the issue, should be identical to day shifts
def write_to_night_file(dt, username):
    '''Function for writing to night_shifts.csv, since the number of columns differs between the two'''
    filename = "night_shifts.csv"
    next_dt = dt + timedelta(1)
    with open(filename, 'a+') as csvfile: #closes file after use
        #creating a CSV write object-
        csvwriter = csv.writer(csvfile)
        #writing the fields
        new_night_shift = [f'{dt}', f'{next_dt}' '19:00 - 09:00', f'{username}']
        csvwriter.writerow(new_night_shift)
        print("New shift successfully selected!")


def availability_funcs(user):
    shifts_df = select_shift_type() #makes dataframe from different csv files depending on shift type selected (day or night)
    '''Method for user to view current shifts or add new shifts'''
    #again, would need to incorporate select_shift_type
    username = user
    options = {'View current shifts': 0, 'Add new shift': 1, 'Exit': 2}
    # action = int(input(f"Please select one of the following personal details to change:\n\
    # View current shifts: [{options['View current shifts']}]\n\
    # Add new shift: [{options['Add new shift']}]\n\
    # Exit: [{options['Exit']}] \n"))
    action = int(input("Please select one of the following personal details to change:"))
    print("[0] View current shifts")
    print("[1] Add new shift")
    print("[2] Exit")

    if action == 0:
        #Print all rows where current shifts are in 
        shifts = shifts_df.loc[shifts_df['Volunteer username'] == f'{username}']
        if shifts.empty:
            print('No shifts at present')
        else: 
            print(shifts_df.loc[shifts_df['Volunteer username'] == f'{username}'])
            
        print('\n')
        availability_funcs()

    elif action == 1:
        #Turn into a function so I can call the function repeatedly
        #File should be for getting a date AND writing to CSV, call repeatedly in here until user leaves
        #When user leaves, return to main function/ dict for (0) other actions within availability, (1) main menu, (2) exit
        print("You will be asked for the details of the shift you are signing up for")
        y = int(input("Please enter a year as a single integer: "))
        m = int(input("Please enter a month as a single integer, with no leading 0's (e.g., '1', not '01): "))
        d = int(input("Please enter a day as a single integer, with no leading 0's (e.g., '1', not '01): "))

        try:
            dt = date(y, m, d)
        except ValueError:
            print('Invalid date format') #add a line so the user has to retry until they exit or choose a valid date
        
        if len(shifts_df.columns) == 3: #then choice made has been day shifts
            decision = int(input(f"Sign up for a shift on {dt} at 09:00 - 19:00?\n\
            No: [0]\n\
            Yes: [1]\n" ))
            if decision == 0:
                availability_funcs()
            elif decision == 1:
                write_to_day_file(dt, username)
                availability_funcs()
            else: #error handling
                pass
        elif len(shifts_df.columns) == 4: #then choice made has been night shifts
            decision = int(input(f"Sign up for a shift from {dt} at 19:00 to {dt + timedelta(1)} at 09:00?\n\
            No: [0]\n\
            Yes: [1]\n" ))
            if decision == 0:
                availability_funcs()
            elif decision == 1:
                write_to_night_file(dt, username)
                availability_funcs()
            else: #error handling
                pass


        #Extra features:
        #if date before today:
        #add to list of prior dates
        #print ("prior dates: \n")
        #print out each date in list
        #else:
        #print("Today onwards: \n")
        #print out each date in list
        #Ask user to select year, month, day
        #If tuple is before today: print(date is in past)
        #if tuple is today: print(can't book shifts for current date! Must give advance notice)
        #If tuple is more than 30 days in advance: print("Can't book more than 30 days in advance")
        #Else:
        #Check if tuple in csv file
        #If so: print("You have already signed up for this time. Pick another time?") If yes, restart function. If not, exit
        #If not: add row to csv file. If done successfully, print appropriate message
        pass
    #TODO: if row[date] not in csv file: add row to file (assuming ≤ 30 days)
    #TODO: elif row in file: If count(row[volunteer]) < 5: insert new row. Else: return 'no slots available on this date. Please pick another' (max. number of volunteers present at a time)

    elif action == 2:
        print("Goodbye")
    else: #error handling
        pass

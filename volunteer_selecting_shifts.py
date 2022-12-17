import pandas as pd
from datetime import date, datetime, timedelta
import csv
from tabulate import tabulate
import volunteer_home

#to avoid FutureWarning about the coming deprecation of the .append method for Pandas dataframes
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#Custom errors
class DuplicateError(Exception):
    '''Raises an error when a user tries to sign up for an existing shift'''
    pass

class ConsecutiveShiftError(Exception):
    '''Raises an error when a user tries to sign up for consecutive shifts'''
    pass

#Functions for use within volunteer options

def check_duplicates(df, start_date, end_date):
    """Checks if a user has already signed up for a given shift. 
    I think we should band together all the validation functions for each file into one class to demonstrate OOP"""
    if ((df['startdate'] == f'{start_date}') & (df['enddate'] == f'{end_date}')).any():
        return True
    elif ((df['startdate'] == f'{start_date}') & (df['enddate'] == f'{end_date}')).any():
        pass
    else: 
        return False

def check_successive_shifts(df, shift_type, start_date, end_date):
    """Checks if a user has signed up for successsive shifts."""
    if shift_type == '1':
        #Case 1: a night shift ends before - its end date is this start date, and its time is 19:00 - 09:00
        if ((df['enddate'] == f'{start_date}') & (df['time'] == '19:00 - 09:00')).any():
            return True
        #Case 2: a night shift starts after this shift - its end date is this start date, and its time is 19:00 - 09:00
        elif ((df['startdate'] == f'{end_date}') & (df['time'] == '19:00 - 09:00')).any():
            return True
    elif shift_type == '2':
        #Case 1: a day shift starts before - its end date is this start date, and its time is 09:00 - 19:00
        if ((df['enddate'] == f'{start_date}') & (df['time'] == '09:00 - 19:00')).any():
            return True
        # #Case 2: a day shift starts after - its start date is this end date, and its time is 09:00 - 19:00
        elif ((df['startdate'] == f'{end_date}') & (df['time'] == '09:00 - 19:00')).any():
            return True
    return False

def too_many_volunteers():
    '''Checks if a camp is already at its staffing limit'''
    pass
    #TODO: elif row in file: If count(row[volunteer]) < 5: insert new row. 
    #Else: return 'no slots available on this date. Please pick another' (max. number of volunteers present at a time)

def write_to_file(new_shift):
    '''Function for writing to new shifts to shifts.csv'''
    filename = "shifts.csv"
    with open(filename, 'a+') as csvfile: #closes file after use
        #creating a CSV write object-
        csvwriter = csv.writer(csvfile)
        #writing the fields
        csvwriter.writerow(new_shift)
        print("New shift successfully selected!")

def select_shift_type():
    '''Allows volunteer to select shift type'''
    print("-------------------------------------------------------------------------------")
    print("Which type of shift would you like to interact with?")
    print("[1] Day shifts")
    print("[2] Night shifts")
    print("[3] Return to main menu")

    shift_type = input("Please select an option: ").strip()
    while True:
        if shift_type == '1':
            break
        elif shift_type == '2':
            break
        elif shift_type == '3':
            print("Returning you now: ")
            break
        else: #error handling
            print("Please enter a valid input.")
        shift_type = input("Please select an option: ").strip()
    return shift_type

#TODO: create main menu here that can be
#TODO: let Minhaz know this will need linking to main menu for volunteers


def view_shifts(df, volunteer_shifts_df, username):
    '''Function for a volunteer to view their current shifts'''
    past_shifts_df = pd.DataFrame(columns = volunteer_shifts_df.columns)
    today_shifts_df = pd.DataFrame(columns = volunteer_shifts_df.columns)
    future_shifts_df = pd.DataFrame(columns = volunteer_shifts_df.columns)

    #Dataframe of all rows where current shifts are in 
    shifts = volunteer_shifts_df.loc[df['username'] == f'{username}']
    shifts.sort_values(by='startdate', inplace=True) #sorts by start date
    
    # print(tabulate(shifts, headers=["Start Date", "End Date", "Time", "Username", "Emergency Plan Index", "Camp ID"], tablefmt='fancy_grid', showindex=False))
    # for ind in shifts.index:
    #     print(shifts.loc[ind])

    if shifts.empty:
        print('No shifts at present')
    else: 
        print('\n')
        for ind in shifts.index:
            a = shifts.loc[ind]
            b = a.values.tolist()
            b[0] = b[0].date()
            b[1] = b[1].date()
            b_series = pd.Series(b, index = volunteer_shifts_df.columns)
            
            if b[0] < date.today():
                past_shifts_df = past_shifts_df.append(b_series, ignore_index = True)
            elif b[0] == date.today():
                today_shifts_df = today_shifts_df.append(b_series, ignore_index = True)
            elif b[0] > date.today():
                future_shifts_df = future_shifts_df.append(b_series, ignore_index = True)
        
        table_headers = ["Start Date", "End Date", "Time", "Username", "Emergency Plan Index", "Camp ID"]

        if len(past_shifts_df.index) > 0:
            print("Past shifts:\n")
            # print(past_shifts_df)
            print(tabulate(past_shifts_df, headers=table_headers, tablefmt='fancy_grid', showindex=False))
            print('\n')
        if len(today_shifts_df.index) > 0: 
            print("Today's shifts:\n")
            # print(today_shifts_df)
            print(tabulate(today_shifts_df, headers=table_headers, tablefmt='fancy_grid', showindex=False))
            print('\n')
        if len(future_shifts_df.index) > 0: 
            print("Future shifts:\n")
            # print(future_shifts_df)
            print(tabulate(future_shifts_df, headers=table_headers, tablefmt='fancy_grid', showindex=False))
            print('\n')

def add_new_shift(shift_type, volunteer_shifts_df, username, camp_id, emergency_plan_index):
    '''Function for users to add a new shift'''
    print("You will be asked for the details of the shift you are signing up for. \n")

    now = date.today()
    thirty_days_time = (date.today() + timedelta(30)) 
        
    date_input = input(f'Please enter a date (YYYY-MM-DD) between {now} and {thirty_days_time}: ')

    try:
        # Convert the string input to datetime object, it will catch error if you enter a unvalid date like 2020-12-40
        start_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        # Limit the date_input to dates between today and thirty days' time
        
        if not (now <= start_date <= thirty_days_time):
            raise ValueError
        else:
            # print("The date you entered ->%f<- is valid", date_input)
            # You can write the date_input to csv file.
            pass

        if shift_type == '1':
            print(f"Sign up for a shift on {start_date} from 09:00 to 19:00?")
            print("[0] No")
            print("[1] Yes\n")
            decision = input("Please select an option: ").strip()
            print('\n')
        elif shift_type == '2':
            print(f"Sign up for a shift from {start_date} at 19:00 to {start_date + timedelta(1)} at 09:00?")
            print("[0] No")
            print("[1] Yes \n")
            decision = input("Please select an option: ").strip()
            print('\n')

        if decision == '0':
            pass #returns to availability_funcs, which is called after this function executes
        elif decision == '1':

            if shift_type == '1':
                end_date = start_date
                shift_time = '09:00 - 19:00'
            elif shift_type == '2':
                end_date = start_date + timedelta(1)
                shift_time = '19:00 - 09:00'

            new_shift = [f'{start_date}', f'{end_date}', f'{shift_time}', f'{username}', f'{emergency_plan_index}', f'{camp_id}']

            try:
                if check_duplicates(volunteer_shifts_df, start_date, end_date):
                    raise DuplicateError
                if check_successive_shifts(volunteer_shifts_df, shift_type, start_date, end_date):
                    raise ConsecutiveShiftError
                else:
                    write_to_file(new_shift)

            except DuplicateError:
                print("You have already signed up for this shift. Please select another\n")
                add_new_shift(shift_type, volunteer_shifts_df, username, camp_id, emergency_plan_index)
            except ConsecutiveShiftError:
                print("You cannot sign up for consecutive shifts.\n")
                add_new_shift(shift_type, volunteer_shifts_df, username, camp_id, emergency_plan_index)
    except ValueError:
        print(f"Date out of range, please enter date from {now} to {thirty_days_time}.")
        add_new_shift(shift_type, volunteer_shifts_df, username, camp_id, emergency_plan_index)


def availability_funcs(user):
    """Method for user to view current shifts or add new shifts. Main menu for this section.
    The code block after 'username = user' is in place so that only volunteers who have a camp
    (i.e., not new users) can view or edit shifts."""

    username = user

    #Check to see if volunteer has chosen a camp yet
    all_volunteers_df = pd.read_csv("volunteers_db.csv")
    volunteer_info_df = all_volunteers_df.loc[all_volunteers_df['usernames'] == f'{username}']
    check_nan = volunteer_info_df.isnull().values.any()

    if check_nan: #doesn't allow new users to use these functions
        print("It seems like you have not yet signed up to a camp. Please do so before trying to view and edit your shifts.")
    else:

        b = volunteer_info_df['campid'].values
        camp_id = str(b[0])
        c = volunteer_info_df['emergencyplanindex'].values
        emergency_plan_index = str(int(c[0]))

        custom_date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')   
        df = pd.read_csv("shifts.csv", parse_dates = ['startdate', 'enddate'], date_parser = custom_date_parser)
        volunteer_shifts_df = df[df['username'] == f'{username}'] #dataframe of user's shifts
        print("-------------------------------------------------------------------------------")
        print("[1] View current shifts")
        print("[2] Add new shift")
        print("[3] Return to home screen")

        user_input = input("Please select an option: ")
        while True:
            if user_input == '1':
                view_shifts(df, volunteer_shifts_df, username)
                #print('--------------------------------\n')
                availability_funcs(user)
                break
            elif user_input == '2':
                shift_type = select_shift_type()
                if shift_type == '3':
                    break
                else:
                    add_new_shift(shift_type, volunteer_shifts_df, username, camp_id, emergency_plan_index)
                    #print('--------------------------------\n')
                    availability_funcs(user)
                    break
            elif user_input == '3':
                #return to Home menu
                #print("Goodbye")
                volunteer_home.volunteer_home(user)
                break
            else: #error handling
                print("Please enter a valid input.")
                user_input = input("Please select an option: ")


# for testing this page in isolation, define a specific user below
# user = 'volunteer2'
# username = user
# availability_funcs(user)
import pandas as pd
from datetime import date, datetime, timedelta
import csv

class DuplicateError(Exception):
    '''Raises an error when a user tries to sign up for an existing shift'''
    pass

class ConsecutiveShiftError(Exception):
    '''Raises an error when a user tries to sign up for consecutive shifts'''
    pass


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
    pass
    #TODO: elif row in file: If count(row[volunteer]) < 5: insert new row. 
    #Else: return 'no slots available on this date. Please pick another' (max. number of volunteers present at a time)

def write_to_file(new_shift):
    #For volunteer_change_camp: load CampDetails csv to dataframe
    '''Function for writing to new shifts to shifts.csv'''
    filename = "shifts.csv"
    with open(filename, 'a+') as csvfile: #closes file after use
        #creating a CSV write object-
        csvwriter = csv.writer(csvfile)
        #writing the fields
        csvwriter.writerow(new_shift)
        print("New shift successfully selected!")
    #Change counts in CampDetails.csv
    #   #For each campID:"
    #   #   #count number of occurrences of that campID in shifts.csv
    #   #   #write the result to No. df['Volunteers']
    #Write df to campDetails.csv
    #Instead of incrementing counts one-by-one, performs fresh count each time - less likely to cause errors

def view_shifts(df, user_df, username):
    '''Function for a volunteer to view their current shifts'''
    past_shifts_df = pd.DataFrame(columns = user_df.columns)
    today_shifts_df = pd.DataFrame(columns = user_df.columns)
    future_shifts_df = pd.DataFrame(columns = user_df.columns)
    print(past_shifts_df)

    #Print all rows where current shifts are in 
    shifts = user_df.loc[df['username'] == f'{username}']
    print(shifts)
    # for ind in shifts.index:
    #     print(shifts.loc[ind])

    if shifts.empty:
        print('No shifts at present')
    else: 

        for ind in shifts.index:
            a = shifts.loc[ind]
            b = a.values.tolist()
            b[0] = b[0].date()
            b[1] = b[1].date()
            b_series = pd.Series(b, index = user_df.columns)
            
            if b[0] < date.today():
                past_shifts_df = past_shifts_df.append(b_series, ignore_index = True)
            elif b[0] == date.today():
                today_shifts_df = today_shifts_df.append(b_series, ignore_index = True)
            elif b[0] > date.today():
                future_shifts_df = future_shifts_df.append(b_series, ignore_index = True)

        if len(past_shifts_df.index) > 0:
            print("Past shifts:")
            print(past_shifts_df)
            print('\n')
        if len(today_shifts_df.index) > 0: 
            print("Today's shifts:")
            print(today_shifts_df)
            print('\n')
        if len(future_shifts_df.index) > 0: 
            print("Future shifts:")
            print(future_shifts_df)
            print('\n')

def add_new_shift(shift_type, user_df, username):
    '''Function for users to add a new shift'''
    print("You will be asked for the details of the shift you are signing up for")
        
    date_input = input('Please enter a date (YYYY-MM-DD): ')

    try:
        # Convert the string input to datetime object, it will catch error if you enter a unvalid date like 2020-12-40
        start_date = datetime.strptime(date_input, '%Y-%m-%d').date()
        # Limit the date_input to dates between today and thirty days' time
        now = date.today()
        thirty_days_time = (date.today() + timedelta(30)) 
        if not (now <= start_date <= thirty_days_time):
            raise ValueError
        # elif shift already selected:
        #     pass
        #raise an error for incorrect format
        else:
            print("The date you entered ->%f<- is valid", date_input)
            # You can write the date_input to csv file.
    except ValueError:
        print(f"Date out of range, please enter date from {now} to {thirty_days_time}.")
        availability_funcs(user)

    if shift_type == '1':
        print(f"Sign up for a shift on {start_date} from 09:00 to 19:00?")
        print("No: [0]")
        print("Yes: [1]")
        decision = input("Please select an option: ").strip()
    elif shift_type == '2':
        print(f"Sign up for a shift from {start_date} at 19:00 to {start_date + timedelta(1)} at 09:00?")
        print("No: [0]")
        print("Yes: [1]")
        decision = input("Please select an option: ").strip()

    if decision == '0':
        pass #returns to availability_funcs, which is called after this function executes
    elif decision == '1':

        if shift_type == '1':
            end_date = start_date
        elif shift_type == '2':
            end_date = start_date + timedelta(1)

        new_shift = [f'{start_date}', f'{end_date}', '19:00 - 09:00', f'{username}']

        try:
            if check_duplicates(user_df, start_date, end_date):
                raise DuplicateError
            if check_successive_shifts(user_df, shift_type, start_date, end_date):
                raise ConsecutiveShiftError
            else:
                write_to_file(new_shift)

        except DuplicateError:
            print("You have already signed up for this shift. Please select another")
            availability_funcs(user)
        except ConsecutiveShiftError:
            print("You cannot sign up for consecutive shifts.")
            availability_funcs(user)
            
    else: #error handling
        pass


def availability_funcs(user):
    """Method for user to view current shifts or add new shifts. Main menu for this section.
    The code block after 'username = user' is in place so that only volunteers who have a camp
    (i.e., not new users) can view or edit shifts."""

    username = user

    #Check to see if volunteer has chosen a camp yet
    all_volunteers_df = pd.read_csv("volunteers_db.csv")
    volunteer_df = all_volunteers_df.loc[all_volunteers_df['usernames'] == f'{username}']
    check_nan = volunteer_df.isnull().values.any()

    if check_nan: #doesn't allow new users to use these functions
        print("It seems like you have not yet signed up to a camp. Please do so before trying to view and edit your shifts.")
    else:

        print("Which type of shift would you like to interact with?")
        print("[1] Day shifts")
        print("[2] Night shifts")
        print("[3] Return to main menu")
        while True:
            shift_type = input("Please select an option: ").strip()
            if shift_type == '1':
                break
            elif shift_type == '2':
                break
            elif shift_type == '3':
                print("Returning you now: ")
                break
            else: #error handling
                print("Please enter a valid input.")

        custom_date_parser = lambda x: datetime.strptime(x, '%Y-%m-%d')   
        df = pd.read_csv("shifts.csv", parse_dates = ['startdate', 'enddate'], date_parser = custom_date_parser)
        user_df = df[df['username'] == f'{username}'] #dataframe of user's shifts

        print("[1] View current shifts")
        print("[2] Add new shift")
        print("[3] Return to home screen")

        user_input = input("Please select an option: ")

        if user_input == '1':
            view_shifts(df, user_df, username)
            print('--------------------------------')
            availability_funcs(user)

        elif user_input == '2':
            if False: #change to condition 'if volunteer has not signed up for a camp'
                pass
            else:
                add_new_shift(shift_type, user_df, username)
                print('--------------------------------')
                availability_funcs(user)

        elif user_input == 3:
            #return to Home menu
            print("Goodbye")
        else: #error handling
            pass

# for testing this page in isolation, define a specific user below
# user = 'volunteer2'
# username = user
# availability_funcs(user)
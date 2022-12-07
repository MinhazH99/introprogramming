import pandas as pd
import numpy as np
import os
import csv

#Menu:

#Logic:

## At start of session, need to read in current number - in practice, a limitation would be that only one
## user can use the system at a time for data integrity (overlapping transactions)
#Load disaster count table to dataframe
#Maybe use value_counts() to produce the values for the number of volunteers in each camp (number of times a camp name occurs)
#Load volunteer info to dataframe
#Options: 
#[0] assign oneself to camp for first time
#[1] view current camp
#[2] change camps
#If [0]:
#   Check whether they have a camp, and raise an error if so. 
#   Show them current camp
#   If they don't:
#       Ask them which city 
#       Ask them the disaster time
#       Based on these two, show current camps and numbers of staff/ refugees (make this a new (temportary?) dataframe)
#       Ask user which camp they'd like to change to
#       Decrement number of users at user's
#       Change user's camp to that one
#       Increment the number of volunteers at the camp in dataframe
#       Write change to CSV file
# 
#See bookmarked articles - can read in CSV data to Pandas dataframe and change data type as appropriate (useful for integers)

# test_file = open('list_of_camps.csv', 'r')
# DictReader_obj = csv.DictReader(test_file)
# for item in DictReader_obj:
#     print(item['Camp ID'])


def get_num_camps():
    df = pd.read_csv('test_file.csv')
    print(df)
    num_volunteers = df['Camp ID'].value_counts()
    return num_volunteers


# print(get_num_camps())

# Come back to these lines - for making a 'view' of camps and volunteer counts
# df = pd.read_csv('test_file.csv')
# res = pd.Series(list(zip(df['Camp ID'], df['Emergency plan index']))).value_counts()
# df2 = df[['Camp ID', 'Emergency plan index']].value_counts().reset_index(name = 'Number of volunteers')
# print(df2)




# class volunteerCampFunctions:
#     """
#     All methods for viewing and changing camp assignment for volunteers
#     """

def pick_relevant_camps(emergency_plan_index):
    '''Method for listing camps to user signed up to a particular emergency plan'''
    print(type(emergency_plan_index))
    print("Here is a list of camps:")
    camps_df = pd.read_csv('list_of_camps.csv')
    q = camps_df[camps_df['Emergency plan index'] == emergency_plan_index]['Camp ID']
    l = []
    for ind in q.index:
        print(q[ind])
        l += [q[ind]]
    choice = input("Which camp would you like to join?" ).strip()
    while choice not in l:
        print("Invalid choice. Please select one of the available camps.")
        choice = pick_relevant_camps(emergency_plan_index)
    return choice

def choose_camp(user):

    found = False

    df = pd.read_csv('test_file.csv') #file containing all volunteer info
    username = user
    a = df[df['Username'] == f'{username}']
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        camp_id = a['Camp ID'].to_string(index = False)
        if camp_id != 'NaN':
            print("You are already assigned to a camp. Your camp ID is", camp_id) #print Camp ID without index
        else:
            emergency_plan = int(a['Emergency plan index'].to_string(index = False)) #get emergency plan of volunteer from file
            choice = pick_relevant_camps(emergency_plan)
            #insert validation/ error-catching here

            test_file = open('test_file.csv', 'r')
            for line in test_file:
                part = line.split(',') # creates list of strings separated by , from the line
                if part[3] == username:
                    found = True
                    new = (part[0] + "," + part[1] + "," + part[2] + "," + part[3] + "," + part[4] + "," + part[5] + "," + choice) # Create new line to replace old one
                    tempfile = open('temp.csv', 'w')
                    test_file.seek(0,0) #set file pointer to the start of line 0
                    for line in test_file:
                        if username in line:
                            tempfile.write(new) #replace only the line to be overwritten
                            tempfile.write('\n')
                        else:
                            tempfile.write(line)
                #else: do nothing
            test_file.close()

            if found == False:
                print("Username not in records!")
            elif found == True:
                os.rename('test_file.csv', 'delete.csv')
                os.remove('delete.csv')
                os.rename('temp.csv', 'test_file.csv')
                print("Camp selected successfully. New camp: ", choice)


    else:
        print("Username not found!")
        choose_camp(user)

def view_camp(user):
    '''View curent camp'''
    df = pd.read_csv('test_file.csv') #file containing all volunteer info
    username = user
    a = df[df['Username'] == f'{username}']
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        camp_id = a['Camp ID'].to_string(index = False)
        if camp_id != 'NaN':
            print("Your camp ID is", camp_id) #print Camp ID without index
        else: 
            action = input("You are not currently assigned to a camp.\n\
            Enter [0] to return to menu.\n\
            Enter [1] to exit.") #with the understanding that from the menu, a user can pick a camp
            if action == 0:
                change_camp #call main menu function
            elif action == 1:
                print("Goodbye")
            else: #error handling
                pass
    else:
        print("Username not found!")
        view_camp(user)


def change_camp(user):
    '''To allow volunteers to change their camp'''
    found = False

    df = pd.read_csv('test_file.csv') #file containing all volunteer info
    username = user
    a = df[df['Username'] == f'{username}']
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        camp_id = a['Camp ID'].to_string(index = False)
        print(camp_id)
        print(type(camp_id))
        if camp_id != 'NaN':
            action = input("Your current camp is " + camp_id + ". Would you still like to change this? (Y/N)").strip()
            if action.lower() == 'y':
                emergency_plan = int(a['Emergency plan index'].to_string(index = False)) #get emergency plan of volunteer from file
                choice = pick_relevant_camps(emergency_plan)

                test_file = open('test_file.csv', 'r')
                for line in test_file:
                    part = line.split(',') # creates list of strings separated by , from the line
                    if part[3] == username:
                        found = True
                        new = (part[0] + "," + part[1] + "," + part[2] + "," + part[3] + "," + part[4] + "," + part[5] + "," + choice) # Create new line to replace old one
                        tempfile = open('temp.csv', 'w')
                        test_file.seek(0,0) #set file pointer to the start of line 0
                        for line in test_file:
                            if username in line:
                                tempfile.write(new) #replace only the line to be overwritten
                                tempfile.write('\n')
                            else:
                                tempfile.write(line)
                #else: do nothing
                test_file.close()
            elif action.lower() == 'n':
                print("Goodbye")
            else: #error handling
                pass
            

            if found == False:
                print("Username not in records!")
            elif found == True:
                os.rename('test_file.csv', 'delete.csv')
                os.remove('delete.csv')
                os.rename('temp.csv', 'test_file.csv')
                print("Camp selected successfully. New camp: ", choice)
        elif camp_id == 'NaN':
            action = input("You are not currently assigned to a camp. Would you like to choose a camp? (Y/N) ").strip()
            if action.lower() == 'y':
                choose_camp(user)
            elif action.lower() == 'n':
                print("Goodbye")
            else: #error handling
                pass
        else: #error handling
            pass
            
    else:
        print("Username not found!")
        change_camp(user)




def camp_volunteer_counts():
    '''Counts the number of volunteers at each camp. Creates a series with volunteer counts and merges with dataframe'''
    pass



# pick_relevant_camps(0)



#at present, achieved without auto-creation of new camps based on number of volunteers. Can only choose/ change to existing camp
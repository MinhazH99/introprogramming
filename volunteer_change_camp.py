import pandas as pd

def get_camp_list():
    '''Returns a list of all camps in CampDetails.csv'''
    df = pd.read_csv('CampDetails.csv')
    camp_list = []
    for ind in df.index:
        camp_list.append(df.loc[ind]["Camp ID"])
    return camp_list

def get_assoc_emergency_plan(camp):
    '''For a choice of camp, returns the associated emergency plan index'''
    df = pd.read_csv('CampDetails.csv')
    emergency_plan_index_df = df[df["Camp ID"] == camp]
    b = emergency_plan_index_df['Emergency Plan Index']
    c = int(b)
    emergency_plan_index = str(c)
    # print(c)
    return emergency_plan_index

def update_volunteer_count():
    '''Function to update the number of volunteers in each camp'''
    volunteer_df = pd.read_csv('volunteers_db.csv')
    camps_df = pd.read_csv('CampDetails.csv')
    camp_list = get_camp_list() #store list of all camps
    camp_count_list = []
    for camp in camp_list:
        #iterate through the list and store the number of occurrences of the camp in the volunteer database, 
        #i.e. how many volunteers are at that camp
        try:
            camp_count_list.append(volunteer_df['campid'].value_counts()[f'{camp}'])
        except KeyError:
            camp_count_list.append(0) #if the camp does not appear in the volunteer database, nobody has signed up to it
    
    camp_count_dict = {camp_list[i]: camp_count_list[i] for i in range(len(camp_list))} #dictionary of camp IDs and no. volunteers at each
    for key, value in camp_count_dict.items():
        camps_df.loc[camps_df['Camp ID'] == f'{key}', 'No. Volunteers'] = f'{value}' #update number of volunteers at each
    camps_df.to_csv("CampDetails.csv",index=False) #store the updated counts

def camp_functions_menu(user):
    '''Main menu for users to decide whether to choose a camp, view current camp, change camp, or return to main menu.'''
    print("Enter [1] to choose a camp for the first time.")
    print("Enter [2] to view the ID of the camp you are currently assigned to.")
    print("Enter [3] to change camps.")
    print("Enter [4] to exit.") #with the understanding that from the menu, a user can pick a camp
    user_input = input("Please select an option: ").strip()
    if user_input == '1':
        choose_camp(user)
    elif user_input == '2':
        view_camp(user) 
    elif user_input == '3':
        change_camp(user) 
    elif user_input == '4':
        print("Goodbye") #call main menu function
    else: #error handling
        pass


def choose_camp(user):
    """
    Allows user to change camp id
    Removes user from camp they were previously at (should edit the text file containing all camp details)
    NOT IMPLEMENTED YET: notifies camp administrator that volunteer has moved to different camp
    NOT IMPLEMENTED YET: Doesn't allow volunteer to move camps if their camp is understaffed, or at minimum staffing level.
    Minimum staffing level could be set manually, or set as a default to the closest integer value to number of refugees / 10
    """

    df = pd.read_csv('volunteers_db.csv') #file containing all volunteer info
    username = user
    a = df[df['usernames'] == f'{username}']
    camp_list = get_camp_list()
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        b = a.at[1, 'campid']
        camp_id = str(b)
        if camp_id != 'nan':
            print("You are already assigned to a camp. Your camp ID is", camp_id) #print Camp ID without index
        else:
            # The commented lines are only relevant if we decide volunteers can only move within camps from one plan
            # emergency_plan = int(a['emergencyplanindex'].to_string(index = False)) #get emergency plan of volunteer from file
            
            # choice = pick_relevant_camps(emergency_plan) #assigns choice of camp to variable 'choice'
            #insert validation/ error-catching here
            for camp in camp_list:
                print(camp)
            while True:
                choice = input("Pick a camp from the above list: ").strip()
                if choice not in camp_list:
                    print("Invalid choice.")
                emergency_plan_index = get_assoc_emergency_plan(choice)
                break
        
            #camps_df = pd.read_csv('CampDetails.csv')
            df.loc[(df["usernames"] == username),"campid"]=f'{choice}' #Use this in selecting_shifts
            df.loc[(df["usernames"] == username),"emergencyplanindex"]=f'{emergency_plan_index}'
            print("Camp ID updated")
            df.to_csv("volunteers_db.csv",index=False)
            update_volunteer_count()

            #modify camps_df by row count 
            #rewrite camps_df

    else:
        print("Username not found!")
        choose_camp(user)

def view_camp(user):
    '''View curent camp'''
    df = pd.read_csv('volunteers_db.csv') #file containing all volunteer info
    username = user
    a = df[df['usernames'] == f'{username}']
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        # camp_id = a['Camp ID'].to_string(index = False)
        b = a.at[1, 'campid']
        camp_id = str(b)
        if camp_id != 'nan':
            print("Your camp ID is", camp_id) #print Camp ID without index
            action = input("Your current camp is " + camp_id + ". Would you still like to change this? (Y/N)").strip()
            if action.lower() == 'y':
                pass
            elif action.lower() == 'n':
                print("Goodbye") #leaves camp manipulation menu
            else: #error handling
                pass
        else: 
            print("You are not currently assigned to a camp.")
            print("Enter [1] to choose a camp.")
            print("Enter [2] to exit.") #with the understanding that from the menu, a user can pick a camp
            user_input = input("Please select an option: ").strip()
            if user_input == '1':
                change_camp(user) 
            elif user_input == '2':
                print("Goodbye") #call main menu function
            else: #error handling
                pass
    else:
        print("Username not found!")
        view_camp(user)


def change_camp(user):
    """
    To allow volunteers to change their camp
    Removes user from camp they were previously at (should edit the CSV file containing all camp details)
    NOT IMPLEMENTED YET: notifies camp administrator that volunteer has moved to different camp
    NOT IMPLEMENTED YET: Doesn't allow volunteer to move camps if their camp is understaffed, or at minimum staffing level.
    Minimum staffing level could be set manually, or set as a default to the closest integer value to number of refugees / 10
    """

    df = pd.read_csv('volunteers_db.csv') #file containing all volunteer info
    username = user
    a = df.loc[df['usernames'] == f'{username}']
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        b = a.at[1, 'campid']
        camp_id = str(b)
        print(type(camp_id))
        if camp_id != 'nan':
            action = input("Your current camp is " + camp_id + ". Would you still like to change this? (Y/N)").strip()
            if action.lower() == 'y':
                
                #the superior version
                # emergency_plan = int(a['emergencyplanindex'].to_string(index = False)) #get emergency plan of volunteer from file
                #for now:
                
                # choice = pick_relevant_camps(emergency_plan_index)
                while True:
                    choice = input("Pick a camp from the above list: ").strip()
                    camp_list = get_camp_list()
                    if choice not in camp_list:
                        print("Invalid choice.")
                    emergency_plan_index = get_assoc_emergency_plan(choice)
                    break


                df.loc[(df["usernames"] == username),"campid"]=f'{choice}' #Use this in selecting_shifts
                df.loc[(df["usernames"] == username),"emergencyplanindex"]=f'{emergency_plan_index}'
                print("Camp ID updated")
                df.to_csv("volunteers_db.csv",index=False)
                update_volunteer_count()

            elif action.lower() == 'n':
                print("Goodbye") #return to main menu
            else: #error handling
                pass
        
        elif camp_id == 'nan':
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
import pandas as pd
import volunteer_home

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
    print("-------------------------------------------------------------------------------")
    print("Enter [1] to choose a camp for the first time.")
    print("Enter [2] to view the ID of the camp you are currently assigned to.")
    print("Enter [3] to change camps.")
    print("Enter [4] to return to the main menu.") #with the understanding that from the menu, a user can pick a camp
    user_input = input("Please select an option: ").strip()
    while True: 
        if user_input == '1':
            choose_camp(user)
            break
        elif user_input == '2':
            view_camp(user) 
            break
        elif user_input == '3':
            change_camp(user) 
            break
        elif user_input == '4':
            #print("Goodbye") #call main menu function
            volunteer_home.volunteer_home(user)
            break
        else: #error handling
            print("Invalid choice")
            user_input = input("Please select an option: ").strip()
            
def choose_camp(user):
    '''Allows a volunteer to choose a camp for the first time and redirects if they have one already'''

    df = pd.read_csv('volunteers_db.csv') #file containing all volunteer info
    username = user
    a = df[df['usernames'] == f'{username}']
    camp_list = get_camp_list()
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        try:
            b = a['campid'].values
            camp_id = str(b[0])
        except:
            camp_id = 'nan'
        if camp_id != 'nan':
            print("You are already assigned to a camp. Your camp ID is", camp_id, "\n") #print Camp ID without index
            camp_functions_menu(user)
        else:
            print("Below are a list of camps:\n")
            for camp in camp_list:
                print(camp)
            print("\n")
            choice = input("Pick a camp from the above list: ").strip()
            while choice not in camp_list:
                print("Invalid choice.")
                choice = input("Pick a camp from the above list: ").strip()
                
            emergency_plan_index = str(int(get_assoc_emergency_plan(choice)))
        
            df.loc[(df["usernames"] == username),"campid"]=f'{choice}' 
            df.loc[(df["usernames"] == username),"emergencyplanindex"]=f'{emergency_plan_index}'
            print("Camp ID updated")
            df.to_csv("volunteers_db.csv",index=False)
            update_volunteer_count()

            camp_functions_menu(user)

            #modify camps_df by row count 
            #rewrite camps_df

    else:
        print("Username not found!")
        camp_functions_menu(user)

def view_camp(user):
    '''Allows a volunteer to view their curent camp'''
    df = pd.read_csv('volunteers_db.csv') #file containing all volunteer info
    username = user
    a = df[df['usernames'] == f'{username}']
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        # camp_id = a['Camp ID'].to_string(index = False)
        try:
            b = a['campid'].values
            camp_id = str(b[0])
        except:
            camp_id = 'nan'
        if camp_id != 'nan':
            print("Your camp ID is", camp_id, '\n')
            camp_functions_menu(user)
            
        else: 
            while True:
                print("You are not currently assigned to a camp.")
                print("Enter [1] to choose a camp.")
                print("Enter [2] to return to main menu.") 
                user_input = input("Please select an option: ").strip()
                if user_input == '1':
                    choose_camp(user) 
                    break
                elif user_input == '2':
                    break
                else: 
                    print("Invalid choice.")
                    user_input = input("Please select an option: ").strip()
            camp_functions_menu(user)
    else:
        print("Username not found!")
        camp_functions_menu(user)


def change_camp(user):
    '''Allows a volunteer to move between camps'''

    df = pd.read_csv('volunteers_db.csv') #file containing all volunteer info
    username = user
    a = df.loc[df['usernames'] == f'{username}']
    
    if len(a) > 0: #i.e., if there are any rows in the dataframe with this username
        try:
            b = a['campid'].values
            camp_id = str(b[0])
        except:
            camp_id = 'nan'
        
        if camp_id != 'nan':
            action = input("Your current camp is " + camp_id + ". Would you still like to change this? (Y/N)").strip()

            while True:

                if action.lower() == 'y':
                    camp_list = get_camp_list()
                    for camp in camp_list:
                        print(camp)
                    print("\n")
                    choice = input("Pick a camp from the above list: ").strip()
                    while choice.upper() not in camp_list: #converts string to upper case
                        print("Invalid choice.")
                        choice = input("Pick a camp from the above list: ").strip()
                    emergency_plan_index = str(int(get_assoc_emergency_plan(choice))) #safeguard against unexplained issue

                    df.loc[(df["usernames"] == username),"campid"]=f'{choice}'
                    df.loc[(df["usernames"] == username),"emergencyplanindex"]=f'{emergency_plan_index}'
                    print("Camp ID updated")
                    df.to_csv("volunteers_db.csv",index=False)
                    update_volunteer_count()
                    break

                elif action.lower() == 'n':
                    print("Goodbye") #return to main menu
                    break
                else: 
                    print("Invalid choice")
                    action = input("Your current camp is " + camp_id + ". Would you still like to change this? (Y/N)").strip()
            camp_functions_menu(user)

        
        elif camp_id == 'nan':
            while True:
                print("You are not currently assigned to a camp.")
                print("Enter [1] to choose a camp.")
                print("Enter [2] to return to main menu.") 
                user_input = input("Please select an option: ").strip()
                if user_input == '1':
                    choose_camp(user) 
                    break
                elif user_input == '2':
                    break
                else: 
                    print("Invalid choice.")
                    user_input = input("Please select an option: ").strip()
            camp_functions_menu(user)
            
    else:
        print("Username not found!")
        change_camp(user)


# camp_functions_menu('volunteer2')
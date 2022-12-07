from volunteer_login import editVolunteer
from emergency import emergency_profile
from volunteer_change_camp import change_camp,choose_camp,pick_relevant_camps,view_camp
from volunteer_selecting_shifts import availability_funcs

def volunteer_home(user):
    print("[1] Edit your details")
    print("[2] Assign yourself a camp")
    print("[3] Edit avalaiblity")
    print("[4] Create or Edit Emergency Profile for Refugee")

    user_input = input("Please select an option: ")

    if user_input == '1':
        pass

    elif user_input == '2':
        change_camp(user)

    elif user_input == '3':
        availability_funcs(user)


    elif user_input == '4':
        emergency_profile()


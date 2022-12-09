import volunteer_editdetails
import emergency
import volunteer_change_camp
import volunteer_selecting_shifts

def volunteer_home(user):
    print("-------------------------------------------------------------------------------")
    print("[1] Edit your details")
    print("[2] Assign yourself a camp")
    print("[3] Edit avalaiblity")
    print("[4] Create or Edit Emergency Profile for Refugee")
    print("[5] Logout")

    while True:

        user_input = input("Please select an option: ")

        if user_input == '1':
            volunteer_editdetails.volunteerEditDetails(user)
            break

        elif user_input == '2':
            volunteer_change_camp.change_camp(user)
            break

        elif user_input == '3':
            volunteer_selecting_shifts.availability_funcs(user)
            break
            
        elif user_input == '4':
            emergency.emergency_profile()
            break

        elif user_input == '5':
            print("Successfully logged out!")
            break
        
        else:
            print("Please select a valid option")
        




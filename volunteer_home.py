import volunteer_editdetails
import emergency
import volunteer_change_camp
import volunteer_selecting_shifts
import home
import report

def volunteer_home(user):
    print("-------------------------------------------------------------------------------")
    print("[1] Edit your personal details")
    print("[2] View and edit your assigned camp")
    print("[3] Edit availability")
    print("[4] Create or Edit Emergency Profile for Refugee")
    print("[5] Report an issue")
    print("[6] Logout")

    while True:

        user_input = input("Please select an option: ")

        if user_input == '1':
            volunteer_editdetails.volunteerEditDetails(user)
            break

        elif user_input == '2':
            volunteer_change_camp.camp_functions_menu(user)
            break

        elif user_input == '3':
            volunteer_selecting_shifts.availability_funcs(user)
            break
            
        elif user_input == '4':
            emergency.emergency_profile(user)
            break

        elif user_input == '5':
            report.report(user)
            break
        
        
        elif user_input == '6':
            
            print("Successfully logged out!")
            print("-------------------------------------------------------------------------------")
            home.home()
            break
        
        else:
            print("Please select a valid option")
        

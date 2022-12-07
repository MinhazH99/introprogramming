# One thing I'm not yet clear on is how volunteers would be created. I've not tackled that below,
# but I've used the __init method for the time being to create and test out dummy data
# Make repeating part into a function and call it

import os

def getLine(datum):
    '''Function for getting a specific line from a text file if it contains a certain string'''
    with open('test_file.csv', 'r+') as test_file:  # opening test file at beginning for use in all functions
        data = test_file.readlines()
        # print("Number of lines: ", len(data))
        i = 0
        for line in data:
            if(f'{datum}' in line):
                return line
            else:
                return False

class Volunteer:
    """
    Allows the volunteer to:
    -Edit their information
    -   -name
    -   -phone
    -   -identification of their camp
    -   -availability
    """

    def __init__(self, firstname, family_name, phone_number):
        #open file
        #if dictionary object whose name is username exists:

        #else

        self.firstname = firstname
        self.family_name = family_name
        self.phone_number = phone_number
        self.username = 'volunteer1' #this should be set automatically based on data in the text file
        self.account_type = 'Volunteer'
        self.pwd = '111' #since all passwords are set to the string 111. Better way to define it?

        #create dictionary in python file whose name is username, and fill values
        #username
        #temp = username
        #figure out way to make dictionary whose name corresponds to username

    def editPersonalInfo(self):
        """
        Currently the way of rewriting files is written in a difficult-to-read way, and is a bit clumsy, but functional
        """

        option = {'First name': 0, 'Family name': 1, 'Phone number': 2, 'Password': 3, 'Exit': 4}
        action = int(input(f"Please select one of the following personal details to change:\n\
        First name: [{option['First name']}]\n\
        Family name: [{option['Family name']}]\n\
        Phone number: [{option['Phone number']}]\n\
        Password: [{option['Password']}]\n\
        Exit: [{option['Exit']}] \n"))

        # instructions for changing name
        if action == 0:

            found = False

            username = input("Enter username: ").strip()  # first names aren't unique, but usernames are. Need both to match to update record
            current_firstname = input("Enter current first name: ").strip()

            new_firstname = input("Enter your first name: ").strip()
            new_firstname_verification = input("Re-enter your first name: ").strip()

            if new_firstname != new_firstname_verification:
                print("Names must match.")
            else:
                test_file = open('test_file.csv', 'r')
                for line in test_file:
                    part = line.split(',') # creates list of strings separated by / from the line
                    if part[0] == current_firstname and part[3] == username:
                        self.firstname = new_firstname
                        found = True
                        new = (new_firstname + "," + part[1] + "," + part[2] + "," + part[3] + "," + part[4] + "," + part[5] + "," + part[6]) # Create new line to replace old one
                        tempfile = open('temp.csv', 'w')
                        test_file.seek(0,0) #set file pointer to the start of line 0
                        for line in test_file:
                            if current_firstname in line and username in line:
                                tempfile.write(new) #replace only the line to be overwritten
                            else:
                                tempfile.write(line)
                        print("\nFirst name updated")
                    #else: do nothing
                test_file.close()

                # TO DO: create a trigger to include the reason for a name change when sending a report to the administrator

            if found == False:
                print("First name not in records!")
            elif found == True:
                os.rename('test_file.csv', 'delete.csv')
                os.remove('delete.csv')
                os.rename('temp.csv', 'test_file.csv')
                print("Name changed successfully. New name: ", self.firstname)

        elif action == 1:
            # reason = input("Enter your reason for changing names: ")
            found = False

            username = input("Enter username: ").strip()  # family names aren't unique, but usernames are. Need both to match to update record
            current_family_name = input("Enter current family name: ").strip()

            new_family_name = input("Enter your family name: ").strip()
            new_family_name_verification = input("Re-enter your family name: ").strip()
            if new_family_name != new_family_name_verification:
                print("Names must match.")
            else:
                test_file = open('test_file.csv', 'r')
                for line in test_file:
                    part = line.split(',')  # creates list of strings separated by / from the line
                    if part[1] == current_family_name and part[3] == username:
                        self.family_name = new_family_name
                        found = True
                        new = (part[0] + "," + new_family_name + "," + part[2] + "," + part[3] + "," + part[4] + "," +
                               part[5] + "," + part[6])  # Create new line to replace old one
                        tempfile = open('temp.csv', 'w')
                        test_file.seek(0, 0)  # set file pointer to the start of line 0
                        for line in test_file:
                            if current_family_name in line and username in line:
                                tempfile.write(new)  # replace only the line to be overwritten
                            else:
                                tempfile.write(line)
                        print("\nFirst name updated")
                    # else: do nothing
                test_file.close()

                # TO DO: create a trigger to include the reason for a name change when sending a report to the administrator

            if found == False:
                print("First name not in records!")
            elif found == True:
                os.rename('test_file.csv', 'delete.csv')
                os.remove('delete.csv')
                os.rename('temp.csv', 'test_file.csv')
                print("Name changed successfully. New name: ", self.family_name)


                # create a trigger to include the reason for a name change when sending a report to the administrator

        # instructions for changing phone number
        elif action == 2:
            #TO DO: implement type/ format forcing
            #could make phone number unique by default, but for now written as if it's not

            username = input("Enter username: ").strip()  # family names aren't unique, but usernames are. Need both to match to update record
            current_number = str(input("Enter current phone number: ")).strip()

            new_number = str(int(input("Enter your phone number without spaces: "))).strip()
            new_number_verification = str(int(input("Re-enter your phone number without spaces: "))).strip()
            if new_number != new_number_verification:
                print("Numbers must match.")
            else:
                test_file = open('test_file.csv', 'r')
                for line in test_file:
                    part = line.split(',')  # creates list of strings separated by / from the line
                    if part[2] == current_number and part[3] == username:
                        self.phone_number = new_number
                        found = True
                        new = (part[0] + "," + part[1] + "," + new_number + "," + part[3] + "," + part[4] + "," +
                               part[5] + "," + part[6])  # Create new line to replace old one
                        tempfile = open('temp.csv', 'w')
                        test_file.seek(0, 0)  # set file pointer to the start of line 0
                        for line in test_file:
                            if current_number in line and username in line:
                                tempfile.write(new)  # replace only the line to be overwritten
                            else:
                                tempfile.write(line)
                        print("\nFirst name updated")
                    # else: do nothing
                test_file.close()

                # TO DO: create a trigger to include the reason for a name change when sending a report to the administrator

            if found == False:
                print("First name not in records!")
            elif found == True:
                os.rename('test_file.csv', 'delete.csv')
                os.remove('delete.csv')
                os.rename('temp.csv', 'test_file.csv')
                print("Name changed successfully. New name: ", self.family_name)



                self.phone_number = new_number
                print("Number changed successfully. New phone number: ", self.phone_number)

        # instructions for changing password
        elif action == 3:
            if self.account_type == 'Volunteer':
                print("Sorry, only system administrators can change their passwords.")
            else:
                new_pwd = input("Enter your new password: ")
                new_pwd_verification = input("Re-enter your new password: ")
                if new_pwd != new_pwd_verification:
                    print("Passwords must match.")
                else:
                    self.pwd = new_pwd
                    print("Password changed successfully. New password: ", self.pwd)

        # instructions for exiting
        elif action == 4:
            print("Exiting now.")

            # implement error-handling here

        else:
            print("Value not recognised.")

            # not yet implemented error-handling

    def editCampID(self):
        """
        Allows user to change camp id
        Removes user from camp they were previously at (should edit the text file containing all camp details)
        NOT IMPLEMENTED YET: notifies camp administrator that volunteer has moved to different camp
        NOT IMPLEMENTED YET: Doesn't allow volunteer to move camps if their camp is understaffed, or at minimum staffing level.
        Minimum staffing level could be set manually, or set as a default to the closest integer value to number of refugees / 10
        """
        pass

    def editAvailability(self):
        pass

a = Volunteer('John', 'Doe', 1203)
a.editPersonalInfo()
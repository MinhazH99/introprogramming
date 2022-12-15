import smtplib
import pandas as pd

sys_email = "3.mergency.sys@gmail.com"
sys_password = "mhtxjymibjyqlixb"
def get_password():
    # TODO Don't know how to get the volunteer's username, set a dummy data 'volunteer2'. 
    volunteer = 'volunteer2'
    df = pd.read_csv('volunteers_db.csv')
    user_email = df.loc[(df['usernames'] == volunteer)]['email']
    print(user_email)
    # If the user entered the right email that they registered
    if user_email.empty == False:
        # TODO type(password) is an object, how can I convert it into a string?
        password = df.loc[(df['usernames'] == volunteer)]['password']
        print(password)
        # Set up the connection with the mail server
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sys_email, sys_password)

            # Set up the email content as follows:
            subject = "No reply: Your password for e-mergency management system"
            body = f"Your password is: {password}"
            msg = f"Subject:{subject}\n\n{body}"
            smtp.sendmail(sys_email, user_email, msg)
            print(f"Your password is sent to your email: {user_email}, please take a look.")
    else:
        print("The email you entered didn't match the email you registered. ")
get_password()
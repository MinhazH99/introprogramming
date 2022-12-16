import smtplib
import pandas as pd
import subprocess

# implement pip as subprogress:
subprocess.Popen(['pip3', 'install', 'secure-smtplib'])


sys_email = "3.mergency.sys@gmail.com"
sys_password = "mhtxjymibjyqlixb"
def get_password():
    # TODO Don't know how to get the volunteer's username, set a dummy data 'volunteer2'. 
    volunteer = 'volunteer2'
    df = pd.read_csv('volunteers_db.csv', index_col = False)
    user_email = df.loc[(df['usernames'] == volunteer)]['email']
    # If the user entered the right email that they registered
    if user_email.empty == False:
        user_df = df.loc[(df['usernames'] == volunteer)]
        password_list = user_df['password'].values
        password = str(password_list[0])

        # Set up the connection with the mail server
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login(sys_email, sys_password)

            # Set up the email content as follows:
            subject = "<No reply> Your password for e-mergency management system"
            body = f"Hi {volunteer},\nYou recently sent a request to view your password.\nYour password is: {password}.\nDon't show this email to anyone else."
            msg = f"Subject:{subject}\n\n{body}"
            smtp.sendmail(sys_email, user_email, msg)
            print(f"Your password is sent to your email: {user_email}, please take a look.")
    else:
        print("The email you entered didn't match the email you registered. ")
get_password()
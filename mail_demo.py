
import smtplib
import pandas as pd
import subprocess



sys_email = "ems.management.sys@gmail.com"
sys_password = "ofqdrgiwzemsnmbo"

# sys_email = "3.mergency.sys@gmail.com"
# sys_password = "mhtxjymibjyqlixb"
def get_password(user):
    #TODO Don't know how to get the volunteer's username, set a dummy data 'volunteer2'. 
    volunteer = user
    df = pd.read_csv('volunteers_db.csv', index_col = False)
    user_email = df.loc[(df['usernames'] == volunteer)]['email'].values[0]

    while True:
        em_user_input = input("Please enter your email: ")
        if user_email == em_user_input:
            user_df = df.loc[(df['usernames'] == volunteer)]
            password_list = user_df['password'].values
            password = str(password_list[0])
            token = df.loc[(df['usernames'] == volunteer)]['token'].values[0]
            
            with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(sys_email, sys_password)

                subject = "<No reply> Reset passsword for E-Mergency Management System (EMS)"
                body = f"Hi {volunteer},\nYou recently sent a request to reset your password.\nYour reset token is: {token}.\nDon't show this email to anyone else."
                msg = f"Subject:{subject}\n\n{body}"
                smtp.sendmail(sys_email, user_email, msg)
                print(f"Your reset token is sent to your email: {user_email}, please take a look. Please also check spam/junk folder")
                break
        else:
            print("The email you entered didn't match the email you registered. ")

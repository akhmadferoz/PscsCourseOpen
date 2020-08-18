# Import relevant Packages
from bs4 import BeautifulSoup
import requests
from getpass import getpass
import time
import re
import sys
import smtplib, ssl

def sendemail(messages,email,email_password):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = email
    receiver_email = email
    password = email_password
    message = """\
Subject: Course OPEN!

course is open\n""" + messages


    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


# Page to send request to login
login_page = "https://pscs.habib.edu.pk/psp/ps/?&cmd=login&languageCd=ENG"

# Get credentials.
user = input("ID: ")
password = getpass()
payload ={"userid": user,
"pwd": password}
email = input("Email: ")
emailpassword = getpass()

# Create a session
session = requests.Session()
# Send a post request to log in
session.post(login_page,data=payload)

# Do forever till found
while True:
    shopping_cart_page = "https://pscs.habib.edu.pk/psc/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?&ICAGTarget=startnewlink" 
    content = session.get(shopping_cart_page)
    content = BeautifulSoup(content.text,"html.parser")
    # Extract the content in shopping cart by pattern matching using regular patterns
    content =content.find_all(id=re.compile("trSSR_REGFORM_VW\$0_row[0-9]"))
    # print(a)
    for i in content:
        # Get class name
        classnames= i.find(id=re.compile("win0divP_CLASS_NAME\$[0-9]")).get_text()
        # Get class status
        classstatus = i.find(id=re.compile("win0divDERIVED_REGFRM1_SSR_STATUS_LONG\$[0-9]")).find("img").get("alt")
        # If class is open then email
        if classstatus == "Open":
            sendemail(f"{classnames} is {classstatus}",email,emailpassword)
            print("done")
            sys.exit()
    
    # Sleep for 60 seconds before next request
    time.sleep(60)

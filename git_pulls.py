#!/usr/bin/env python

from github import Github
import requests
import datetime
import pandas
import smtplib
from email.message import EmailMessage
from tabulate import tabulate

# Authentication(only if needed)
#access_token = "my_access_token"
#auth = Auth.Token(access_token)
#g = Github(auth=auth)
#user = g.get_user().login
#print ("Logged in as:",user)

# User variables(for testing)
#repo = "https://api.github.com/repos/hashicorp/terraform-provider-aws/pulls"
#repo = "https://api.github.com/repos/hashicorp/vault/pulls"
#email_address = ""
#dest_address = ""
#email_password = ""

# User variables from inputs
repo = input("Enter repository URL: ")
email_address= input("Enter sender email address: ")
email_password = input("Enter sender email password: ")
dest_address = input("Enter destination email address: ")

# App variables
subject = "Pull Request summary from last week for: "+repo
today = datetime.date.today()
week_ago = today - datetime.timedelta(days=7)
prs_list = [] 

# Getting PRs
print ("Fetching pull requests from:",repo)
req = requests.get(repo)
req_json = req.json()

# Filtering PRs
for item in req_json:
	date=item["updated_at"]
	pandas_date=pandas.to_datetime(date).date()
	if pandas_date > week_ago:
		prs_list.append({"URL": item["html_url"], "updated_at": item["updated_at"], "title": item["title"]})

# Generating email content
df = pandas.DataFrame(prs_list)
content = tabulate(df, headers='keys', tablefmt='presto')
#print (content)

# Sending email
msg = EmailMessage()
msg['Subject'] = subject
msg['From'] = email_address
msg['To'] = dest_address
msg.set_content(content)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(email_address, email_password) 
    smtp.send_message(msg)


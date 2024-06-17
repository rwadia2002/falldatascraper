import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import random
import gspread
import csv
import os.path

api_key = ""
endpoint_url = "http://maker.ifttt.com/trigger/Fall_reset"
falltype = ''
# Example GET request
response = requests.get('http://maker.ifttt.com/trigger/Fall_detect/with/key/dL_eQ1RwjirqHa02INa_8T')
resetresponse = requests.get('http://maker.ifttt.com/trigger/Fall_reset/with/key/dL_eQ1RwjirqHa02INa_8T')
positivefallresponse = (b"Congratulations! You've fired the Fall_detect event")
if response.content==(positivefallresponse):
    positiveresetreponse = (b"Congratulations! You've fired the Fall_reset event")

    if resetresponse.content == positiveresetreponse :

        print('send a confirmation email that everything will be fine')
        falltype = 'reset'
        subject = 'Report of a reset fall'
        body = 'This is a notification that your vulnerable person may have suffered  a fall but reset the system!'

    if resetresponse.content != positiveresetreponse :
        print('send a confirmation email that everything will not be fine')
        falltype = ' fall'
        subject = 'Report of fall'
        body = 'This is a notification that your vulnerable person suffered a fall!'



# Example POST request with payload
#payload = {'param1': 'value1', 'param2': 'value2'}
#response = requests.post(endpoint_url, json=payload, headers={'Authorization': f'Bearer {api_key}'})

print(response.status_code)


def send_email(subject, body, to_email):
    # Your Outlook credentials
    outlook_user = 'falldetecttest@outlook.com'
    outlook_password = 'Tester123!'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = outlook_user
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server (Outlook)
    with smtplib.SMTP('smtp-mail.outlook.com', 587) as server:
        server.starttls()  # Secure the connection
        server.login(outlook_user, outlook_password)  # Login to your Outlook account
        server.sendmail(outlook_user, to_email, message.as_string())  # Send the email

# Example usage

to_email = 'falldetecttest@outlook.com'

send_email(subject, body, to_email)

#falldetecttest@outlook.com


internal_email = 'rw00800@surrey.ac.uk'


condenseddate=datetime.datetime.now()
serialdatetime=datetime.datetime.now().strftime('%Y/%m%/d--%H:%M:%S')

eventid=random.randint(10**8, (10**10)-1)
date=''
category=''

evendata = {'eventid':eventid,'date':condenseddate,'category':falltype,'acceleration':0,'velocity':0}
print('hi')

# Load the service account credentials
gc = gspread.service_account(filename='fall-detection-407423-c71db70926a7.json')

# Open the Google Sheet
sheet = gc.open("Fall Detection Data").sheet1

# Example: Read contents of the sheet
values = sheet.get_all_records()

# Print the values
print('hi')


for value in reversed(values):
    if value.get('Time/Date'):
        timedate= (value.get('Time/Date'))
        acceleration = value.get('Acceleration')
        gyro=value.get('Gyroscope (x,y,z)')
        eventid = random.randint(10 ** 8, (10 ** 10) - 1)
        body = f"Fall at  {timedate} at acceleration {acceleration} with Gyroscope coordinates {gyro}."
        subject=f"EVENT ID -- {eventid} Fall at  {timedate} "
        send_email(subject, body, to_email)
        with open('data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(timedate)
            writer.writerows(acceleration)
            writer.writerows(gyro)






### Script to get an alert if there is a servicenow incident that is close to running on SLA.
import pymssql
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

server = 'IP'
user = 'USER'
password = 'PASSWORD'
database = 'DB_NAME'

# Connect to the database
conn = pymssql.connect(server=server, user=user, password=password, database=database)


# Perform search for KontaktPersonServer filter and Server filter
query = f"Select TOP 1000 * from [Database].[fact].[SagerView] where (DV_Gruppe ='Gruppe1' OR DV_Gruppe ='Gruppe2') AND status NOT IN ('closed', 'resolved') and Sagstype_ID = 'request'"
df1 = pd.read_sql_query(query, conn)
print ("------------ Alle aktive sager ---------")
print(df1)
df1.to_csv('output.txt', sep='\t', index=False)

# Current date and time
now = datetime.now()

# Time 24 hours from now
time_in_24_hours = now + timedelta(hours=24)


# Convert 'SLA_Due' column to datetime if not already
df1['sla_Due'] = pd.to_datetime(df1['sla_due'])

# Check if any dates are within the next 24 hours
due_within_24_hours = (df1['sla_due'] > now) & (df1['sla_due'] <= time_in_24_hours)


## Print Nummer and DV_assigned_to fields for tasks due within 24 hours
#if due_within_24_hours.any():
#    tasks_due_soon = df1[due_within_24_hours][['Nummer', 'DV_assigned_to', 'sla_due', 'short_description']]
#    print(tasks_due_soon)
#    tasks_due_soon.to_csv('output.txt', sep='\t', index=False)
#else:
#    print("No tasks are due within the next 24 hours")



# Send an email if there are tasks due within 24 hours
if due_within_24_hours.any():
    pretext = "Følgende INC's løber for sla inden for de næste 24 timer:\n\n"
    tasks_due_soon = df1[due_within_24_hours][['Nummer', 'DV_assigned_to', 'sla_due', 'short_description', 'Link']]
    email_body = pretext + tasks_due_soon.to_string(index=False)
    print ("---- Alle sager de løber på SLA 24 timer ---")
    print (tasks_due_soon.to_string())
    # Set up email parameters
    sender = 'PYsoar@company.dk'  # Replace with your email address
    recipient = 'reciever@company.dk'
    subject = 'Følgende Incidents løber for SLA inden for 24 timer.'

    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = 'reciever@company.dk'
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP('smtprelay.company.dk', 25)
        server.send_message(msg)
        server.quit()
        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email: {e}')
else:
    print('No tasks are due within the next 24 hours.')


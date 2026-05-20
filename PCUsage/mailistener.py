import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import imaplib
import email
import getpass
import time
from datetime import datetime, date, timedelta, timezone
from email.utils import parsedate_to_datetime
from plyer import notification

LOG_FILE = "usage_log.txt"
EMAIL_USER = "YOUR GMAIL"
EMAIL_PASSWORD = "YOUR SMTP GMAIL PASSWORD"
TO_EMAIL = "EMAIL RECIPIENT (USUALLY SAME AS YOUR GMAIL)"
SYNTAX_ERROR = """
Subject --> \"PCUsage Command\"
Command list:
- extend [time (h:m)]
- reduce [time (h:m)]
- set [time (h:m)]
- drain
- getlogs [day/week/month]
- msg [message]
"""

def calctime(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    return f"{hours}:{minutes:02}h"

def cseconds(given_hours):
    time = given_hours.split(':')
    if len(time) == 1:
        minutes = int(time[0])
        total_seconds = minutes*60
    if len(time) == 2:
        hours, minutes = map(int, time)
        total_seconds = (hours * 3600) + (minutes * 60)
    return total_seconds

def send_notification(message):
    notification.notify(
        title='Messaggio da Andre',
        message=message,
        app_icon=None,
        timeout=10,
    )

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, TO_EMAIL, text)

def check_log():
    with open(LOG_FILE, 'r') as log:
            lines = log.readlines()
            for line in lines:
                parts = line.split(' - ')
                if parts[0].strip() == str(date.today()):
                    if parts[-1].strip() == '0':
                        return 0
                    else:
                        return int(parts[-1])
            return False

def update_log(log_file_path, new_number):
    today_date = date.today()
    today_date_str = today_date.strftime('%Y-%m-%d')

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    updated_lines = []
    for line in lines:
        if today_date_str in line:
            # Update the last number for today's date
            parts = line.split(' - ')
            parts[-1] = str(new_number)
            parts[1] = str(datetime.now().strftime('%H:%M:%S'))
            updated_line = ' - '.join(parts)
            updated_lines.append(updated_line + '\n')
        else:
            updated_lines.append(line)

    with open(log_file_path, 'w') as log_file:
        log_file.writelines(updated_lines)

def get_daily_logs():
    today = date.today()

    daily_logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            lines = log.readlines()
            for line in lines:
                date_str = line.split()[0]
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                if log_date == today:
                    t = line.split()[-1]
                    time_played = None
                    if t == '0' or t == '-1':
                        time_played = '1:05h'
                    else:
                        time_played = calctime(t)
                    line = line.strip() + f' - {time_played}\n'
                    daily_logs.append(line)

    return ''.join(daily_logs)

def get_weekly_logs():
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    weekly_logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            lines = log.readlines()
            for line in lines:
                date_str = line.split()[0]
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                if start_of_week <= log_date <= end_of_week:
                    t = line.split()[-1]
                    time_played = None
                    if t == '0' or t == '-1':
                        time_played = '1:05h'
                    else:
                        time_played = calctime(t)
                    line = line.strip() + f' - {time_played}\n'
                    weekly_logs.append(line)

    if len(weekly_logs) > 0:
        return ''.join(weekly_logs)
    else:
        return 'No logs for this week'

def get_monthly_logs():
    today = date.today()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

    monthly_logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            lines = log.readlines()
            for line in lines:
                date_str = line.split()[0]
                log_date = datetime.strptime(date_str, '%Y-%m-%d').date()

                if start_of_month <= log_date <= end_of_month:
                    t = line.split()[-1]
                    time_played = None
                    if t == '0' or t == '-1':
                        time_played = '1:05h'
                    else:
                        time_played = calctime(t)
                    line = line.strip() + f' - {time_played}\n'
                    monthly_logs.append(line)

        if len(monthly_logs) > 0:
            return ''.join(monthly_logs)
        else:
            return 'No logs for this month'
    else:
        return 'No logfile found'

def parse_command(body):
    try:
        command = body.split(' ')
        if command[0] == 'extend':
            update_log(LOG_FILE, check_log() + cseconds(command[-1]))
        elif command[0] == 'reduce':
            update_log(LOG_FILE, check_log() - cseconds(command[-1]))
        elif command[0] == 'set':
            update_log(LOG_FILE, cseconds(command[-1]))
        elif command[0] == 'drain':
            update_log(LOG_FILE, 0)
        elif command[0] == 'getlogs':
            if command[-1] == 'day': send_email('PCUsage Requested Daily Log', get_daily_logs())
            elif command[-1] == 'week': send_email('PCUsage Requested Weekly Log', get_weekly_logs())
            elif command[-1] == 'month': send_email('PCUsage Requested Monthly Log', get_monthly_logs())
        elif command[0] == 'msg':
            send_notification(command[-1])
        else:
            send_email('Syntax Error', SYNTAX_ERROR)
    except:
        send_email('Syntax Error', SYNTAX_ERROR)

def check_emails():
    # Replace these values with your email server details
    email_server = 'imap.gmail.com'
    email_user = EMAIL_USER
    email_password = EMAIL_PASSWORD

    # Connect to the IMAP server
    mail = imaplib.IMAP4_SSL(email_server)

    # Log in to the email account
    mail.login(email_user, email_password)

    # Select the mailbox you want to monitor
    mail.select('inbox')

    # Search for all unseen (unread) emails
    status, messages = mail.search(None, 'UNSEEN')

    # Calculate the date 1 minute ago from the current time
    one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

    # Iterate through unseen emails
    for num in messages[0].split():
        # Fetch the email data
        status, msg_data = mail.fetch(num, '(RFC822)')
        if status == 'OK':
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            # Extract the email subject
            subject = msg.get('Subject', '')
            subject = subject.lower().strip()

            # Extract the email date
            date_str = msg.get('Date', '')
            email_date = parsedate_to_datetime(date_str)

            # Check if the subject contains a specific keyword and email is within the last 1 minute
            if 'pcusage command' == subject and email_date and email_date >= one_minute_ago:

                # Extract and print the email body
                email_body = ''
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            email_body = part.get_payload(decode=True).decode('utf-8', 'ignore')
                else:
                    email_body = msg.get_payload(decode=True).decode('utf-8', 'ignore')
                
                email_body = email_body.strip().lower()
                parse_command(email_body)

    # Logout from the email server
    mail.logout()

# Run the email checking function in a loop
while True:
    check_emails()
    # Add a delay to avoid continuous checking (you can adjust the duration)
    time.sleep(1)
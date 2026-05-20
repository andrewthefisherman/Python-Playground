import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from plyer import notification
import time
import os
import datetime
import pyautogui

LOG_FILE = "usage_log.txt"
CHECKER_FILE = "weekly_checker.txt"
EMAIL_USER = "YOUR GMAIL"
EMAIL_PASSWORD = "YOUR SMTP GMAIL PASSWORD"
TO_EMAIL = "EMAIL RECIPIENT (USUALLY SAME AS YOUR GMAIL)"

def calctime(seconds):
    hours = seconds // 3600
    remaining_seconds = seconds % 3600
    minutes = remaining_seconds // 60
    return f"{hours}:{minutes:02}h"

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

def log_usage():
    with open(LOG_FILE, 'a') as log:
        log.write(f"{datetime.date.today()} - {datetime.datetime.now().strftime('%H:%M:%S')} - 3900")

def send_weekly_report():
    if datetime.datetime.now().weekday() == 6:  # Sunday is the 6th day of the week (0-indexed)
        subject = "PCUsage Weekly Report"
        weekly_logs = get_weekly_logs()
        body = "Weekly Usage Log:\n\n" + weekly_logs
        send_email(subject, body)

def get_weekly_logs():
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    
    weekly_logs = []

    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            lines = log.readlines()
            for line in lines:
                date_str = line.split()[0]
                log_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

                if start_of_week <= log_date <= end_of_week:
                    t = int(line.split()[-1])
                    time_played = None
                    if log_date.weekday() == 5 or log_date.weekday() == 6:
                        time_played = calctime(24*60*60 - t)
                    else:
                        time_played = calctime(3900 - t)

                    line = line.strip() + f' - {time_played}\n'
                    weekly_logs.append(line)

    return ''.join(weekly_logs)

def update_log(log_file_path, new_number):
    today_date = datetime.date.today()
    today_date_str = today_date.strftime('%Y-%m-%d')

    with open(log_file_path, 'r') as log_file:
        lines = log_file.readlines()

    updated_lines = []
    for line in lines:
        if today_date_str in line:
            # Update the last number for today's date
            parts = line.split(' - ')
            parts[-1] = str(new_number)
            parts[1] = str(datetime.datetime.now().strftime('%H:%M:%S'))
            updated_line = ' - '.join(parts)
            updated_lines.append(updated_line + '\n')
        else:
            updated_lines.append(line)

    with open(log_file_path, 'w') as log_file:
        log_file.writelines(updated_lines)

def check_log():
    with open(LOG_FILE, 'r') as log:
            lines = log.readlines()
            for line in lines:
                parts = line.split(' - ')
                if parts[0].strip() == str(datetime.date.today()):
                    if parts[-1].strip() == '0':
                        return 0
                    else:
                        return int(parts[-1])
            return False

def send_notification(message):
    notification.notify(
        title='Tempo Limite',
        message=message,
        app_icon=None,
        timeout=10,
    )

def main():

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            pass
    if not os.path.exists(CHECKER_FILE):
        with open(CHECKER_FILE, 'w') as f:
            pass
    
    if datetime.datetime.now().weekday() == 6:  # Check if it's Sunday
        today_date = datetime.date.today()
        today_date_str = today_date.strftime('%Y-%m-%d')

        with open(CHECKER_FILE, 'r') as log_file:
            lines = log_file.readlines()

        notsent = True
        for line in lines:
            if today_date_str in line:
                notsent = True
            else: pass

        if notsent:
            send_weekly_report()
            with open(CHECKER_FILE, 'a') as file:
                file.write(f"{datetime.date.today()} = Sent!")

    if check_log():
        if check_log() <= 0:
            send_email('PCUsage Alert','User tried to access the PC more than once today.')
            update_log(LOG_FILE,60)
        else:
            t = check_log()
            time_left = calctime(t)
            send_notification(f'Tempo Limite è stato riattivato. {time_left} rimanenti')
    else:
        if datetime.datetime.now().weekday() == 5:
            log_usage()
            update_log(LOG_FILE, 24*60*60)
        else:
            log_usage()
            t = 5400

    r = 0
    countdown = False
    while t >= 0:
        time.sleep(1)
        t = check_log()
        if log_date.weekday() == 5 or log_date.weekday() == 6:
            if r == 1*60*60: send_notification("Il PC è in utilizzo da 1 ora consecutiva. Fai una pausa!")
        if r == 2*60*60: send_notification("Il PC è in utilizzo da 2 ore consecutive. Fai una pausa!")
        if r == 3*60*60: send_notification("Il PC è in utilizzo da 3 ore consecutive. Fai una pausa!")
        if r == 4*60*60: send_notification("Il PC è in utilizzo da 4 ore consecutive. Fai una pausa!")
        if r == 5*60*60: send_notification("Il PC è in utilizzo da 5 ore consecutive. Così è troppo!!!")
        if r == 6*60*60: send_notification("Sei arrivato a 6 ore. Lo sai che ti vedo. Direi di spegnere eh")
        if t == 3900: send_notification("Tempo Limite è attivato. 1:05h rimanenti")
        if t == 2700: send_notification("Tempo Limite: 0:45h rimanente")
        if t == 1800: send_notification("Tempo Limite: 0:30h rimanenti")
        if t == 60: send_notification("Tempo Limite Scaduto. Spegnimento automatico in 0:01h")
        if t < 60: countdown = True
        if countdown:
            if check_log() > 60:
                send_notification('Tempo Limite è stato riattivato')
                time.sleep(10)
                countdown = False
                main()

        r = r + 1
        t = t - 1
        update_log(LOG_FILE, t)

    pyautogui.hotkey('win','d')
    time.sleep(1)
    send_notification("Tempo limite raggiunto. Spegnimento in 0:01h")
    time.sleep(60)
    update_log(LOG_FILE, 0)

    os.system("shutdown /s /t 1")

if __name__ == "__main__":
    main()
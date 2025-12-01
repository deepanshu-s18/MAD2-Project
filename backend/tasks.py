from email import encoders
from email.mime.base import MIMEBase
from celery_setup import celery
from celery.schedules import crontab
from models import User, Reservation
from jinja2 import Template
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import os

def create_report(user_name, data):
    with open("report_template.html", "r") as f:
        template = Template(f.read())
        return template.render(user_name=user_name, data=data)

def send_email(to_email, subject, content, attachment=None):
    smtp_host = "127.0.0.1"
    smtp_port = 1025
    from_email = "admin@gmail.com"
    password = "admin"
    
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(content, "html"))
    
    if attachment:
        with open(attachment, "rb") as f:
            part = MIMEBase("text", "csv")
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(attachment)}"')
            msg.attach(part)
    
    server = smtplib.SMTP(host=smtp_host, port=smtp_port)
    # server.login(from_email, password)
    server.send_message(msg)
    server.quit()
    
    print('Email sent')
    
    if attachment and os.path.exists(attachment):
        os.remove(attachment)

@celery.on_after_configure.connect
def setup_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, daily_reminder.s(), name='daily reminder')
    sender.add_periodic_task(40.0, monthly_report.s(), name='monthly report')
    sender.add_periodic_task(30.0, test.s('test'), expires=10)
    
    sender.add_periodic_task(crontab(hour=7, minute=30), daily_reminder.s())
    sender.add_periodic_task(crontab(hour=7, minute=30, day_of_month=1), monthly_report.s())

@celery.task
def test(arg):
    print(arg)

@celery.task
def daily_reminder():
    users = User.query.filter_by(role='customer').all()
    
    for user in users:
        content = f'<h1>Daily Parking Reminder for {user.name}</h1>'
        send_email(user.email, 'Daily Reminder', content)
    
    print('Daily reminders sent')

@celery.task
def send_new_lot_alert():
    users = User.query.filter_by(role='customer').all()
    
    for user in users:
        content = f'<h1>New parking location available, {user.name}!</h1>'
        send_email(user.email, 'New Location Alert', content)
    
    print('New location alerts sent')

@celery.task
def monthly_report():
    users = User.query.filter_by(role='customer').all()
    
    for user in users:
        reservations = Reservation.query.filter_by(user_id=user.id).all()
        data = []
        
        for res in reservations:
            data.append([
                res.id,
                res.vehicle_number,
                res.parking_time,
                res.leaving_time,
                res.status
            ])
        
        report = create_report(user.name, data)
        send_email(user.email, 'Monthly Report', report)
        
        print(f'Report sent to {user.email}')

@celery.task
def export_data(reservations, email):
    if not reservations:
        return 'No data to export'
        
    filename = 'export.csv'
    
    with open(filename, 'w', newline='') as f:
        fields = list(reservations[0].keys())
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reservations)
    
    send_email(email, 'Data Export', f'Your data has been exported', filename)
    
    return 'Export complete'

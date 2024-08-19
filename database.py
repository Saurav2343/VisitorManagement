import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import os
def init_db():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()

    # # Drop existing tables if they exist
    # c.execute('DROP TABLE IF EXISTS employees')
    # c.execute('DROP TABLE IF EXISTS visitors')

    # Create employees table with ID as primary key
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
                    eid INTEGER PRIMARY KEY ,
                    email TEXT NOT NULL UNIQUE,
                    phone_number TEXT UNIQUE,
                    name TEXT NOT NULL)''')

    # Create visitors table with host_id referencing employees table
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    visit_date TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    contact TEXT UNIQUE,
                    host_id INTEGER,
                    FOREIGN KEY (host_id) REFERENCES employees (id))''')

    conn.commit()
    conn.close()

def add_employee(eid,email,phone_number, name):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (eid, email,phone_number, name) VALUES (?, ?,?, ?)", (eid ,email,phone_number, name))
    conn.commit()
    conn.close()

def get_employee_id_by_email(email):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("SELECT eid FROM employees WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None
def get_employee_phone_number(host_id):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("SELECT phone_number FROM employees WHERE eid = ?", (host_id,))
    host_phone_number = c.fetchone()
    conn.close()
    if host_phone_number:
        return host_phone_number
    return None
def add_visitor(name, visit_date, purpose, contact, host_email):
    host_id = get_employee_id_by_email(host_email)
    if host_id is None:
        return False
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("INSERT INTO visitors (name, visit_date, purpose, contact, host_id) VALUES (?, ?, ?, ?, ?)",
              (name, visit_date, purpose, contact, host_id))
    conn.commit()
    conn.close()
    #host_phone_number = get_employee_phone_number(host_id)
    send_email_to_host(host_email, name, visit_date, purpose, contact)
    #send_sms(host_phone_number, name, visit_date, purpose, contact)
    return True

def get_visitors():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''SELECT visitors.id, visitors.name, visitors.visit_date, visitors.purpose, visitors.contact, employees.email
                 FROM visitors
                 JOIN employees ON visitors.host_id = employees.eid''')
    records = c.fetchall()
    conn.close()
    return records

def search_visitors(name):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''SELECT visitors.id, visitors.name, visitors.visit_date, visitors.purpose, visitors.contact, employees.email
                 FROM visitors
                 JOIN employees ON visitors.host_id = employees.eid
                 WHERE visitors.name LIKE ?''', ('%' + name + '%',))
    records = c.fetchall()
    conn.close()
    return records
def send_sms(host_phone_number, visitor_name, visit_date, purpose, contact):
    account_sid = 'sender'
    auth_token = 'nm'
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body=f'A visitor has entered on your name.\n\nDetails:\nName: {visitor_name}\nDate: {visit_date}\nPurpose: {purpose}\nContact: {contact}',
            from_='senderphone',  # Your Twilio number
            to=host_phone_number   # Recipient's number
        )
        print(message.sid)
    except Exception as e:
        print(f"Failed to send SMS: {e}")

def send_email_to_host(host_email, visitor_name, visit_date, purpose, contact):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'sender_gmail'
    sender_password = 'sender_password'

    # Email content
    subject = 'Visitor Notification'
    body = f'A visitor has entered on your name.\n\nDetails:\nName: {visitor_name}\nDate: {visit_date}\nPurpose: {purpose}\nContact: {contact}'

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = host_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, host_email, msg.as_string())
        server.quit()
        print(f'Email sent to {host_email}')
    except Exception as e:
        print(f'Failed to send email to {host_email}: {str(e)}')

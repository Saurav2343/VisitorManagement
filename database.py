import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def init_db():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()

    # Create employees table with ID as primary key
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    name TEXT NOT NULL)''')

    # Create visitors table with host_id referencing employees table
    c.execute('''CREATE TABLE IF NOT EXISTS visitors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    visit_date TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    contact TEXT,
                    host_id INTEGER,
                    FOREIGN KEY (host_id) REFERENCES employees (id))''')

    conn.commit()
    conn.close()

def add_employee(email, name):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("INSERT INTO employees (email, name) VALUES (?, ?)", (email, name))
    conn.commit()
    conn.close()

def get_employee_id_by_email(email):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute("SELECT id FROM employees WHERE email = ?", (email,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
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
    send_email_to_host(host_email, name, visit_date, purpose, contact)
    return True

def get_visitors():
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''SELECT visitors.id, visitors.name, visitors.visit_date, visitors.purpose, visitors.contact, employees.email
                 FROM visitors
                 JOIN employees ON visitors.host_id = employees.id''')
    records = c.fetchall()
    conn.close()
    return records

def search_visitors(name):
    conn = sqlite3.connect('visitors.db')
    c = conn.cursor()
    c.execute('''SELECT visitors.id, visitors.name, visitors.visit_date, visitors.purpose, visitors.contact, employees.email
                 FROM visitors
                 JOIN employees ON visitors.host_id = employees.id
                 WHERE visitors.name LIKE ?''', ('%' + name + '%',))
    records = c.fetchall()
    conn.close()
    return records

def send_email_to_host(host_email, visitor_name, visit_date, purpose, contact):
    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'

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

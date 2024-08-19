# Visitor Management System

A Visitor Management System built with Python, SQLite, and Tkinter. This system allows you to manage visitor entries, send notification emails and sms to host employees, and view/search visitor records.

## Project Structure

- `database.py`: Contains functions for database operations and email sending.
- `gui.py`: Contains the code for the GUI application.
- `main.py`: Initializes the database and starts the GUI.
- `add_employees.py`: Script to add employee details to the database.
- `visitors.db`: SQLite database file (created automatically).

## Setup and Installation

### Prerequisites

- Python 3.x installed on your system.
- SQLite3 (usually comes pre-installed with Python).

### Install Required Libraries

Make sure you have the following standard libraries: `sqlite3`, `tkinter`,'twilio' and `smtplib`. These should come pre-installed with Python.

### SMTP Configuration

In `database.py`, update the `send_email_to_host` function with your actual email and password. If you're using Gmail, you might need to enable "Less secure app access" or use an App Password for your Google account.
In `database.py`, update the `send_sms` function with your actual accont_sid,auth_token and from_.

### Initialize the Database and Add Employees

1. **Initialize the Database**: Run `main.py` to create the necessary database tables:
    python main.py
2. ** Add Employee Details**: Run 'add_employees.py' to add employee details:
    python add_employees.py
3. *Running the Application**: Run 'main.py'

## Usage
1. Run the main script to start the application:
    ```sh
    python main.py
    ```
2. Use the GUI to add, view, and search visitors.
3. To add a new employee, use the `add_employees.py` before starting the GUI:
    ```python
    import database
    database.add_employee(12, "john.doe@example.com", "+18777804236", "John Doe")
    ```

## License

### Summary

- **Project Structure**: Details the files in your project.
- **Setup and Installation**: Instructions for prerequisites, library installation, and SMTP configuration.
- **Initialize the Database and Add Employees**: Steps to set up the database and add employee records.
- **Running the Application**: How to start the GUI application.
- **Usage**: Instructions for adding, viewing, and searching visitors.

This `README.md` file provides clear and comprehensive guidance on setting up and using the Visitor Management System.

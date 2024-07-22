import database

def add_employees():
    employees = [
        ("john.doe@example.com", "John Doe"),
        ("jane.smith@example.com", "Jane Smith"),
        ("bob.johnson@example.com", "Bob Johnson"),
        # Add more employees as needed
    ]

    for email, name in employees:
        database.add_employee(email, name)
        print(f"Added employee: {name} ({email})")

if __name__ == '__main__':
    add_employees()

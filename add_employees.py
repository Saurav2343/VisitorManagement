import database

def add_employees():
    employees = [
        (12,"john.doe@example.com", "John Doe"),
        (34,"jane.smith@example.com", "Jane Smith"),
        (43,"bob.johnson@example.com", "Bob Johnson"),
        # Add more employees as needed
    ]

    for eid,email, name in employees:
        database.add_employee(eid,email, name)
        print(f"Added employee:{eid} {name} ({email})")

if __name__ == '__main__':
    add_employees()

import database

def add_employees():
    employees = [
        (12, "john.doe@example.com", "+18777804236", "John Doe"),
        (34, "jane.smith@example.com", "9876543210", "Jane Smith"),
        (43, "bob.johnson@example.com", "1122334455", "Bob Johnson"),
        # Add more employees as needed
    ]

    for eid, email, phone_number, name in employees:
        try:
            database.add_employee(eid, email, phone_number, name)
            print(f"Added employee: {eid} {name} {phone_number} ({email})")
        except Exception as e:
            print(f"Failed to add employee: {eid} {name} {phone_number} ({email}) - {e}")

if __name__ == '__main__':
    add_employees()

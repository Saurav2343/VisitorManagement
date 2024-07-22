import tkinter as tk
from tkinter import messagebox, ttk
import database

def start_gui():
    root = tk.Tk()
    root.title("Visitor Management System")
    root.geometry("500x450")

    name_label = tk.Label(root, text="Name")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    visit_date_label = tk.Label(root, text="Visit Date (YYYY-MM-DD)")
    visit_date_label.pack()
    visit_date_entry = tk.Entry(root)
    visit_date_entry.pack()

    purpose_label = tk.Label(root, text="Purpose")
    purpose_label.pack()
    purpose_entry = tk.Entry(root)
    purpose_entry.pack()

    contact_label = tk.Label(root, text="Contact")
    contact_label.pack()
    contact_entry = tk.Entry(root)
    contact_entry.pack()

    host_email_label = tk.Label(root, text="Host Employee Email")
    host_email_label.pack()
    host_email_entry = tk.Entry(root)
    host_email_entry.pack()

    def add_visitor():
        name = name_entry.get()
        visit_date = visit_date_entry.get()
        purpose = purpose_entry.get()
        contact = contact_entry.get()
        host_email = host_email_entry.get()

        if name and visit_date and purpose and host_email:
            if database.add_visitor(name, visit_date, purpose, contact, host_email):
                messagebox.showinfo("Success", "Visitor added successfully and email sent to host!")
            else:
                messagebox.showerror("Error", "Host employee email not found.")
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    add_visitor_button = tk.Button(root, text="Add Visitor", command=add_visitor)
    add_visitor_button.pack()

    def view_visitors():
        records = database.get_visitors()
        view_window = tk.Toplevel(root)
        view_window.title("View Visitors")

        tree = ttk.Treeview(view_window, columns=("ID", "Name", "Visit Date", "Purpose", "Contact", "Host Email"), show='headings')
        tree.heading("ID", text="ID")
        tree.heading("Name", text="Name")
        tree.heading("Visit Date", text="Visit Date")
        tree.heading("Purpose", text="Purpose")
        tree.heading("Contact", text="Contact")
        tree.heading("Host Email", text="Host Email")
        tree.pack(fill=tk.BOTH, expand=True)

        for record in records:
            tree.insert("", tk.END, values=record)

    view_visitors_button = tk.Button(root, text="View Visitors", command=view_visitors)
    view_visitors_button.pack()

    def search_visitor():
        search_window = tk.Toplevel(root)
        search_window.title("Search Visitor")

        search_label = tk.Label(search_window, text="Enter Name to Search")
        search_label.pack()
        search_entry = tk.Entry(search_window)
        search_entry.pack()

        def search():
            name = search_entry.get()
            records = database.search_visitors(name)
            for widget in search_window.winfo_children():
                if isinstance(widget, ttk.Treeview):
                    widget.destroy()

            tree = ttk.Treeview(search_window, columns=("ID", "Name", "Visit Date", "Purpose", "Contact", "Host Email"), show='headings')
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Visit Date", text="Visit Date")
            tree.heading("Purpose", text="Purpose")
            tree.heading("Contact", text="Contact")
            tree.heading("Host Email", text="Host Email")
            tree.pack(fill=tk.BOTH, expand=True)

            for record in records:
                tree.insert("", tk.END, values=record)

        search_button = tk.Button(search_window, text="Search", command=search)
        search_button.pack()

    search_visitor_button = tk.Button(root, text="Search Visitor", command=search_visitor)
    search_visitor_button.pack()

    root.mainloop()

"""
main.py
-------
Rental Vehicle Management System - Tkinter user interface.
Run with:  python main.py

The window has 5 tabs:
    1. Vehicles       - add + view vehicles
    2. Rent Vehicle   - rent an available vehicle (saves customer details)
    3. Return Vehicle - return a rented vehicle and see the bill
    4. Customers      - view customer details
    5. Rental Status  - history of all rentals
"""

import tkinter as tk
from tkinter import ttk, messagebox

import database


class RentalApp:
    def __init__(self, root):
        self.root = root
        root.title("Rental Vehicle Management System")
        root.geometry("850x500")

        ttk.Label(root, text="Rental Vehicle Management System",
                  font=("Arial", 16, "bold")).pack(pady=8)

        # Notebook = the tabs
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=5)

        self.build_vehicles_tab()
        self.build_rent_tab()
        self.build_return_tab()
        self.build_customers_tab()
        self.build_status_tab()

        # Refresh the tables every time the user switches tab
        self.tabs.bind("<<NotebookTabChanged>>", lambda e: self.refresh_all())
        self.refresh_all()

    # ------------------------------------------------------------ helpers
    def make_table(self, parent, columns, widths):
        """Create a Treeview (table) with a scrollbar."""
        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True, padx=5, pady=5)
        table = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        for col, w in zip(columns, widths):
            table.heading(col, text=col)
            table.column(col, width=w, anchor="center")
        scroll = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scroll.set)
        table.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return table

    def fill_table(self, table, rows):
        """Clear a table and fill it with new rows."""
        table.delete(*table.get_children())
        for row in rows:
            table.insert("", "end", values=row)

    def add_field(self, parent, label, row):
        """Add a label + text box to a grid. Returns the Entry widget."""
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=4)
        entry = ttk.Entry(parent, width=28)
        entry.grid(row=row, column=1, padx=5, pady=4)
        return entry

    # ------------------------------------------------------- 1. vehicles
    def build_vehicles_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Vehicles")

        form = ttk.LabelFrame(tab, text="Add New Vehicle")
        form.pack(fill="x", padx=5, pady=5)

        self.v_name = self.add_field(form, "Vehicle Name:", 0)
        ttk.Label(form, text="Type:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.v_type = ttk.Combobox(form, values=["Car", "Bike", "Scooter", "Van"],
                                   state="readonly", width=25)
        self.v_type.current(0)
        self.v_type.grid(row=1, column=1, padx=5, pady=4)
        self.v_reg = self.add_field(form, "Registration No:", 2)
        self.v_price = self.add_field(form, "Price per Day (Rs):", 3)
        ttk.Button(form, text="Add Vehicle", command=self.add_vehicle).grid(
            row=4, column=1, sticky="w", padx=5, pady=8)

        self.vehicle_table = self.make_table(
            tab, ("ID", "Name", "Type", "Reg No", "Price/Day", "Status"),
            (50, 180, 90, 130, 100, 100))

    def add_vehicle(self):
        name = self.v_name.get().strip()
        v_type = self.v_type.get()
        reg = self.v_reg.get().strip().upper()
        price_text = self.v_price.get().strip()

        # Validation
        if not name or not reg or not price_text:
            messagebox.showwarning("Missing data", "Please fill in all fields.")
            return
        try:
            price = float(price_text)
            if price <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid price", "Price must be a number greater than 0.")
            return

        if database.add_vehicle(name, v_type, reg, price):
            messagebox.showinfo("Success", f"{name} added successfully.")
            for box in (self.v_name, self.v_reg, self.v_price):
                box.delete(0, "end")
            self.refresh_all()
        else:
            messagebox.showerror("Duplicate", "A vehicle with this registration number already exists.")

    # ------------------------------------------------------- 2. rent
    def build_rent_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Rent Vehicle")

        form = ttk.LabelFrame(tab, text="Rent a Vehicle")
        form.pack(fill="x", padx=5, pady=5)

        ttk.Label(form, text="Select Vehicle:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.rent_vehicle_box = ttk.Combobox(form, state="readonly", width=40)
        self.rent_vehicle_box.grid(row=0, column=1, padx=5, pady=4)

        self.c_name = self.add_field(form, "Customer Name:", 1)
        self.c_phone = self.add_field(form, "Phone (10 digits):", 2)
        self.c_license = self.add_field(form, "Driving Licence No:", 3)
        self.c_days = self.add_field(form, "Number of Days:", 4)
        ttk.Button(form, text="Rent Vehicle", command=self.rent_vehicle).grid(
            row=5, column=1, sticky="w", padx=5, pady=8)

        self.available_vehicles = []   # remembers the vehicle behind each dropdown item

    def rent_vehicle(self):
        index = self.rent_vehicle_box.current()
        name = self.c_name.get().strip()
        phone = self.c_phone.get().strip()
        license_no = self.c_license.get().strip().upper()
        days_text = self.c_days.get().strip()

        # Validation
        if index < 0:
            messagebox.showwarning("No vehicle", "Please select a vehicle.")
            return
        if not name or not phone or not license_no or not days_text:
            messagebox.showwarning("Missing data", "Please fill in all customer details.")
            return
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showwarning("Invalid phone", "Phone number must be exactly 10 digits.")
            return
        if not days_text.isdigit() or int(days_text) < 1:
            messagebox.showwarning("Invalid days", "Days must be a whole number (1 or more).")
            return

        vehicle = self.available_vehicles[index]
        days = int(days_text)
        if database.rent_vehicle(vehicle[0], name, phone, license_no, days):
            estimate = days * vehicle[4]
            messagebox.showinfo("Rented",
                                f"{vehicle[1]} rented to {name} for {days} day(s).\n"
                                f"Estimated cost: Rs {estimate:.2f}")
            for box in (self.c_name, self.c_phone, self.c_license, self.c_days):
                box.delete(0, "end")
            self.refresh_all()
        else:
            messagebox.showerror("Not available", "This vehicle is not available.")
            self.refresh_all()

    # ------------------------------------------------------- 3. return
    def build_return_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Return Vehicle")

        ttk.Label(tab, text="Select a rental below and click 'Return Vehicle'.").pack(pady=5)
        self.return_table = self.make_table(
            tab, ("Rental ID", "Vehicle", "Reg No", "Customer", "Phone", "Rent Date", "Days"),
            (70, 130, 100, 130, 100, 100, 50))
        ttk.Button(tab, text="Return Vehicle", command=self.return_vehicle).pack(pady=5)

    def return_vehicle(self):
        selected = self.return_table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a rental first.")
            return
        rental_id = self.return_table.item(selected[0])["values"][0]

        result = database.return_vehicle(rental_id)
        if result is None:
            messagebox.showerror("Error", "Rental not found.")
        else:
            days_used, total = result
            messagebox.showinfo("Vehicle Returned",
                                f"Days used: {days_used}\nTotal bill: Rs {total:.2f}")
        self.refresh_all()

    # ------------------------------------------------------- 4. customers
    def build_customers_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Customers")
        self.customer_table = self.make_table(
            tab, ("ID", "Name", "Phone", "Licence No"), (50, 200, 150, 180))

    # ------------------------------------------------------- 5. status
    def build_status_tab(self):
        tab = ttk.Frame(self.tabs)
        self.tabs.add(tab, text="Rental Status")
        self.status_table = self.make_table(
            tab, ("ID", "Vehicle", "Reg No", "Customer", "Rent Date", "Days",
                  "Return Date", "Bill (Rs)", "Status"),
            (40, 110, 90, 110, 90, 45, 90, 70, 70))

    # ------------------------------------------------------- refresh
    def refresh_all(self):
        """Reload every table / dropdown from the database."""
        self.fill_table(self.vehicle_table, database.get_vehicles())
        self.fill_table(self.return_table, database.get_active_rentals())
        self.fill_table(self.customer_table, database.get_customers())
        self.fill_table(self.status_table, database.get_all_rentals())

        self.available_vehicles = database.get_vehicles(only_available=True)
        self.rent_vehicle_box["values"] = [
            f"{v[1]} ({v[3]}) - Rs {v[4]:.0f}/day" for v in self.available_vehicles]
        self.rent_vehicle_box.set("")


if __name__ == "__main__":
    database.init_db()          # make sure tables exist
    window = tk.Tk()
    RentalApp(window)
    window.mainloop()

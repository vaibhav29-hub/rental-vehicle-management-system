"""
database.py
-----------
All SQLite (database) code lives here, so the UI file stays simple.
SQLite is built into Python, so nothing needs to be installed.

Tables:
    vehicles  -> the cars/bikes we own
    customers -> people who rent
    rentals   -> which customer rented which vehicle, and when
"""

import os
import sqlite3
from datetime import date

# The database file is created next to this script.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rental.db")


def get_connection():
    """Open a connection to the database file."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create the tables if they do not exist yet."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT NOT NULL,
            type         TEXT NOT NULL,
            reg_no       TEXT NOT NULL UNIQUE,
            price_per_day REAL NOT NULL,
            status       TEXT NOT NULL DEFAULT 'Available'
        )""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            phone      TEXT NOT NULL,
            license_no TEXT NOT NULL UNIQUE
        )""")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rentals (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_id  INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            rent_date   TEXT NOT NULL,
            days        INTEGER NOT NULL,
            return_date TEXT,
            total_cost  REAL,
            status      TEXT NOT NULL DEFAULT 'Active',
            FOREIGN KEY (vehicle_id)  REFERENCES vehicles(id),
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )""")
    conn.commit()
    conn.close()


# ---------------------------------------------------------------- vehicles
def add_vehicle(name, v_type, reg_no, price_per_day):
    """Add a vehicle. Returns False if the registration number already exists."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO vehicles (name, type, reg_no, price_per_day) VALUES (?, ?, ?, ?)",
            (name, v_type, reg_no, price_per_day),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:      # reg_no is UNIQUE
        return False
    finally:
        conn.close()


def get_vehicles(only_available=False):
    """Return all vehicles (or only the available ones)."""
    conn = get_connection()
    sql = "SELECT id, name, type, reg_no, price_per_day, status FROM vehicles"
    if only_available:
        sql += " WHERE status = 'Available'"
    rows = conn.execute(sql + " ORDER BY id").fetchall()
    conn.close()
    return rows


# ------------------------------------------------------------------ rental
def rent_vehicle(vehicle_id, cust_name, phone, license_no, days):
    """
    Rent a vehicle to a customer.
    Returns True on success, False if the vehicle is not available.
    """
    conn = get_connection()
    try:
        row = conn.execute("SELECT status FROM vehicles WHERE id = ?",
                           (vehicle_id,)).fetchone()
        if row is None or row[0] != "Available":
            return False

        # Re-use the customer if the licence number is already saved.
        cust = conn.execute("SELECT id FROM customers WHERE license_no = ?",
                            (license_no,)).fetchone()
        if cust:
            customer_id = cust[0]
            conn.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?",
                         (cust_name, phone, customer_id))
        else:
            cur = conn.execute(
                "INSERT INTO customers (name, phone, license_no) VALUES (?, ?, ?)",
                (cust_name, phone, license_no))
            customer_id = cur.lastrowid

        conn.execute(
            "INSERT INTO rentals (vehicle_id, customer_id, rent_date, days) VALUES (?, ?, ?, ?)",
            (vehicle_id, customer_id, date.today().isoformat(), days))
        conn.execute("UPDATE vehicles SET status = 'Rented' WHERE id = ?", (vehicle_id,))
        conn.commit()
        return True
    finally:
        conn.close()


def get_active_rentals():
    """Rentals that have not been returned yet."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT r.id, v.name, v.reg_no, c.name, c.phone, r.rent_date, r.days
        FROM rentals r
        JOIN vehicles  v ON v.id = r.vehicle_id
        JOIN customers c ON c.id = r.customer_id
        WHERE r.status = 'Active'
        ORDER BY r.id""").fetchall()
    conn.close()
    return rows


def return_vehicle(rental_id):
    """
    Return a vehicle. The bill is based on the days actually used
    (minimum 1 day). Returns (days_used, total_cost) or None if not found.
    """
    conn = get_connection()
    try:
        row = conn.execute("""
            SELECT r.rent_date, r.vehicle_id, v.price_per_day
            FROM rentals r JOIN vehicles v ON v.id = r.vehicle_id
            WHERE r.id = ? AND r.status = 'Active'""", (rental_id,)).fetchone()
        if row is None:
            return None

        rent_date, vehicle_id, price = row
        days_used = max(1, (date.today() - date.fromisoformat(rent_date)).days)
        total = days_used * price

        conn.execute("""UPDATE rentals
                        SET return_date = ?, total_cost = ?, status = 'Returned'
                        WHERE id = ?""",
                     (date.today().isoformat(), total, rental_id))
        conn.execute("UPDATE vehicles SET status = 'Available' WHERE id = ?",
                     (vehicle_id,))
        conn.commit()
        return days_used, total
    finally:
        conn.close()


def get_all_rentals():
    """Every rental (active and returned) for the Rental Status tab."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT r.id, v.name, v.reg_no, c.name, r.rent_date, r.days,
               IFNULL(r.return_date, '-'), IFNULL(r.total_cost, '-'), r.status
        FROM rentals r
        JOIN vehicles  v ON v.id = r.vehicle_id
        JOIN customers c ON c.id = r.customer_id
        ORDER BY r.id DESC""").fetchall()
    conn.close()
    return rows


# --------------------------------------------------------------- customers
def get_customers():
    conn = get_connection()
    rows = conn.execute("SELECT id, name, phone, license_no FROM customers ORDER BY id").fetchall()
    conn.close()
    return rows

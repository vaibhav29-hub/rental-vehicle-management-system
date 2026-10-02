# Rental Vehicle Management System

A beginner-friendly desktop app built with **Python + Tkinter + SQLite** for managing vehicle rentals.

## Features
- Add vehicles (name, type, registration no, price per day)
- View all vehicles with live status (Available / Rented)
- Rent a vehicle and save customer details
- Return a vehicle and get an automatic bill
- View customer details
- View rental status / history
- Input validation (empty fields, 10-digit phone, positive price/days, duplicate registration number)

## Folder Structure
```
rental-vehicle-management-system/
├── main.py              # Tkinter UI (5 tabs)
├── database.py          # All SQLite code
├── tests/
│   └── test_database.py # Unit tests
├── docs/
│   └── KANBAN_TASKS.md  # GitHub issues for the Kanban board
├── scripts/
│   └── create_issues.sh # Optional: creates the issues using GitHub CLI
├── .gitignore
└── README.md
```

## Setup
1. Install Python 3.8+ (Tkinter and SQLite come bundled with Python on Windows/macOS).
   On Linux: `sudo apt install python3-tk`
2. Download or clone the project:
   ```
   git clone https://github.com/<your-username>/rental-vehicle-management-system.git
   cd rental-vehicle-management-system
   ```
3. Run the app (no extra packages needed):
   ```
   python main.py
   ```
   The database file `rental.db` is created automatically on first run.

## How to Use
1. **Vehicles tab** - fill the form and click *Add Vehicle*.
2. **Rent Vehicle tab** - pick an available vehicle, enter customer details and days, click *Rent Vehicle*.
3. **Return Vehicle tab** - select a rental, click *Return Vehicle* to see the bill.
4. **Customers / Rental Status tabs** - view saved data.

## Billing Rule
Bill = (days actually used) x (price per day). Minimum charge is 1 day.

## Run Tests
```
python -m unittest discover tests
```

## Database Design
| Table | Columns |
|---|---|
| vehicles | id, name, type, reg_no (unique), price_per_day, status |
| customers | id, name, phone, license_no (unique) |
| rentals | id, vehicle_id, customer_id, rent_date, days, return_date, total_cost, status |

## Viva Quick Answers
- **Why SQLite?** Built into Python, needs no server, stores data in one file.
- **Why two files?** `database.py` handles data, `main.py` handles the screen (separation of concerns).
- **Why `?` in SQL queries?** Parameterised queries prevent SQL injection.
- **How is a vehicle blocked from double rental?** `rent_vehicle()` checks status is `Available` before renting.
- **What is Treeview?** The Tkinter widget used to display tables.
- **What is Notebook?** The Tkinter widget that creates tabs.

## Possible Future Improvements
Edit/delete vehicles, search and filter, late fees, login system, export to CSV.

# Kanban Tasks (GitHub Issues)

Board columns: **Backlog -> To Do -> In Progress -> Testing -> Done**

| # | Title | Label | Description |
|---|---|---|---|
| 1 | Project setup and repository structure | setup | Create repo, folders, .gitignore, first commit |
| 2 | Design database schema | database | Tables: vehicles, customers, rentals |
| 3 | Implement database helper functions | database | init_db, add, get, rent, return functions in database.py |
| 4 | Design main window and tabs | ui | Tkinter window with Notebook tabs and title |
| 5 | Add vehicle form | vehicle | Form fields + Add button saving to the database |
| 6 | View vehicles table | vehicle | Treeview showing all vehicles and status |
| 7 | Customer details storage and view | customer | Save customer on rent; Customers tab table |
| 8 | Rent vehicle functionality | rental | Rent tab: choose available vehicle, enter customer, save rental |
| 9 | Return vehicle and bill calculation | rental | Return tab: pick rental, calculate bill, free the vehicle |
| 10 | Rental status screen | rental | Table of all active and returned rentals |
| 11 | Input validation | validation | Empty fields, phone digits, numeric price/days |
| 12 | Write unit tests for database | testing | unittest cases for add, rent, return, duplicates |
| 13 | Manual testing of full workflow | testing | Add -> rent -> return -> check status, note results |
| 14 | Fix bugs found in testing | bug | Duplicate reg no, double rental, refresh issues |
| 15 | Write README and documentation | documentation | Setup, usage, structure, viva notes |

## Suggested starting columns
- Backlog: 12, 13, 14, 15 (later work)
- To Do: 9, 10, 11
- In Progress: 8
- Testing: 5, 6, 7
- Done: 1, 2, 3, 4

(Move cards honestly as you actually finish them - your professor will check the board history.)

#!/usr/bin/env bash
# Creates the 15 project issues using GitHub CLI (https://cli.github.com).
# Run from the project folder AFTER pushing to GitHub:
#   gh auth login
#   bash scripts/create_issues.sh
set -e

mk() { gh issue create --title "$1" --label "$2" --body "$3"; }

for l in setup database ui vehicle customer rental validation testing bug documentation; do
  gh label create "$l" --force >/dev/null
done

mk "Project setup and repository structure" setup "Create repo, folders, .gitignore, first commit."
mk "Design database schema" database "Tables: vehicles, customers, rentals."
mk "Implement database helper functions" database "init_db, add, get, rent, return functions in database.py."
mk "Design main window and tabs" ui "Tkinter window with Notebook tabs and title."
mk "Add vehicle form" vehicle "Form fields + Add button saving to the database."
mk "View vehicles table" vehicle "Treeview showing all vehicles and status."
mk "Customer details storage and view" customer "Save customer on rent; Customers tab table."
mk "Rent vehicle functionality" rental "Choose available vehicle, enter customer details, save rental."
mk "Return vehicle and bill calculation" rental "Pick rental, calculate bill, mark vehicle available."
mk "Rental status screen" rental "Table of all active and returned rentals."
mk "Input validation" validation "Empty fields, 10-digit phone, numeric price and days."
mk "Write unit tests for database" testing "unittest cases for add, rent, return, duplicates."
mk "Manual testing of full workflow" testing "Add -> rent -> return -> check status, record results."
mk "Fix bugs found in testing" bug "Duplicate reg no, double rental, refresh issues."
mk "Write README and documentation" documentation "Setup, usage, structure, viva notes."
echo "Done. Now add the issues to your Project board (see README / chat steps)."

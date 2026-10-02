"""Simple tests for database.py. Run from the project folder:  python -m unittest discover tests"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database


class TestDatabase(unittest.TestCase):
    def setUp(self):
        # Use a temporary database so real data is never touched
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.tmp.close()
        database.DB_PATH = self.tmp.name
        database.init_db()

    def tearDown(self):
        os.remove(self.tmp.name)

    def test_add_vehicle(self):
        self.assertTrue(database.add_vehicle("Swift", "Car", "MH01AB1234", 1500))
        self.assertEqual(len(database.get_vehicles()), 1)

    def test_duplicate_registration_rejected(self):
        database.add_vehicle("Swift", "Car", "MH01AB1234", 1500)
        self.assertFalse(database.add_vehicle("Other", "Car", "MH01AB1234", 900))

    def test_rent_marks_vehicle_rented(self):
        database.add_vehicle("Swift", "Car", "MH01AB1234", 1500)
        vid = database.get_vehicles()[0][0]
        self.assertTrue(database.rent_vehicle(vid, "Asha", "9876543210", "DL123", 2))
        self.assertEqual(database.get_vehicles()[0][5], "Rented")
        self.assertEqual(len(database.get_customers()), 1)

    def test_cannot_rent_twice(self):
        database.add_vehicle("Swift", "Car", "MH01AB1234", 1500)
        vid = database.get_vehicles()[0][0]
        database.rent_vehicle(vid, "Asha", "9876543210", "DL123", 2)
        self.assertFalse(database.rent_vehicle(vid, "Ravi", "9123456780", "DL456", 1))

    def test_return_vehicle_calculates_bill(self):
        database.add_vehicle("Swift", "Car", "MH01AB1234", 1500)
        vid = database.get_vehicles()[0][0]
        database.rent_vehicle(vid, "Asha", "9876543210", "DL123", 2)
        rental_id = database.get_active_rentals()[0][0]
        days, total = database.return_vehicle(rental_id)
        self.assertEqual((days, total), (1, 1500))      # same day = minimum 1 day
        self.assertEqual(database.get_vehicles()[0][5], "Available")
        self.assertEqual(database.get_active_rentals(), [])


if __name__ == "__main__":
    unittest.main()

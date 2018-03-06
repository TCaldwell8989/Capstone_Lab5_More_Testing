
import mileage
from mileage import MileageError
import sqlite3
from unittest import TestCase

class TestMileageDB(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url

        mileage.create_database()

        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()


    def test_add_new_vehicle(self):
        mileage.add_miles('Blue Car', 100)
        expected = { 'BLUE CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Green Car', 50)
        expected['GREEN CAR'] = 50
        self.compare_db_to_expected(expected)


    def test_increase_miles_for_vehicle(self):
        mileage.add_miles('Red Car', 100)
        expected = { 'RED CAR': 100 }
        self.compare_db_to_expected(expected)

        mileage.add_miles('Red Car', 50)
        expected['RED CAR'] = 100 + 50
        self.compare_db_to_expected(expected)


    def test_add_new_vehicle_no_vehicle(self):
        with self.assertRaises(Exception):
            mileage.addMiles(None, 100)


    def test_add_new_vehicle_invalid_new_miles(self):
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', -100)
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', 'abc')
        with self.assertRaises(MileageError):
            mileage.add_miles('Car', '12.def')


    # This is not a test method, instead, it's used by the test methods
    def compare_db_to_expected(self, expected):

        conn = sqlite3.connect(self.test_db_url)
        cursor = conn.cursor()
        all_data = cursor.execute('SELECT * FROM MILES').fetchall()

        # Same rows in DB as entries in expected dictionary
        self.assertEqual(len(expected.keys()), len(all_data))

        for row in all_data:
            # Vehicle exists, and mileage is correct
            self.assertIn(row[0], expected.keys())
            self.assertEqual(expected[row[0]], row[1])

        conn.close()

    def test_vehicle_to_uppercase(self):
        vehicle = "red car"
        self.assertEqual("RED CAR", mileage.uppercase_vehicle(vehicle))


class TestSearchDB(TestCase):

    test_db_url = 'test_miles.db'

    # The name of this method is important - the test runner will look for it
    def setUp(self):
        # Overwrite the mileage
        mileage.db_url = self.test_db_url

        mileage.create_database()

        # drop everything from the DB to always start with an empty database
        conn = sqlite3.connect(self.test_db_url)
        conn.execute('DELETE FROM miles')
        conn.commit()
        conn.close()

        mileage.add_miles("blue car", 20)
        mileage.add_miles("red car", 30)

    def test_search_function(self):
        self.assertEqual(20, mileage.search("blue car"))

    def test_search_fail_function(self):
        self.assertEqual(None, mileage.search("green car"))

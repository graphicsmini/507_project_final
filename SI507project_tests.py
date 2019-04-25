from SI507project_tools import *
import unittest
import csv
import numpy as np
import random
import itertools


class TestOne(unittest.TestCase):
    def test_csv_file(self):
        self.csv_file = open('nps.csv','r')
        self.row_reader = self.csv_file.readlines()
        # print(self.row_reader) # For debug
        self.assertTrue(self.row_reader[1].split(",")[0], "Testing that there is a park name / first value in the row at index 1")
        self.assertTrue(self.row_reader[10].split(",")[0], "Testing that there is a park name / first value in the row at index 10")
        self.csv_file.close()

    def test_csv_file2(self):
        csv_file = open('nps.csv','r')
        self.contents = csv_file.readlines()
        csv_file.close()
        # print(self.contents)
        self.assertTrue('0,National Monument,Birmingham Civil Rights,AL,Alabama,"In 1963, images of snarling police dogs unleashed against non-violent protesters and of children being sprayed with high-pressure hoses appeared in print and television news across the world. These dramatic scenes from Birmingham, Alabama, of violent police aggression against civil rights protesters were vivid examples of segregation and racial injustice in America."\n')


class TestTwo(unittest.TestCase):
    def test_db_file(self):
        self.db_file = sqlite3.connect('nps.db').execute("select * from Park")
        rows = self.db_file.fetchall()
        park_num = len(rows)
        # print(rows)
        self.assertEqual(park_num, 654, "Testing the number of park listed in Park table.")

    def test_db_file_2(self):
        self.db_file = sqlite3.connect('nps.db').execute("select * from State")
        rows = self.db_file.fetchall()
        state_num = len(rows)
        # print(rows)
        self.assertEqual(state_num, 56, "Testing the number of state listed in State table.")

if __name__ == "__main__":
    unittest.main(verbosity=2)

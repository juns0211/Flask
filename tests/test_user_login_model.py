import unittest
from user.user_db import mysql_db as db

class user_testcase(unittest.TestCase):
    u = db(password = 'cat')
    def test_pw_setter(self):
        self.assertTrue(self.u.password_hash is not None)

    def test_no_pw_getter(self):
        with self.assertRaises(AttributeError):
            self.u.password
    
    def test_pw_verification(self):
        self.assertTrue(self.u.verify_password('cat'))
        self.assertFalse(self.u.verify_password('dog'))

    def test_pw_salts_are_random(self):
        u2 = db(password='cat')
        self.assertTrue(self.u.password_hash != u2.password_hash)

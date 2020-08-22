from test_plus.test import TestCase as PlusTestCase
from test_plus import APITestCase as APIPlusTestCase

class TestCase(PlusTestCase):
    """A base test case class"""

class APITestCase(APIPlusTestCase):
    """A base test case class"""

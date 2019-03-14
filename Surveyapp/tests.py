"""
test cases
"""
from django.urls import resolve
from django.test import TestCase
from .views import index


class HomePageTest(TestCase):
    """
    first test case
    """

    def setUp(self):
        pass

    def test_root_url_resolves_to_home_page_view(self):
        """
        test cases
        """
        found = resolve('/')
        self.assertEqual(found.func, index)

    def tearDown(self):
        pass

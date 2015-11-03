from django.contrib.auth import authenticate
from django.test import TestCase

from UserProfile.models import LQUser


class LQUserTests(TestCase):
    def test_authentication_of_user(self):
        """
        Tests to see if the authenticate works with JQUser objects
        """
        username = 'btboop'
        email = username + '@example.com'
        password = 'boop'

        user = LQUser.objects.create_user(username, email, password)
        test = authenticate(username=username, password=password)

        self.assertTrue(type(test) == LQUser)
        self.assertTrue(test.username == user.username)
        self.assertTrue(test.check_password(password))


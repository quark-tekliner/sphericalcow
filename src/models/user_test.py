from unittest import TestCase
from src.models.user import User


class UserTest(TestCase):

    def test_foo(self):
        user = User(uid='foo', pic='pic', name='bar', city='123')
        User.set_city_names((user, ))
        print user.city

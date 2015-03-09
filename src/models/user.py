from itertools import ifilter
from src.models import Model
from src.utils.vk import Vk


class User(Model):

    def __init__(self, uid=None, token=None, pic=None, name=None, city=None):
        self._uid = uid
        self._token = token
        self._is_admin = None
        self._pic = pic
        self._name = name
        self._city = None
        self._city_id = None
        self.city = city

    @property
    def uid(self):
        return self._uid

    @property
    def token(self):
        return self._token

    @property
    def pic(self):
        return self._pic

    @property
    def name(self):
        return self._name

    @property
    def city_id(self):
        return self._city_id

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, value):
        try:
            value = int(value)
        except ValueError:
            self._city = value
        else:
            self._city_id = value

    @property
    def is_admin(self):
        if self._uid is None:
            return False
        if self._is_admin is None:
            self._is_admin = self._db.sismember('admins', self._uid)
        return self._is_admin

    @classmethod
    def _get_key(cls, uid):
        return "user:%s" % (uid, )

    @property
    def key(self):
        return self._get_key(self._uid)

    @classmethod
    def from_session(cls, session):
        return cls(session.get('uid'), session.get('token'))

    def save(self):
        self._db.hmset(
            self.key, {
            'uid': self._uid,
            'token': self._token,
            'pic': self._pic,
            'name': self._name,
            'city': self._city,
        })

    def city_should_be_requested(self):
        return self._city is None and self._city_id is not None

    @classmethod
    def get_any_admin_token(cls):
        #todo: raise when token is None
        id = cls._db.srandmember('admins', 1)
        return cls._db.hget(cls._get_key(id[0]), 'token')

    @classmethod
    def get_by_id(cls, id):
        obj = cls._db.hgetall(cls._get_key(id))
        if len(obj) == 0:
            return None
        return cls(**obj)

    @classmethod
    def set_city_names(cls, users):
        user_by_city_id = {}
        for user in ifilter(lambda user: user.city_should_be_requested(), users):
            if user.city_id not in user_by_city_id:
                user_by_city_id[user.city_id] = []
            user_by_city_id[user.city_id].append(user)
        cities = Vk.call('database.getCitiesById', '', city_ids=','.join(user_by_city_id.keys()))
        for city in cities:
            for user in user_by_city_id[city.get('id')]:
                user.city = city.get('title')
                user.save()

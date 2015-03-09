import redis
from src.conf import Conf


class Db(object):
    _db = None

    @classmethod
    def get(cls):
        if cls._db is None:
            host = Conf.get('db_host', 'localhost')
            port = Conf.get('db_port', 6379)
            index = Conf.get('db_index', 0)
            cls._db = redis.StrictRedis(host=host, port=port, db=index)
        return cls._db

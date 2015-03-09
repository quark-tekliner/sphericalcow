from src.db import Db


class Model(object):
    _db = Db.get()
    #
    # def to_json(self):
    #     raise NotImplementedError()
    #
    # @classmethod
    # def from_json(cls, obj):
    #     return cls(**obj)

    # def save(self):
    #     key = self._get_db_key()
    #     obj = json.dumps(self.to_json())
    #     self.db.set(key, obj)
    #
    # @classmethod
    # def get_by_id(cls, id):
    #     key = cls.get_db_key(id)
    #     cls.from_json(cls._db.get(key))
    #
    # @classmethod
    # def get_all(cls):
    #     keys = list(cls._db.scan_iter("%s*" % cls._get_db_prefix()))
    #     items = cls._db.mget(sorted(keys, reverse=True))
    #     for item in items:
    #         yield cls.from_json(json.loads(item))

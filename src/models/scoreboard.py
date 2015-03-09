from src.models import Model


class Scoreboard(Model):

    CURRENT_SCOREBOARD = 'scoreboard:current_1'

    @classmethod
    def update_current_scoreboard(cls, uid, score):
        cls._db.zincrby(cls.CURRENT_SCOREBOARD, uid, score)

    @classmethod
    def get_current_scoreboard(cls):
        return cls._db.zrevrangebyscore(cls.CURRENT_SCOREBOARD, '+inf', 1, withscores=True)

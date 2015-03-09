from src.conf import Conf
from src.models import Model
import json
from src.utils.vk import Vk
from dateutil.parser import parse as parse_date


class Poll(Model):
    _owner_id = Conf.get("vk_owner")

    def __init__(self, id=None, date=None, post_id=None, answers=None, factor=1, correct_answer_id=None,
                 problem_is_incorrect_answer_id=None):
        self._id = id
        self._date = date
        self._post_id = post_id
        self._factor = factor
        self._answers = answers or {}
        self._correct_answer_id = correct_answer_id
        self._problem_is_incorrect_answer_id = problem_is_incorrect_answer_id

    @property
    def id(self):
        return self._id

    @property
    def date(self):
        return self._date

    @property
    def answers(self):
        return self._answers

    @property
    def factor(self):
        return self._factor

    @property
    def correct_answer_id(self):
        return self._correct_answer_id

    @property
    def problem_is_incorrect_answer_id(self):
        return self._problem_is_incorrect_answer_id

    @classmethod
    def _get_key(cls, id):
        return "poll:%s" % (id, )

    @property
    def key(self):
        return self._get_key(self._id)

    @property
    def score_delta(self):
        total = self.total_votes_count
        numerator = 1 - (self._answers[self._problem_is_incorrect_answer_id] / float(total))
        denumerator = self._answers[self._correct_answer_id] / float(total)
        return numerator/denumerator

    @property
    def total_votes_count(self):
        return sum(self._answers.values())

    def save(self):
        self._db.hmset(
            self.key, {
                'id': self._id,
                'date': self._date.isoformat(),
                'post_id': self._post_id,
                'factor': self._factor,
                'correct_answer_id': self._correct_answer_id,
                'problem_is_incorrect_answer_id': self._problem_is_incorrect_answer_id,
                'answers': json.dumps(self._answers),
            })

    def update_from_vk(self):
        for option in Vk.get_poll_answers(self._owner_id, self._post_id):
            self._answers[option.get('id')] = option.get('votes_count')

    @classmethod
    def get_by_id(cls, id):
        obj = cls._db.hgetall(cls._get_key(id))
        if len(obj) == 0:
            return None
        obj['factor'] = int(obj.get('factor'))
        obj['date'] = parse_date(obj.get('date'))
        obj['answers'] = json.loads(obj.get('answers'))
        return cls(**obj)

    def get_voters(self, token):
        answer_ids = ','.join((self._correct_answer_id, self._problem_is_incorrect_answer_id, ))
        fields = ','.join(('photo', 'city'))
        return Vk.call('polls.getVoters', token, owner_id=self._owner_id, poll_id=self._id, answer_ids=answer_ids,
                       fields=fields, count=1000, offset=0)

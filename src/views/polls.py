from datetime import datetime
from json import dumps
from bottle import request, abort
from src.conf import Conf
from src.models.poll import Poll
from src.utils.vk import Vk
from src.views import View


class Polls(View):
    _owner_id = Conf.get("vk_owner")
    _polls_cache = None
    _polls_as_dict = None

    @classmethod
    @View.admin_only
    def get_polls(cls, user):
        if cls._polls_cache is None:
            polls = []
            cls._polls_as_dict = {}
            for vk_poll in Vk.get_polls_from_wall(user.token, cls._owner_id):
                vk_poll['answers'] = list(vk_poll.get('answers'))
                id = vk_poll.get('id')
                poll = Poll.get_by_id(id)
                if poll is not None:
                    cls._update_vk_poll(vk_poll, poll)
                polls.append(vk_poll)
                cls._polls_as_dict[id] = vk_poll
            cls._polls_cache = dumps(polls)
        return cls._polls_cache

    @classmethod
    @View.admin_only
    def save_polls(cls, user, id):
        vk_poll = cls._polls_as_dict.get(id)
        if vk_poll is None:
            return abort(401, "Poll with id %s not presented." % (id, ))
        factor = request.json.get("factor")
        try:
            factor = int(factor)
        except ValueError:
            return abort(401, "Invalid factor value %s." % (factor, ))
        answers = {}
        for answer in vk_poll['answers']:
            answers[answer.get('id')] = answer.get('votes_count')
        correct_answer_id = request.json.get("correct_answer_id")
        problem_is_incorrect_answer_id = request.json.get("problem_is_incorrect_answer_id")
        if correct_answer_id not in answers:
            return abort(401, "Unknown id %s for correct answer." % (correct_answer_id, ))
        if problem_is_incorrect_answer_id not in answers:
            return abort(401, "Unknown id %s for problem is incorrect answer." % (problem_is_incorrect_answer_id, ))
        date = datetime.utcfromtimestamp(vk_poll.get('date'))
        post_id = vk_poll.get('post_id')
        poll = Poll(id=id, date=date, post_id=post_id, factor=factor, answers=answers,
                    correct_answer_id=correct_answer_id, problem_is_incorrect_answer_id=problem_is_incorrect_answer_id)
        poll.save()
        cls._update_vk_poll(vk_poll, poll)
        cls._update_polls_cache()
        return {}

    @classmethod
    def _update_vk_poll(cls, vk_poll, poll):
        vk_poll['factor'] = poll.factor
        vk_poll['correct_answer_id'] = poll.correct_answer_id
        vk_poll['problem_is_incorrect_answer_id'] = poll.problem_is_incorrect_answer_id

    @classmethod
    def _update_polls_cache(cls):
        cls._polls_cache = dumps(cls._polls_as_dict.values())

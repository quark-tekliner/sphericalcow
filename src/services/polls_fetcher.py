import sys


from src.models.poll import Poll
from src.models.user import User
from src.models.scoreboard import Scoreboard


class PollsFetcher(object):

    @classmethod
    def _get_active_poll(cls):
        return '171521116'

    @classmethod
    def _fetch_options(cls, poll_id):
        poll = Poll.get_by_id(poll_id)
        poll.update_from_vk()
        poll.save()
        token = User.get_any_admin_token()
        for result in poll.get_voters(token):
            if str(result.get('answer_id')) != poll.correct_answer_id:
                continue
            delta = poll.score_delta
            current_place_scores = int(round(delta * poll.factor))
            delta = int(round(delta))
            for vk_user in reversed(result.get('users', [])[1:]):
                uid = vk_user.get('uid')
                pic = vk_user.get('photo')
                name = "%s %s" % (vk_user.get('first_name', ''), vk_user.get('last_name', ''))
                city = vk_user.get('city')
                user = User(uid=uid, pic=pic, name=name, city=city)
                user.save()
                Scoreboard.update_current_scoreboard(uid, current_place_scores)
                current_place_scores -= delta
                if current_place_scores <= 0:
                    return


    @classmethod
    def run(cls):
        pass

    @classmethod
    def run_once(cls, poll_id):
        cls._fetch_options(poll_id)


if __name__ == '__main__':
    poll_id = sys.argv[1]
    PollsFetcher.run_once(poll_id)

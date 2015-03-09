import json
from bottle import response
from src.models.scoreboard import Scoreboard
from src.models.user import User
from src.views import View


class ScoreboardView(View):

    @classmethod
    @View.user_from_session
    def get_current_scoreboard(cls, current_user):
        return json.dumps(list(cls._get_current_scoreboard(current_user)))

    @classmethod
    @View.user_from_session
    def get_current_scoreboard_as_csv(cls, current_user):
        response.content_type = 'text/csv'
        lines = map(
            lambda item: ','.join((item['id'], item['name'], str(item['score']))),
            cls._get_current_scoreboard(current_user))
        return '\n'.join(lines)

    @classmethod
    def _get_current_scoreboard(cls, current_user):
        for user_id, score in Scoreboard.get_current_scoreboard():
            user = User.get_by_id(user_id)
            if user is None:
                continue
            yield {
                'id': user.uid,
                'name': user.name,
                'pic': user.pic,
                'city': user.city,
                'score': score,
                'is_current_user': user.uid == current_user.uid}
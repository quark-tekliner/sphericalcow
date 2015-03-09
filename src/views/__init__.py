from bottle import abort
from src.models.user import User


class ViewException(Exception):
    pass


class View(object):

    @staticmethod
    def user_from_session(func):
        def wrapper(cls, session, *args, **kwargs):
            user = User.from_session(session)
            return func(cls, user, *args, **kwargs)
        return wrapper

    @staticmethod
    def admin_only(func):
        def fake_func(cls, user, *args, **kwargs):
            if user.is_admin and user.token:
                return func(cls, user, *args, **kwargs)
            return abort(403, "Permission denied")
        return View.user_from_session(fake_func)

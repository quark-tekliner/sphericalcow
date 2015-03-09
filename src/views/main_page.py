from src.views import View


class MainPage(View):

    @classmethod
    @View.user_from_session
    def index(cls, user, jade):
        if user.is_admin:
            return jade.render('index_admin.jade')
        return jade.render('index_user.jade')

    @classmethod
    @View.user_from_session
    def sb(cls, user, jade):
        return jade.render('index_user.jade')

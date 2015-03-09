import requests
from bottle import redirect, request
from src.conf import Conf
from src.models.user import User
from src.utils.vk import Vk
from src.views import View


class Auth(View):

    _APP_ID = Conf.get("vk_app_id")
    _APP_SECRET = Conf.get("vk_app_secret")
    _CODE_URL = "https://oauth.vk.com/authorize?client_id=%s&scope=16,8192&redirect_uri=%s&response_type=code&v=5.26"
    _TOKEN_URL = "https://oauth.vk.com/access_token?client_id=%s&client_secret=%s&code=%s&redirect_uri=%s"

    @classmethod
    def login(cls):
        redirect(cls._CODE_URL % (cls._APP_ID, 'http://localhost:8080/code_callback', ))

    @classmethod
    def code_callback(cls, session):
        code = request.query.code
        url = cls._TOKEN_URL % (cls._APP_ID, cls._APP_SECRET, code, 'http://localhost:8080/code_callback', )
        token_res = requests.get(url)
        token = token_res.json().get('access_token')
        response = Vk.call('users.get', token)
        if len(response) == 0:
            redirect('/')
        uid = response[0].get('uid')
        if uid is None:
            redirect('/')
        User(uid, token).save()
        session['uid'] = uid
        session['token'] = token
        redirect('/')

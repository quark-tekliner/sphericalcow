import bottle_session
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '../'))

from bottle import run, Bottle, static_file
from bottle_jade import JadePlugin
from src.conf import Conf
from src.views.main_page import MainPage
from src.views.auth import Auth
from src.views.polls import Polls
from src.views.scoreboard import ScoreboardView

app = Bottle()

session_db_index = Conf.get('session_db_index', 0)
session_plugin = bottle_session.SessionPlugin(db=session_db_index, cookie_lifetime=6000)
app.install(session_plugin)
templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
jade_plugin = app.install(JadePlugin(template_folder=templates_dir))


@app.get('/')
def index(session):
    return MainPage.index(session, jade_plugin)

@app.get('/sb')
def index(session):
    return MainPage.sb(session, jade_plugin)


@app.get('/login')
def login():
    return Auth.login()


@app.get('/code_callback')
def code_callback(session):
    return Auth.code_callback(session)


@app.get('/polls')
def get_polls(session):
    return Polls.get_polls(session)

@app.post('/polls/<id:int>')
def get_polls(session, id):
    return Polls.save_polls(session, id)

@app.get('/scoreboard')
def get_current_scoreboard(session):
    return ScoreboardView.get_current_scoreboard(session)

@app.get('/scoreboard.csv')
def get_current_scoreboard_csv(session):
    return ScoreboardView.get_current_scoreboard_as_csv(session)


@app.get('/bower_components/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./web/bower_components')


@app.get('/s/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./web/static')


if __name__ == '__main__'
    port = Conf.get('port', 8080)
    debug = Conf.get('port', False)
    run(app=app, host='localhost', port=port, debug=debug)

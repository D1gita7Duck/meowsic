from flask import Flask, request
import remote.remote as remote
from app.music import *
import threading
import app.widgets as widgets
flask_app = Flask(__name__)

@flask_app.route('/control', methods=['POST'])
def control_music_player():
    action = request.form.get('action')
    if action == 'play_pause':
        play_pause(widgets.play_button)
    elif action == 'song_previous':
        song_previous()
    elif action == 'song_next':
        song_next()
    return "OK"


def run_flask():
    flask_app.run(host='0.0.0.0', port=5000)


def run_client_side():
    remote.app.run(host="0.0.0.0", port=80)

def start():
    """
    starts flask server side and client side
    """
    global flask_thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    client_side_thread = threading.Thread(target=run_client_side)
    client_side_thread.daemon = True
    client_side_thread.start()


def kill_app():
    "kills app and flask"
    func = flask_thread._stop
    try:
        func()
    except:
        print("closing flaskapp")

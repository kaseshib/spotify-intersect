from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import uuid
import os
import intersect

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path(user):
    return caches_folder + session.get(f'uuid_{user}')


def clear_caches():
    try:
        if session.get('uuid_1') and os.path.exists(session_cache_path(1)):
            os.remove(session_cache_path(1))
        if session.get('uuid_2') and os.path.exists(session_cache_path(2)):
            os.remove(session_cache_path(2))
        session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


@ app.route('/')
def index():

    clear_caches()
    session['uuid_1'] = str(uuid.uuid4())

    auth_manager_1 = spotipy.oauth2.SpotifyOAuth(
        scope='user-library-read playlist-modify-private', cache_path=session_cache_path(1), show_dialog=True)

    auth_url_1 = auth_manager_1.get_authorize_url()

    return render_template('signin.html', url=auth_url_1, first=True)


@ app.route('/callback/')
def callback():
    auth_manager_1 = spotipy.oauth2.SpotifyOAuth(
        scope='user-library-read playlist-modify-private', cache_path=session_cache_path(1), show_dialog=True)

    if not auth_manager_1.get_cached_token():
        auth_manager_1.get_access_token(request.args.get("code"))
        session['uuid_2'] = str(uuid.uuid4())

        auth_manager_2 = spotipy.oauth2.SpotifyOAuth(
            scope='user-library-read playlist-modify-private', cache_path=session_cache_path(2), show_dialog=True)
        auth_url_2 = auth_manager_2.get_authorize_url()

        return render_template('signin.html', url=auth_url_2, first=False)
    else:
        auth_manager_2 = spotipy.oauth2.SpotifyOAuth(
            scope='user-library-read playlist-modify-private', cache_path=session_cache_path(2), show_dialog=True)

        auth_manager_2.get_access_token(request.args.get("code"))
        return render_template('loading.html')


@ app.route('/playlist')
def playlist():
    if session.get('playlist'):
        both = session['playlist']
        return render_template('playlist.html', songs=both)

    if not session.get('uuid_1') or not session.get('uuid_2'):
        return render_template('error.html')

    auth1 = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(1))
    auth2 = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(2))

    user1 = spotipy.Spotify(auth_manager=auth1)
    user2 = spotipy.Spotify(auth_manager=auth2)

    both = intersect.setIntersect(user1, user2)
    session['playlist'] = both

    return render_template('playlist.html', songs=both)


@ app.route('/saveplaylist')
def savePlaylist():
    print("flask: saving playlist")
    if not session.get('uuid_1') or not session.get('uuid_2'):
        return render_template('error.html')

    auth1 = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(1))
    user1 = spotipy.Spotify(auth_manager=auth1)

    auth2 = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(2))
    user2 = spotipy.Spotify(auth_manager=auth2)

    if session.get('playlist'):
        both = session['playlist']
    else:
        return redirect(url_for('index'))

    intersect.savePlaylist(user1, user2, both)
    return("saved successfully")


if __name__ == "__main__":
    app.run(threaded=True, port=5000)

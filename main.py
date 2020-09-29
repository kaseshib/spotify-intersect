from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import uuid
import os
from pprint import pprint

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './.flask_session/'
Session(app)

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)


def session_cache_path(user):
    print(f"user {user} cache:", caches_folder + session.get(f'uuid_{user}'))

    return caches_folder + session.get(f'uuid_{user}')


# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     scope="user-library-read playlist-modify-private"))


@ app.route('/')
def index():
    print("---------- NEW REFRESH ----------")
    if not session.get('uuid_1'):  # or session.get('uuid_2'):
        # Step 1. There is no user 1, give random ID

        session['uuid_1'] = str(uuid.uuid4())
        # session['uuid_2'] = str(uuid.uuid4())
    if not session.get('uuid_2'):
        # There is no user 2, give random ID
        session['uuid_2'] = str(uuid.uuid4())

    auth_manager_1 = spotipy.oauth2.SpotifyOAuth(
        scope='user-library-read playlist-modify-private', cache_path=session_cache_path(1), show_dialog=True)

    auth_manager_2 = spotipy.oauth2.SpotifyOAuth(
        scope='user-library-read playlist-modify-private', cache_path=session_cache_path(2), show_dialog=True)

    if request.args.get("code"):
        # Step 3. Being redirected from Spotify auth page
        print('redirected here')
        if not auth_manager_1.get_cached_token():
            auth_manager_1.get_access_token(request.args.get("code"))
        else:
            auth_manager_2.get_access_token(request.args.get("code"))
        return redirect('/')

    auth_url_1 = auth_url_2 = spotify_1 = spotify_2 = None

    # print("auth_1 token:", auth_manager_1.get_cached_token())
    # if not auth_manager_1.get_cached_token():
    #     print("**** BOOOO ****")
    #     # Step 2. Display sign in link when no token
    #     auth_url_1 = auth_manager_1.get_authorize_url()
    #     # return f'<h2><a href="{auth_url_1}">Sign in</a></h2>'
    #     return render_template('index.html', user1=None, user2=None, auth_1=auth_url_1, auth_2=auth_url_2)

    # Step 2. Display sign in link when no token
    if not auth_manager_1.get_cached_token():
        auth_url_1 = auth_manager_1.get_authorize_url()
    else:
        spotify_1 = spotipy.Spotify(auth_manager=auth_manager_1)

    if not auth_manager_2.get_cached_token():
        auth_url_2 = auth_manager_2.get_authorize_url()
    else:
        spotify_2 = spotipy.Spotify(auth_manager=auth_manager_2)

    # if not auth_manager_2.get_cached_token():
    #     print("#### WOOHOO ####")
    #     # Step 2. Display sign in link when no token
    #     auth_url_2 = auth_manager_2.get_authorize_url()
    #     # return f'<h2><a href="{auth_url_2}">Sign in</a></h2>'
    #     return render_template('index.html', user1=spotify_1.me(), user2=None, auth_1=auth_url_1, auth_2=auth_url_2)

    # Step 4. Signed in, display data
    # spotify_1 = spotipy.Spotify(auth_manager=auth_manager_1)
    # spotify_2 = spotipy.Spotify(auth_manager=auth_manager_2)
    user1 = spotify_1.me() if spotify_1 else None
    user2 = spotify_2.me() if spotify_2 else None
    return render_template('index.html', user1=user1, user2=user2, auth_1=auth_url_1, auth_2=auth_url_2)
    # return render_template('index.html', user1=spotify_1.me(), user2=spotify_2.me(), auth_1=auth_url_1, auth_2=auth_url_2)


@app.route('/sign_out/<user>')
def sign_out(user):
    other_user = "1" if user == "2" else "2"
    try:
        # Remove the CACHE file (.cache-test) so that a new user can authorize.
        print("signing out...")
        os.remove(session_cache_path(user))
        if not os.path.exists(session_cache_path(other_user)):
            print('-- other user --', other_user)
            print('-- user -- ', user)
            session.clear()
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))
    return redirect('/')


@app.route('/playlists/<user>')
def playlists(user):
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(user))
    if not auth_manager.get_cached_token():
        return redirect('/')

    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user_playlists()


@app.route('/current_user/<user>')
def current_user(user):
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(user))
    if not auth_manager.get_cached_token():
        return redirect('/')
    spotify = spotipy.Spotify(auth_manager=auth_manager)
    return spotify.current_user()


if __name__ == "__main__":
    app.run(debug=True)

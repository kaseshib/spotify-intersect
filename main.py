from flask import Flask, render_template, request, session, redirect, url_for
from flask_session import Session
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import oauth2
import uuid
import os
from pprint import pprint
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


# spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     scope="user-library-read playlist-modify-private"))

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

    # return render_template('user1.html')

    print("---------- NEW REFRESH ----------")

    # implement
    ''' main:
    if no user 1:
        clear_caches()
        create_session_id(1)
    elif no user 2:
        create_session_id(2)
    else:
        display intersect playlist with option to save

    if redirected from auth page:
        get access token
        return same template

    display sign in link for correct user



'''
    #######################

    # if not session.get('uuid_1'):  # or session.get('uuid_2'):
    #     # Step 1. There is no user 1, give random ID
    #     # clear_caches()
    #     session['uuid_1'] = str(uuid.uuid4())
    # if not session.get('uuid_2'):
    #     session['uuid_2'] = str(uuid.uuid4())
    # # else:
    #     # return render_template('playlist.html')

    # auth_manager_1 = spotipy.oauth2.SpotifyOAuth(
    #     scope='user-library-read playlist-modify-private', cache_path=session_cache_path(1), show_dialog=True)

    # auth_manager_2 = spotipy.oauth2.SpotifyOAuth(
    #     scope='user-library-read playlist-modify-private', cache_path=session_cache_path(2), show_dialog=True)

    # if request.args.get("code"):
    #     # Step 3. Being redirected from Spotify auth page
    #     print('redirected here')
    #     if not auth_manager_1.get_cached_token():
    #         auth_manager_1.get_access_token(request.args.get("code"))
    #     else:
    #         auth_manager_2.get_access_token(request.args.get("code"))
    #         return redirect(url_for('playlist'))
    #     return redirect('/')

    # auth_url_1 = auth_url_2 = spotify_1 = spotify_2 = None

    # # Step 2. Display sign in link when no token
    # if not auth_manager_1.get_cached_token():
    #     auth_url_1 = auth_manager_1.get_authorize_url()
    # else:
    #     spotify_1 = spotipy.Spotify(auth_manager=auth_manager_1)

    # if not auth_manager_2.get_cached_token():
    #     auth_url_2 = auth_manager_2.get_authorize_url()
    # else:
    #     spotify_2 = spotipy.Spotify(auth_manager=auth_manager_2)

    # # if not auth_manager_2.get_cached_token():
    # #     print("#### WOOHOO ####")
    # #     # Step 2. Display sign in link when no token
    # #     auth_url_2 = auth_manager_2.get_authorize_url()
    # #     # return f'<h2><a href="{auth_url_2}">Sign in</a></h2>'
    # #     return render_template('index.html', user1=spotify_1.me(), user2=None, auth_1=auth_url_1, auth_2=auth_url_2)

    # # Step 4. Signed in, display data
    # user1 = spotify_1.me() if spotify_1 else None
    # user2 = spotify_2.me() if spotify_2 else None

    # # user = user1 if not user1 else user2
    # # url = auth_url_1 if user == user1 else auth_url_2
    # user = url = None
    # first = False

    # if not user1:
    #     user = user1
    #     first = True
    #     url = auth_url_1
    # elif not user2:
    #     user = user2
    #     first = False
    #     url = auth_url_2
    # else:
    #     return redirect(url_for('playlist'))

    #     both = intersect.setIntersect(spotify_1, spotify_2)
    #     return render_template('playlist.html', songs=both)

    # return render_template('signin.html', user=user, url=url, first=first)

    # return render_template('index.html', user1=user1, user2=user2,  auth_1=auth_url_1, auth_2=auth_url_2)
    # return render_template('index.html', user1=spotify_1.me(), user2=spotify_2.me(), auth_1=auth_url_1, auth_2=auth_url_2)

# @ app.route()


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
        # return redirect(url_for('playlist'))


@ app.route('/playlist')
def playlist():
    if session.get('playlist'):
        both = session['playlist']
        return render_template('playlist.html', songs=both)

    auth1 = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(1))
    auth2 = spotipy.oauth2.SpotifyOAuth(
        cache_path=session_cache_path(2))

    user1 = spotipy.Spotify(auth_manager=auth1)
    user2 = spotipy.Spotify(auth_manager=auth2)

    both = intersect.setIntersect(user1, user2)
    session['playlist'] = both
    # intersect.savePlaylist(user1, both)

    return render_template('playlist.html', songs=both)


@ app.route('/saveplaylist')
def savePlaylist():
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
    app.run(debug=True)

import spotipy
from spotipy.oauth2 import SpotifyOAuth

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="user-library-read playlist-modify-private"))


class Song():
    def __init__(self, song, artist, id):
        self.name = song
        self.artist = artist
        self.id = id

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


def allLiked(user):
    user_set = set()
    index_at = 0
    results = user.current_user_saved_tracks(limit=50, offset=index_at)

    while results['items']:
        for index, item in enumerate(results['items']):
            track = item['track']
            user_set.add(
                Song(track['name'], track['artists'][0]['name'], track['id']))
        index_at += 50
        results = user.current_user_saved_tracks(limit=50, offset=index_at)
    return user_set


def setIntersect(user1, user2):
    set1 = allLiked(user1)
    print('-- done with user1 --')
    set2 = allLiked(user2)
    print('-- done with user2 --')
    return set1.intersection(set2)


def savePlaylist(main_user, second_user, set):
    user_id = main_user.me()['id']

    main_name = main_user.me()['display_name']
    second_name = second_user.me()['display_name']
    title = f"Intersect: {main_name} x {second_name}"

    playlist = main_user.user_playlist_create(
        user=user_id, name=title, public=False)
    song_ids = [i.id for i in set]

    while len(song_ids) > 100:
        main_user.user_playlist_add_tracks(
            user_id, playlist['id'], song_ids[:100])
        song_ids[:] = song_ids[100:]

    main_user.user_playlist_add_tracks(user_id, playlist['id'], song_ids)
    print("*** successfully saved playlist ***")

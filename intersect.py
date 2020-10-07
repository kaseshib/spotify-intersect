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
        # print(index_at)
        results = user.current_user_saved_tracks(limit=50, offset=index_at)
    return user_set


def setIntersect(user1, user2):
    set1 = allLiked(user1)
    print('-- done with user1 --')
    set2 = allLiked(user2)
    print('-- done with user2 --')
    return set1.intersection(set2)


def savePlaylist(user, set):
    user_id = user.me()['id']
    playlist = user.user_playlist_create(
        user=user_id, name="Intersect!", public=False)
    song_ids = [i.id for i in set]

    while len(song_ids) > 100:
        user.user_playlist_add_tracks(user_id, playlist['id'], song_ids[:100])
        song_ids[:] = song_ids[100:]

    user.user_playlist_add_tracks(user_id, playlist['id'], song_ids)
    print("*** successfully saved playlist ***")

# index_at = 0
# user1_set = set()
# results = spotify.current_user_saved_tracks(limit=50, offset=index_at)

# # print(spotify.current_user_saved_tracks(limit=50, offset=900))

# while results['items']:
#     for index, item in enumerate(results['items']):
#         track = item['track']

#         user1_set.add(
#             Song(track['name'], track['artists'][0]['name'], track['id']))

#         print(index_at + index + 1, ' - ', track['name'], ' - ',
#               track['artists'][0]['name'], ' - ', track['id'])
#     index_at += 120
#     results = spotify.current_user_saved_tracks(limit=50, offset=index_at)

# user2_set = set()
# user2_set.add(Song('song name', 'artist!', "19Ov4l8mtvCT1iEUKks4aM"))
# user2_set.add(Song('Two-Headed Boy', "Neutral Milk Hotel", 'codesasdfjkl'))
# user2_set.add(Song('dreamer', 'sas', '2sNhYJ2ggd9BadlTXU3Mah'))

# both = user1_set.intersection(user2_set)

# user1 = spotify.me()['id']
# test_playlist = spotify.user_playlist_create(
#     user=user1, name="test", public=False)

# ids = [i.id for i in both]
# print(ids)
# spotify.user_playlist_add_tracks(user1, test_playlist['id'], ids)
# # print(test_playlist)

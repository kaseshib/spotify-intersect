# Spotify-Intersect

https://spotify-intersect.herokuapp.com/

<img src="https://github.com/kaseshib/spotify-intersect/blob/master/static/images/venn-01.png" width="300">

## About The Project

![Final Screen](https://github.com/kaseshib/spotify-intersect/blob/master/static/images/demo.png)

Spotify-Intersect creates a playlist of "liked" songs in common between two users on Spotify.


### Inspiration

Finding shared music in common with a friend is an awesome feeling, and one I hope I can aid by making this app.  Instead of trying to think of random artists that you think your friend *might* like, you can cut straight to the chase with Spotify-Intersect.

I'm far from the first to think of this idea, [as](https://community.spotify.com/t5/Closed-Ideas/Social-See-Music-in-common-with-Friends/idi-p/4372598) [you](https://community.spotify.com/t5/Closed-Ideas/Songs-you-have-in-common-with-other-users/idi-p/1526320) [can](https://community.spotify.com/t5/Closed-Ideas/Social-Compare-your-Music-Taste-with-Friends/idi-p/1512164) [see](https://community.spotify.com/t5/Closed-Ideas/All-Platforms-Discover-Find-music-in-common-with-friends/idi-p/1436611).


Due to the authorization procedure through Spotify, Spotify-Intersect is only viable if both people are on the same device.  In the future, adding capability for use across different devices/time would be especially valuable.  I would also like to add data visualization and make use of the rich audio analysis data available through the Spotify API. 


### Built With

 * [Flask (Python)](https://flask.palletsprojects.com/en/1.1.x/)
 * [Spotipy](https://spotipy.readthedocs.io/en/2.16.0/)
 * [Bootstrap](https://getbootstrap.com/)
 * [JQuery](https://jquery.com/)
 * HTML/CSS

## Setup

 * Install requirements
   * `pip install -r requirements.txt`
 * Add environment variables (receive credentials [here](https://developer.spotify.com/dashboard/))
   * `SPOTIPY_CLIENT_ID=""`
   * `SPOTIPY_CLIENT_SECRET= ""`
   * `SPOTIPY_REDIRECT_URI=""` (set the same value on Spotify dashboard too)
 * Run
   * `python app.py`

## Contact
Kasey Shibayama - kaseshib@gmail.com

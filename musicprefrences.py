import requests
import spotipy

class ProfileUser(object):

    def __init__(self, token_info=None):
    	self.token_info = token_info
        self.token = self.token_info['access_token']
        self.userid = None

    def start_stats(self):
        profile_info = self._get_profile()
        self.userid = self._get_userid(profile_info)
        self._get_playlists()

    def _get_profile(self):
        headers = {'Authorization': 'Bearer {0}'.format(self.token)}
        headers['Content-Type'] = 'application/json'
        resp = requests.get("https://api.spotify.com/v1/me", headers=headers)
        print(resp.json())
        return(resp.json())

    def _get_playlists(self):

        if(self.userid and self.token):
            sp = spotipy.Spotify(auth=self.token)   
            playlists = sp.user_playlists(self.userid)
            for playlist in playlists['items']:
                if playlist['owner']['id'] == self.userid:
                    print
                    print playlist['name']
                    print '  total tracks', playlist['tracks']['total']
                    results = sp.user_playlist(self.userid, playlist['id'],
                    fields="tracks,next")
                    tracks = results['tracks']
                    self._show_tracks(tracks)
                    while tracks['next']:
                        tracks = sp.next(tracks)
                        self._show_tracks(tracks)

    def _show_tracks(self, tracks):
        for i, item in enumerate(tracks['items']):
            track = item['track']
            print "   %d %32.32s %s" % (i, track['artists'][0]['name'],
                track['name'])

    def _get_userid(self,profile_info):
        return(profile_info['id'])
import os
import requests
import json
import spotipy
import spotipy.util as util
import oauth2
import musicprefrences


from flask import Flask, render_template, redirect, url_for,request, make_response

app=Flask(__name__)
# state_key = 'spotify_auth_state';
client_id = 'c785f3f71d114ddcadf61dc045d1c44b'
redirect_uri = 'http://localhost:5000/callback'
client_secret = '89ae1320fb26458b98c63a4efa804a8c'

global sp_oauth
sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri)

#   token_info = ''

@app.route("/")
def home():
    return(render_template('index.html'))


@app.route('/auth',methods = ['POST'])
def auth_req():
    if request.method == 'POST':
        result = request.form
        spotify_username  = result['Name']

        scope = 'user-top-read'
        sp_oauth = oauth2.SpotifyOAuth(client_id, client_secret, redirect_uri, scope=scope, cache_path=".cache-" + spotify_username )
        token_info = sp_oauth.get_cached_token()

        if not token_info:
            auth_url = sp_oauth.get_authorize_url()
            response = make_response(redirect(auth_url))
            return(response)
        
        music_pref = musicprefrences.ProfileUser(token_info)
        music_pref.start_stats()
    return redirect('/profile')


@app.route('/<path:path>')
def callback(path):
    code = sp_oauth.parse_response_code(request.url)
    token_info = sp_oauth.get_access_token(code)
    music_pref = musicprefrences.ProfileUser(token_info)
    music_pref.start_stats()
    return redirect('/profile')

@app.route('/profile')
def create_profile():
    return(render_template('profile.html'))


if __name__ == '__main__':
    app.run()

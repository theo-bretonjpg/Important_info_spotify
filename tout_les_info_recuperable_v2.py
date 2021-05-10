import sys
import spotipy    # la librairie pour manipuler l'api spotify
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import simplejson as json  #pour manipuler les réponses json 
import json
from CONFIG_SPOTIPY_AXEL import * #le fichier config
import pandas as pd

#recuperation de token.
token = util.prompt_for_user_token(username,scope='playlist-read-private playlist-read-collaborative playlist-modify-public playlist-modify-private',client_id=clientid,client_secret=clientsecret,redirect_uri='http://localhost/')


path= "C:/01__work/01__T2N-CORPORATION-JOB-ALTERNANCE/spotify_project/FICHIER_TEST_YELOTELO/tout_les_info_recuperable_v1/"

Spf_Artist= list()
Spf_Genre= list()
Spf_Album= list()
Spf_Track= list()
Spf_Type= list()

#Debut de la recherche.
if token:

    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    #le GET que on utilise pour recuperer les informations de l'artiste.
    #Pour faire fonctionner ce programme on a just besoins de l'URI de l'artiste.
    artist = sp.artist('spotify:artist:1RyvyyTE3xzB2ZywiAwp0i')
    #On recupere les informations de l'artiste.
    artist_name = artist['name']
    artist_uri = artist['uri']
    artist_genres = artist['genres']
    artist_popularity = artist['popularity']
    artist_followers = artist['followers']
    artist_type = artist['type']

    Spf_Artist.append((artist_name,artist_uri,artist_genres,artist_popularity,artist_followers,artist_type))
    Spf_Genre.append((artist_uri,artist_genres))

    #Le GET que on utilise pour recuperer tout les albums de l'artiste. 
    albums=sp.artist_albums(artist_uri, album_type=None, country=None, limit=20, offset=0)
    print(albums)
    #On recupere tout les URI de l'artiste.
    all_albums = albums['items']
    for i in all_albums :
        albums_uri = i['uri']
        #Le GET que on utilise pour recuperer tout les informations des albums de l'artiste.
        single_album=sp.album(albums_uri)

        for c in single_album['copyrights'] :
            album_copyrights = c['text']

        for a in single_album['artists'] :

            artist_name = a['name']
 
        album_name = single_album['name']
        album_uri = single_album['uri']
        number_tracks = single_album['total_tracks']
        release_date_album = single_album['release_date']
        album_type = single_album['type']

        Spf_Album.append((artist_name,album_name,album_uri,number_tracks,release_date_album,album_copyrights))
        Spf_Type.append((album_uri,album_type))
        
        #Le GET que on utilise pour recuperer tout les tracks et tout le informations sur les tracks de l'artiste.
        tracks_in_albums = sp.album_tracks(album_uri, limit=50, offset=0, market=None)
    
        for i in tracks_in_albums['items'] :
        #On recupere les informations des tracks.
            track_name = i['name']
            track_uri = i['uri']
            time = i['duration_ms']
            millis=(i['duration_ms'])
            millis = int(millis)
            seconds=(millis/1000)%60
            seconds = int(seconds)
            minutes=(millis/(1000*60))%60
            minutes = int(minutes)
            hours=(millis/(1000*60*60))%24
            time =  minutes , seconds
            track_duration = str(time)
            
            Spf_Track.append((track_name,track_uri,track_duration,album_uri))


#Creation des DataFrame et des fichier .csv
spf_artist1 = pd.DataFrame(Spf_Artist, columns=["ARTIST_NAME","ARTIST_URI","ARTIST_GENRE","ARTIST_POPULARITY","ARTIST_FOLLOWERS","ARTIST_TYPE"])
spf_artist1.to_csv(path+"Spf_Artist.csv",mode='a',index=False,encoding="utf-8")

spf_genre1 = pd.DataFrame(Spf_Genre, columns=["ARTIST_URI","ARTIST_GENRES"])
spf_genre1.to_csv(path+"spf_Genre.csv",mode='a',index=False,encoding="utf-8")

spf_Album1 = pd.DataFrame(Spf_Album, columns=["ARTIST_NAME","ARLBUM_NAME","ALBUM_URI","ALBUM_NUMBER_TRACKS","ALBUM_RELEASE_DATE","ALBUM_COPYRIGHTS"])
spf_Album1.to_csv(path+"Spf_Album.csv",mode='a',index=False,encoding="utf-8")

Spf_Type1 = pd.DataFrame(Spf_Type, columns=["ALBUM_URI","ALBUM_TYPE",])
Spf_Type1.to_csv(path+"Spf_Type.csv",mode='a',index=False,encoding="utf-8")

spf_track1 = pd.DataFrame(Spf_Track, columns=["TRACK_NAME","TRACK_URI","TRACK_DURATION","ALBUM_URI"])
spf_track1.to_csv(path+"Spf_Track.csv",mode='a',index=False,encoding="utf-8")
                                            

'''
Pour artist :

artist_name
artist_uri 
artist_genres 
artist_popularity  
artist_followers
artist_type
'''

#tableau_csv_info_Artist.append((artist_name,artist_uri,artist_popularity,artist_followers,artist_type))


'''
Pour genre :

artiste_uri
artiste_genres
'''

#tableau_csv_info_Genre= list(artist_uri,artist_genres)

'''
Pour album :

artist_name 
album_name
album_uri
number_tracks
release_date_album
album_type
album_copyrights
'''

#tableau_csv_info_album.append(artist_name,album_name,album_uri,number_tracks,release_date_album,album_type,album_copyrights)

'''
Pour track :

track_name
track_uri
track_duration
track_upc
'''

#tableau_csv_info_track.append(track_name,track_uri,track_duration,album_uri)

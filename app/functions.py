import os
import time
from datetime import datetime
import pickle
from youtubesearchpython import VideosSearch
import yt_dlp as youtube_dl
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tinytag import TinyTag
import app.db as db

#load api keys
with open("data/secrets.dat","rb") as credentials:
    temp_cred=pickle.load(credentials)
    client_credentials_manager = SpotifyClientCredentials(client_id=temp_cred[0], client_secret=temp_cred[1])
    sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
 
#check if settings file exists else create a new one
if os.path.exists("data/settings.dat"):
    with open("data/settings.dat","rb") as settings:
        temp_sett=pickle.load(settings)
        current_theme=temp_sett[0]
        transparency=temp_sett[1]
else:
    with open("data/settings.dat","wb") as settings:
        current_theme="dark"
        transparency=0.88
        pickle.dump([current_theme,transparency],settings)
if not(os.path.exists("Audio/")) and not(os.path.exists("thumbs/")):
    os.system("mkdir Audio")
    os.system("mkdir thumbs")

#ytdlp args
ydl_opts = {
    'outtmpl': "new",
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

db.init() #initialize DB

def change_mode(mode):
    print("changing mode to",mode)
    with open("data/settings.dat","rb") as f:
        temp_list=pickle.load(f)
        temp_list[0]=mode
    print(temp_list)
    with open("data/settings.dat","wb") as f:
        pickle.dump(temp_list,f)


def change_transparency(alpha):
    print("setting trans to",alpha)
    with open("data/settings.dat","rb") as f:
        temp_list=pickle.load(f)
    with open("data/settings.dat","wb") as f:
        temp_list[-1]=alpha
        pickle.dump(temp_list,f)

def check_recents():
    try:
        file=open("data/recents.dat","rb+")
    except FileNotFoundError:
        file=open("data/recents.dat","wb+")
        pickle.dump([{},{},{}],file)
    finally:
        file.close()

check_recents()

def store_recents(song):
    """
    store recently played songs to recents.dat
    """
    if ".mp3" in song:
        print("local song not adding to recents")
    else:
        file=open("data/recents.dat","rb+")
        file.seek(0,0)
        L=pickle.load(file)
        L.pop()
        L.insert(0,song)
        file.seek(0,0)
        pickle.dump(L,file)
        file.close()

def get_recents():
    """
    retrives recently played songs from recents.dat
    """
    file=open("data/recents.dat","rb")
    file.seek(0,0)
    recent=pickle.load(file)
    while {} in recent:
        recent.remove({})
    return list(set(recent)) #remove repeated songs

def like_song(song):
    res=db.song_search(song)
    path=os.path.join("Audio/",better_name(res["path"])+".mp3")
    db.like_song([path,res["url"],res["duration"],res["pretty_name"],res["thumbnail"],res["artists"]])

def dislike_song(song):
    db.dislike_song(song)

def if_liked(song):
    L=db.get_liked_songs()
    print("L",L)
    for i in L:
        if i["pretty_name"]==song:
            print(song,i["pretty_name"])
            return True
    return False

def get_liked_songs():
    return db.get_liked_songs()

def thumbs(name,url):
    """
    Accepts name and url of a song to store and download the thumbnail.
    Checks if file already exists and skips if yes
    """
    try:
        file=open(os.path.join("thumbs/",f"{name}.png"),"rb+")
    except FileNotFoundError:
        with open(os.path.join("thumbs/",f"{name}.png"),"wb") as file:
            res=requests.get(url,timeout=5).content
            file.write(res)
    else:
        file.close()
        print("thumb already cached. Skipping")
    finally:
        return "thumbs/"+f"{name}.png"


def better_name(stringy):
    """Remove spaces and other special characters from the string
    """
    new_stringy = ''.join(char for char in stringy if char.isalnum() or char in ['_', '-', '.'])
    new_stringy = new_stringy.casefold()
    return new_stringy

def search_results(stringy):
    """
    Accepts keyword and returns list of song names that are close to the keyword
    """
    details=sp.search(q=stringy,limit=5,type="track")
    results=[]
    list=details["tracks"]["items"]
    for song in list:
        temp_artists=song["artists"]
        artists=""
        for i in temp_artists:
            artists+=i["name"]+", "
        artists=artists.rstrip(", ").split(",")[0]      
        if (song["name"],artists) not in results:
            results.append((song["name"],artists))
    return results

def search(stringy):
    """
    Accepts song name and uses youtube and spotify API to get metadata.
    Returns a dictionary of url, duration, prettyname and thumbnail url.
    """
    details=sp.search(q=stringy,limit=1,type="track")
    duration=details["tracks"]["items"][0]["duration_ms"]//1000 #returns in ms
    pretty_name=details["tracks"]["items"][0]["name"]
    thumbnail_url=details["tracks"]["items"][0]["album"]["images"][0]["url"]
    temp_artists=details["tracks"]["items"][0]["artists"]
    artists=""
    for i in temp_artists:
        artists+=i["name"]+", "
    artists=artists.rstrip(", ")
    videos_search = VideosSearch(pretty_name+" by "+artists.split(",")[0], limit = 1)
    videos=videos_search.result()
    url="https://www.youtube.com/watch?v="+videos["result"][0]["id"]
    db_search=db.song_search(pretty_name)
    if db_search:
        print("found in db")
        thumbnail_path=thumbs(better_name(pretty_name),thumbnail_url)
    else:
        print("not found in db downloading thumb")
        thumbnail_path=thumbs(better_name(pretty_name),thumbnail_url)
        db.song_insert(["Audio/"+better_name(pretty_name)+".mp3",url,duration,pretty_name,thumbnail_path,artists])
        print("added record to db")
    
    return {"path":"Audio/"+better_name(pretty_name)+".mp3","url":url,"duration":duration,"pretty_name":pretty_name,"thumbnail_path":thumbnail_path,"artists":artists}

def artist_search(pretty_name):
    """
    local db search for song metadata
    """
    search_res=db.song_search(pretty_name)
    if search_res:
        return search_res
    else:
        return search(pretty_name)

def add_playlist(header_dict):
    if len(header_dict)==1:
        db.insert_playlist_header([header_dict["name"],"Null","Null"])
    else:
        db.insert_playlist_header([x for x in header_dict.values()])

def get_playlists():
    """
    return list of all playlists
    """
    return db.get_all_playlists()

def get_playlist_details(name):
    """
    get details of the given playlist
    """
    print(db.get_playlist_header(name))
    L=[]
    for i in db.get_playlist_header(name):
        for x in i.values():
            L.append(x)
    print(L)
    return L

def add_to_playlist(song_name,playlist_name):
    """
    adds the given song to the given playlist
    """
    print("adding",song_name,"to",playlist_name)
    db.insert_playlist_details([playlist_name,song_name,datetime.today().strftime('%Y-%m-%d')])
    print("after",[playlist_name,song_name,datetime.today().strftime('%Y-%m-%d')])

def delete_playlist(playlist_name):
    db.delete_playlist((playlist_name,))
    
def get_playlist_songs(name):
    """
    returns list of songs in a playlist.
    accepts name as argument
    """
    names=[]
    L=db.get_playlist_detail(name)
    for song in L:
        names.append(song["pretty_name"])
    print(names)
    return names

def store_local(name):
    """
    stores local song metadata in db
    """
    duration=int(TinyTag.get("Audio/"+name).duration)
    db.song_insert([name,"None",duration,name,"None","Miscellaneous"])

def get_recommmended_playlist():
    ''' list of dictionaries of key value pairs where key is playlist name and value is a list of song names'''

    featured_playlists = sp.featured_playlists(limit=10,offset=5)
    recommended_playlist={}
    for playlist in featured_playlists['playlists']['items']:
        playlist_name=playlist["name"]
        songs = sp.playlist_tracks(playlist['id'], limit=15)
        song_names = [song['track']['name'] for song in songs["items"]]
        recommended_playlist[playlist_name] = song_names
    print(recommended_playlist,len(recommended_playlist))
    return recommended_playlist

def download(url,name):
    """
    Function to download song and convert it to mp3.
    Accepts url, Actual song name (pretty_name) and filename
    """
    name=name+r".mp3"
    if os.path.isfile(os.path.join("Audio/",name)):
        print("song already cached skipping")
    else:
        #print(os.path.isfile(os.path.join("Audio/",name)))       
        while True:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    # ydl_down = threading.Thread(target=ydl.download, args=[url])
                    # ydl_down.start()

                    ydl.download([url])
                    try:
                        os.rename("new.mp3", os.path.join(r"Audio/",name))
                        break  # Break out of the loop if the file is successfully renamed
                    except FileNotFoundError:
                        print("File not found. Retrying in 1 second...")
                        time.sleep(1)
                    except FileExistsError:
                        print("Already cached")
                        try:
                            os.remove("new.mp3")
                        except IOError:
                            print("This shouldn't happen")
                        break      
    return name
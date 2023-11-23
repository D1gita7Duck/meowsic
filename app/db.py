import sqlite3
import os
#con=sqlite3.connect("d:\songs2.db", isolation_level=None)

con=sqlite3.connect("data/database.db",check_same_thread=False)

def init():
   global cur
   cur=con.cursor()
   res = cur.execute("SELECT name FROM sqlite_master where name = 'songs'")

   if (res.fetchone() is None):
      print("creating new songs table")
      con.execute("Create table songs(path varchar(50),url varchar(100),duration int,pretty_name varchar(30),thumbnail varchar(50),artists varchar(20))")

   if not(cur.execute("SELECT name FROM sqlite_master where name = 'liked_songs'").fetchone()):
      print("creating new liked_songs table")
      con.execute("Create table liked_songs(path varchar(50),url varchar(100),duration int,pretty_name varchar(30),thumbnail varchar(50),artists varchar(20))")
   if not(cur.execute("SELECT name FROM sqlite_master where name = 'playlist_header'").fetchone()):
      print("creating playlist_header")
      con.execute("Create table playlist_header (playlist_name varchar(100), playlist_art_location varchar(100), date_of_creation date)")
   if not(cur.execute("SELECT name FROM sqlite_master where name = 'playlist_details'").fetchone()):
      print("creating playlist_details")
      con.execute("Create table playlist_details (playlist_name varchar(100),song_name varchar(100),date_of_addition date)")
def song_insert(song_list):
   # res = cur.execute("SELECT name FROM sqlite_master where name = 'songs'")
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO songs(path,url,duration,pretty_name,thumbnail,artists) VALUES (:path, :url, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   con.execute("COMMIT")
   print("add operation done")

def insert_playlist_header(playlist_header_list):
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO playlist_header(playlist_name, playlist_art_location , date_of_creation) VALUES (:playlistname, :playlist_art_location, :date_of_creation)",playlist_header_list)
   con.execute("COMMIT")
   print("add operation done",playlist_header_list)
def insert_playlist_details(playlist_details_list):
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO playlist_details(playlist_name,song_name,date_of_addition ) VALUES (:playlist_name,:song_name,:date_of_addition)",playlist_details_list)
   con.execute("COMMIT")
   print("add operation done",playlist_details_list)


def like_song(song_list):
   print("liking ",song_list)
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO liked_songs(path,url,duration,pretty_name,thumbnail,artists) VALUES (:path, :url, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   con.execute("COMMIT")
   print("like operation done")
def dislike_song(song_list):
   print("disliking ",song_list)
   con.execute("BEGIN TRANSACTION")
   con.execute("delete from liked_songs where pretty_name like '{}'".format(song_list))
   print("delete from liked_songs where pretty_name like '{}'".format(song_list))
   con.execute("COMMIT")
   print("dislike operation done")


   
def get_liked_songs():
   print("getting liked songs")
   res=cur.execute("select * from liked_songs")
   liked_list=res.fetchall()
   desc=cur.description
   column_names=[col[0] for col in desc]
   liked_dict=[dict(zip(column_names,row))for row in liked_list]
   print("liked dict",liked_dict)
   return liked_dict

def song_search(song):
   print("searching")
   res1 = cur.execute("SELECT * FROM songs where pretty_name = :song",[song])
   desc=cur.description
   column_names=[col[0] for col in desc]
   check=cur.fetchall()
   print("check",check)
   if check==[]:
      print("not found")
      return False
   else:
      data=[dict(zip(column_names, row)) for row in check]
      print(data[0])
      return data[0]

def get_playlist_detail(playlist_name_in):
   con=sqlite3.connect(os.getcwd()+"/data/database.db",check_same_thread=False)
   cur=con.cursor()
   res=cur.execute("select pretty_name , duration, artists , date_of_addition from songs, playlist_details where songs.pretty_name= playlist_details.song_name and playlist_details.playlist_name=(?)", (playlist_name_in,))
   playlist_details_list=res.fetchall()
   desc=cur.description
   column_names=[col[0] for col in desc]
   playlist_details_dict=[dict(zip(column_names,row))for row in playlist_details_list]
   print("Play list details dict",playlist_details_dict)
   return playlist_details_dict


def get_all_playlists():
   con=sqlite3.connect(os.getcwd()+"/data/database.db",check_same_thread=False)
   cur=con.cursor()
   res=cur.execute("select playlist_name from playlist_header")
   list_playlists=res.fetchall()
   return list_playlists

# def get_playlist_header(playlist_name):
#     con = sqlite3.connect(os.getcwd() + "/data/database.db", check_same_thread=False)
#     cur = con.cursor()
#     res = cur.execute("""
#     SELECT playlist_header.playlist_name, playlist_header.date_of_creation,
#            COUNT(songs.path) AS number_of_songs, SUM(songs.duration) AS duration
#     FROM playlist_header, playlist_details, songs
#     WHERE playlist_header.playlist_name = playlist_details.playlist_name
#       AND playlist_header.playlist_name = ?
#       AND playlist_details.song_name = songs.pretty_name;
# """, (playlist_name))
#     playlist_details_list = []

#     if res is not None:
#         playlist_details_list = res.fetchall()
#         print(playlist_details_list)
#         desc = cur.description
#         column_names = [col[0] for col in desc]
#         playlist_details_dict = [dict(zip(column_names, row)) for row in playlist_details_list]

#     con.close()
#     return playlist_details_dict
def get_playlist_header(playlist_name_in):
   con=sqlite3.connect(os.getcwd()+"/data/database.db",check_same_thread=False)
   cur=con.cursor()
   #Check if  songs exists with songs
   res=cur.execute("select d.playlist_name, d.song_name from playlist_details d join songs s where d.playlist_name=(?) and d.song_name= s.pretty_name;", (playlist_name_in))
   songs_list=res.fetchall()
   #If songs are not available
   if (len(songs_list)==0):
      res=cur.execute("select h.playlist_name, h.date_of_creation ,  0 as number_of_songs, 0 as duration from playlist_header h where h.playlist_name=(?);", (playlist_name_in))
      playlist_header_list=res.fetchall()
      if (len(playlist_header_list) == 0):
         playlist_header_list=[]
   else: #Songs are available
      res=cur.execute("select h.playlist_name, h.date_of_creation ,  count(*) as number_of_songs, sum(duration) as duration from playlist_header h join playlist_details d join songs s where h.playlist_name=d.playlist_name and h.playlist_name=(?) and d.song_name= s.pretty_name;", (playlist_name_in))
      playlist_header_list=res.fetchall()
      if (playlist_header_list[0][0] is None):
         playlist_header_list=[]
   #Add to Dictionary      
   if (len(playlist_header_list)): #If Playlist is available
      print(playlist_header_list)
      desc=cur.description
      column_names=[col[0] for col in desc]
      playlist_header_dict=[dict(zip(column_names,row))for row in playlist_header_list]
   else:
      print("playlist not available")
      playlist_header_dict={}
   return playlist_header_dict


#print("AAAAA",get_playlist_header("test1"))
def delete_playlist(playlist_name):
   con=sqlite3.connect(os.getcwd()+"/data/database.db",check_same_thread=False)
   cur=con.cursor()
   con.execute("BEGIN TRANSACTION")

   cur.execute("DELETE from playlist_details where playlist_name=(?)", (playlist_name,))
   cur.execute("DELETE from playlist_header where playlist_name=(?)", (playlist_name,))
   con.execute("COMMIT")

def delete_song_from_playlist(song_name, playlist_name):
   con=sqlite3.connect(os.getcwd()+"/data/database.db",check_same_thread=False)
   cur=con.cursor()
   cur.execute("DELETE from playlist_details where song_name=(?) and playlist_name=(?)", (song_name, playlist_name))
def close():
   cur.close()
   con.close()


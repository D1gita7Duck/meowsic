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
   con.execute("INSERT INTO playlist_header(playlistname, playlist_art_location , date_of_creation) VALUES (:playlistname, :playlist_art_location, :date_of_creation)",playlist_header_list)
   con.execute("COMMIT")
   print("add operation done")
def insert_playlist_details(playlist_details_list):
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO playlist_details(playlist_name,song_name,date_of_addition ) VALUES (:playlist_name,:song_name,:date_of_addition)",playlist_details_list)
   con.execute("COMMIT")
   print("add operation done")


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
   res=cur.execute("select path , duration, artists , date_of_addition from songs, playlist_details where songs.path= playlist_details.song_name and playlist_details.playlist_name=(?)", (playlist_name_in,))
   playlist_details_list=res.fetchall()
   desc=cur.description
   column_names=[col[0] for col in desc]
   playlist_details_dict=[dict(zip(column_names,row))for row in playlist_details_list]
   print("Play list details dict",playlist_details_dict)
   return playlist_details_dict



def get_playlist_header(playlist_name_in):
   con=sqlite3.connect(os.getcwd()+"/data/database.db",check_same_thread=False)
   cur=con.cursor() 
   res=cur.execute("select h.playlist_name, h.date_of_creation ,  count(*) as number_of_songs, sum(duration) as duration from playlist_header h join playlist_details d join songs s where h.playlist_name=d.playlist_name and h.playlist_name=(?) and d.song_name= s.path;", (playlist_name_in, ))
   playlist_header_list=res.fetchall()
   desc=cur.description
   column_names=[col[0] for col in desc]
   playlist_header_dict=[dict(zip(column_names,row))for row in playlist_header_list]
   return playlist_header_dict

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


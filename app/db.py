import sqlite3
import os
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

# Function to search a song and store it in the database
def song_insert(song_list):
   try:
      con.execute("BEGIN TRANSACTION")
      con.execute("INSERT INTO songs\
         (path,url,duration,pretty_name,thumbnail,artists) \
         VALUES \
         (:path, :url, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   except Exception as e:
      print("Unable to insert the song.\
            Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("add operation done")

# Function to insert into playlist_header
def insert_playlist_header(playlist_header_list):
   try:
      con.execute("BEGIN TRANSACTION")
      con.execute("INSERT INTO playlist_header\
         (playlist_name, playlist_art_location , date_of_creation) VALUES \
      (:playlistname, :playlist_art_location, :date_of_creation)",playlist_header_list)
   except Exception as e:
      print("Unable to insert into the playlist.\
            Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("add operation done",playlist_header_list)
#Function to insert into playlist_details
def insert_playlist_details(playlist_details_list):
   try:
      con.execute("BEGIN TRANSACTION")
      con.execute("INSERT INTO playlist_details\
         (playlist_name,song_name,date_of_addition ) VALUES \
         (:playlist_name,:song_name,:date_of_addition)",playlist_details_list)
   except Exception as e:
      print("Unable to insert into playlist-details\
         Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("add operation done",playlist_details_list)

# Function to like a song
def like_song(song_list):
   try:
      con.execute("BEGIN TRANSACTION")
      con.execute("INSERT INTO liked_songs\
         (path,url,duration,pretty_name,thumbnail,artists) VALUES \
         (:path, :url, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   except Exception as e:
      print("Unable to add to liked songs\
      Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("like operation done")

#  Function to delete a liked  song 
def dislike_song(song_list):
   try:
      con.execute("BEGIN TRANSACTION")
      con.execute("delete from liked_songs \
         where pretty_name like '{}'".format(song_list))
      print("delete from liked_songs where pretty_name like '{}'".format(song_list))
   except Exception as e:
      print("Unable to delete from liked songs\
            Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("dislike operation done")


# Function to get liked  songs 
def get_liked_songs():
   try:
      res=cur.execute("select * from liked_songs")
      liked_list=res.fetchall()
      desc=cur.description
      column_names=[col[0] for col in desc]
      liked_dict=[dict(zip(column_names,row))for row in liked_list]
   except Exception as e:
      print("Unable to fetch liked songs\
            Error: ", str(e))
      liked_dict={}
   print("liked dict",liked_dict)
   return liked_dict

# Function to search a song 
def song_search(song):
   print("searching")
   try:
      res1 = cur.execute("SELECT * FROM songs where pretty_name = :song",[song])
      check=cur.fetchall()
      print("check",check)
      if check==[]:
         print("not found")
         return False
      else:
         desc=cur.description
         column_names=[col[0] for col in desc]
         data=[dict(zip(column_names, row)) for row in check]
         print(data[0])
         return data[0]
   except Exception as e:
      print("Unable to search song\
            Error Message: ", str(e))
   return False

# Function to get all songs for a playlist
def get_playlist_detail(playlist_name_in):
   try:
      res=cur.execute("select pretty_name , duration, artists , date_of_addition from songs, playlist_details where songs.pretty_name= playlist_details.song_name and playlist_details.playlist_name=(?)", (playlist_name_in,))
      playlist_details_list=res.fetchall()
      desc=cur.description
      column_names=[col[0] for col in desc]
      playlist_details_dict=[dict(zip(column_names,row))for row in playlist_details_list]
      print("Play list details dict",playlist_details_dict)
   except Exception as e:
      print("Unable to fetch songs for a playlists\
            Error Message: ", str(e))
      playlist_details_dict={}
   return playlist_details_dict

# Function to fetch all playlists
def get_all_playlists():
   try:
      res=cur.execute("select playlist_name from playlist_header")
      list_playlists=res.fetchall()
   except Exception as e:
      print("Unable to fetch all playlists\
            Error Message: ", str(e))
      list_playlists=[]
   return list_playlists

# Function to fetch playlist summary information
def get_playlist_header(playlist_name_in):
   try:
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
   except Exception as e:
      print("Unable to fetch playlist summary information\
            Error Message: ", str(e))
      playlist_header_dict={}

   return playlist_header_dict

# Function to Delete a playlist
def delete_playlist(playlist_name):
   try:
      con.execute("BEGIN TRANSACTION")
      cur.execute("DELETE from playlist_details where playlist_name=(?)", (playlist_name))
      cur.execute("DELETE from playlist_header where playlist_name=(?)", (playlist_name))
   except Exception as e:
      print("Unable to delete the playlist\
            Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("Deleted playlist")

# Function to Delete a song from a playlist
def delete_song_from_playlist(song_name, playlist_name):
   try:
      con.execute("BEGIN TRANSACTION")
      cur.execute("DELETE from playlist_details where song_name=(?) and playlist_name=(?)", (song_name, playlist_name))
   except Exception as e:
      print("Unable to delete from playlist\
            Error Message: ", str(e))
      con.execute("ROLLBACK;")
   else:
      con.execute("COMMIT")
      print("Deleted from the playlist")

# Function to close cursor, connection
def close():
   cur.close()
   con.close()

#init()
#song_search("XX")
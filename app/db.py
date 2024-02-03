import sqlite3
import os

def create_table(table_name_in, create_table_statement):
   try:
      # Check if table exists 
      print (table_name_in)
      res = cur.execute("SELECT name FROM sqlite_master \
              where name = (?)",(table_name_in, ))
      # creates a table if the table does not exist.
      if (res.fetchone() is None):
         print("creating new table: ", table_name_in)
         con.execute(create_table_statement)
   except Exception as e:
      print("Database error:", str(e))
   
def create_all_tables():
   """
   wrapper fn to call all necessary functions
   """
   create_song_table()
   create_liked_song_table()
   create_playlist_header_table()
   create_playlist_details_table()

def create_song_table():
   """
   call the create table with name of the table and the sql statement
   """
   create_stmt = "Create table songs\
         (path varchar(100) not null primary key,\
         url varchar(500) not null,\
         duration int not null,\
         pretty_name varchar(100) not null ,\
         thumbnail varchar(100),\
         artists varchar(500))"
   create_table("songs", create_stmt)
   
def create_liked_song_table():
   """
   call the create table with name of the table and the sql statement
   """
   create_stmt="Create table liked_songs\
      (path varchar(100) not null primary key,\
      url varchar(500) not null,\
      duration int not null,\
      pretty_name varchar(100) not null,\
      thumbnail varchar(100),\
      artists varchar(500))"
   create_table("liked_songs", create_stmt)
   

def create_playlist_header_table():
   """
   call the create table fn with name of the header table
   """
   create_stmt="Create table playlist_header\
      (playlist_name varchar(100) not null primary key,\
       playlist_art_location varchar(100) not null,\
       date_of_creation date not null)" 
   create_table("playlist_header", create_stmt)

def create_playlist_details_table():
   """
   call the create table fn with name of the details table
   """
   create_stmt="Create table playlist_details \
      (playlist_name varchar(100) not null,\
      song_name varchar(100) not null,\
      date_of_addition date not null)  "
   create_table("playlist_details", create_stmt)

def init():
   """
   initialises the db if it exists.
   creates db if it doesnt exist and creates all necessary tables.
   """
   global cur
   global con
   con=sqlite3.connect("data/database.db",check_same_thread=False)
   cur=con.cursor()
   create_all_tables()


def song_insert(song_list):
   """
   Function to search a song and store it in the database
   """
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

def insert_playlist_header(playlist_header_list):
   """
   # Function to insert into playlist_header table
   """
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


def insert_playlist_details(playlist_details_list):
   """
   Function to insert into playlist_details table
   """
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


def like_song(song_list):
   """
   Function to like a song given details
   """
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


def dislike_song(song_list):
   """
   Function to delete a liked song 
   """
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



def get_liked_songs():
   """
   # Function to get liked songs 
   """
   try:
      res=cur.execute("select * from liked_songs")
      liked_list=res.fetchall()
      desc=cur.description
      print (cur.description)
      column_names=[col[0] for col in desc]
      liked_dict=[dict(zip(column_names,row))for row in liked_list]
   except Exception as e:
      print("Unable to fetch liked songs\
            Error: ", str(e))
      liked_dict={}
   print("liked dict",liked_dict)
   return liked_dict


def song_search(song):
   """
   # Function to search song details with song name
   """
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


def get_playlist_detail(playlist_name_in):
   """
   Function to get all songs in a playlist given playlist name
   """
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


def get_all_playlists():
   """
   Function to fetch all playlists
   """
   try:
      res=cur.execute("select playlist_name from playlist_header")
      list_playlists=res.fetchall()
   except Exception as e:
      print("Unable to fetch all playlists\
            Error Message: ", str(e))
      list_playlists=[]
   return list_playlists


def get_playlist_header(playlist_name_in):
   """
   Function to fetch playlist summary information
   """
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


def delete_playlist(playlist_name):
   """
   Function to Delete a playlist
   """
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


def delete_song_from_playlist(song_name, playlist_name):
   """
   Function to Delete a song from a playlist
   """
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


def close():
   """
   Function to close cursor, connection
   """
   cur.close()
   con.close()



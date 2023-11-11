import sqlite3
import os
#con=sqlite3.connect("d:\songs2.db", isolation_level=None)

con=sqlite3.connect(os.getcwd()+"/database.db",check_same_thread=False)

def init():
   global cur
   cur=con.cursor()
   res = cur.execute("SELECT name FROM sqlite_master where name = 'songs'")

   if (res.fetchone() is None):
      print("creating new songs table")
      con.execute("Create table songs(path varchar(50),duration int,pretty_name varchar(30),thumbnail varchar(50),artists varchar(20))")

   if not(cur.execute("SELECT name FROM sqlite_master where name = 'liked_songs'").fetchone()):
      print("creating new liked_songs table")
      con.execute("Create table liked_songs(path varchar(50),duration int,pretty_name varchar(30),thumbnail varchar(50),artists varchar(20))")


def song_insert(song_list):
   # res = cur.execute("SELECT name FROM sqlite_master where name = 'songs'")
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO songs(path,duration,pretty_name,thumbnail,artists) VALUES (:path, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   con.execute("COMMIT")
   print("add operation done")


def like_song(song_list):
   print("liking ",song_list)
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO liked_songs(path,duration,pretty_name,thumbnail,artists) VALUES (:path, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   con.execute("COMMIT")
   print("like operation done")
def dislike_song(song_list):
   print("disliking ",song_list)
   con.execute("BEGIN TRANSACTION")
   con.execute("delete from liked_songs where pretty_name like '{}'".format(song_list))
   print("delete from liked_songs where pretty_name like '{}'".format(song_list))
   con.execute("COMMIT")
   print("dislike operation done")


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
   
def get_liked_songs():
   print("getting liked songs")
   res=cur.execute("select * from liked_songs")
   liked_list=res.fetchall()
   desc=cur.description
   column_names=[col[0] for col in desc]
   liked_dict=[dict(zip(column_names,row))for row in liked_list]
   print("liked dict",liked_dict)
   return liked_dict

def close():
   cur.close()
   con.close()


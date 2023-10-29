import sqlite3
import os
#con=sqlite3.connect("d:\songs2.db", isolation_level=None)

con=sqlite3.connect(os.getcwd()+"/database.db")

def init():
   cur=con.cursor()
   res = cur.execute("SELECT name FROM sqlite_master where name = 'songs'")
   if (res.fetchone() is None):
      print("creating new table")
      con.execute("Create table songs(path varchar(50),duration int,pretty_name varchar(30),thumbnail varchar(50),artists varchar(20))")
   cur.close()

def song_insert(song_list):
   cur=con.cursor()
   # res = cur.execute("SELECT name FROM sqlite_master where name = 'songs'")
   con.execute("BEGIN TRANSACTION")
   con.execute("INSERT INTO songs(path,duration,pretty_name,thumbnail,artists) VALUES (:path, :duration, :pretty_name, :thumbnail, :artists)",song_list)
   con.execute("COMMIT")
   print("add operation done")
   cur.close()

def song_search(song):
   print("searching")
   cur=con.cursor()
   res1 = cur.execute("SELECT * FROM songs where pretty_name = :song",[song])
   desc=cur.description
   #print(desc)
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

def close():
   con.close()


# Meowsic  

A Free, Open-Source, and Feature-Rich Music Streaming App built in Python.
  
![image](https://github.com/D1gita7Duck/meowsic/assets/84835176/023e1935-52fa-4708-af71-fd26fc6e73a4)
  
# Features:
- Simple and intuitive interface
- Search and play any song from youtube
- Song metadata from spotify always on display
- Like songs and save any song from the queue and access it later from your liked songs list with the touch of a button
- Create and curate playlists with ease
- Get lyrics of a song
- Remote control playback by simply accessing "http://local-ip-address" of the computer the app is runninng on
- Discover tab with constantly updated suggested playlists from Spotify
- Full support for local .mp3 files

# Screenshots:
![image](https://github.com/D1gita7Duck/meowsic/assets/84835176/c55efadb-7e4b-4d8e-ab5b-ded70bf4df78)

![image](https://github.com/D1gita7Duck/meowsic/assets/84835176/426837e4-2abe-48b0-838c-f699105baf38)

![image](https://github.com/D1gita7Duck/meowsic/assets/84835176/64da8b20-49d1-4cc9-beaa-ba3aaed038fe)

![image](https://github.com/D1gita7Duck/meowsic/assets/84835176/0b9d29c8-030d-40b5-9928-577c15a3ac2d)

![image](https://github.com/D1gita7Duck/meowsic/assets/84835176/bacc972d-9e9d-4493-bffd-f30db98d2ce9)

  
# Disclaimer:
Meowsic does not own or have any affiliation with the songs and other content available through the app.
All songs and other content are the property of their respective owners and are protected by copyright law.
Meowsic is not responsible for any infringement of copyright or other intellectual property rights that may result
from the use of the songs and other content available through the app. Meowsic uses third-party plugins and
is not responsible for any harm or damage to the respective owners or any other parties resulting from the use
of the songs and other content through the third-party plugins.
By using the app, you agree to use the songs and other content only for personal, non-commercial purposes
and in compliance with all applicable laws and regulations.
  
# Roadmap:
  
Version 0.5[DONE]:  
-simple customtkinter gui with one search bar and two buttons [DONE]  
-type in search bar and press search to search youtube ,download video and then convert it to mp3 [DONE]  
-press play to start playing the file in windows music player (ik it sucks) [DONE]


Version 0.9[DONE]:  
-moderately complex customtkinter gui with home window ,seperate search window , "currently playing" window on the the bottom or side (to decide after design is final) [DONE]  
-album art , album name , artist name etc to be searched and auto cached using db [DONE]  
-above metadata to be displayed with currently playing song [DONE]   
-play pause stop next and previous functionality [DONE]  
-use libraries to play file in native python instead of using wmp [DONE]  
-ability to store "liked" songs using sql [DONE]  
-above feature to be used to display "recently played" songs with name and album art on the home screen [DONE]   
-make progress bar to show progress of downloading song [DONE]  

Version 1.0:  
-Add seperate lyrics window which displays lyrics as a label in a scrollable frame[DONE]  
-Add Volume control [DONE]  
-playlists functionality with sql db [DONE]  
-robust mechanism for play,pause,stop,next and previous song [DONE]  
-proper queue system [DONE]  
-settings window to change dark/light mode [DONE] , quality of songs downloaded etc  
-ability for users to delete songs and metadata they dont need anymore  
-import songs from spotify playlist to liked songs [DONE]   
-Discover page with curated playlists with top songs and mood songs etc  [DONE]
-Import spotify playlist into new playlist  [DONE]
-Add a button to import all songs from playlist into queue [DONE]
-Shuffle songs in queue  

Version 1.5:  
-everything in 1.0 and more  
-search mechanism to be more accurate and to provide more options to choose from after searching instead of just one  
-better integration with windows like the windows media controls (play pause buttons on keyboard) should work with app  
-better theming  
-more efficient code for faster execution  
-cache management system aka delete music file if not in any playlist or recently played  
-remote control music playback like spotify connect using flask [DONE]  

~Version 2.0:~
~(extreme optimism)~  
~-db storage on server side (cloud like oracle or AWS)~   
~-login features with email and codename (sm sort of a username)~  
~-db stores all of ur preferences ,recently played liked etc~   
~-if new sign in on a device, auto download user's preferences~  
~-give user option to download all songs in playlists at once~  
~-make friends with someone using their app codename (sm sort of a username)~  
~-see what your friends are listening to~  

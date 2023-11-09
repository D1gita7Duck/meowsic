Note: 
-Intermediate versions are likely
-Version 1.5 is initial "end goal"
-if possible we try 2.0

Version 0.5:

-simple customtkinter gui with one search bar and two buttons [DONE]
-type in search bar and press search to search youtube ,download video and then convert it to mp3 [DONE]
-press play to start playing the file in windows music player (ik it sucks) [DONE]


Version 0.9:

-moderately complex customtkinter gui with home window ,seperate search window , "currently playing" window on the the bottom or side (to decide after design is final) [Almost+Done]
-album art , album name , artist name etc to be searched and auto cached using db [DONE]
-above metadata to be displayed with currently playing song [Backend_DONE]
-play pause stop next and previous functionality [DONE]
-use libraries to play file in native python instead of using wmp [DONE]
-ability to store "liked" songs using sql [DONE]
-above feature to be used to display "recently played" songs with name and album art on the home screen [Backend_DONE]
-make progress bar to show progress of downloading song [DONE]

Version 1.0:

-Add seperate lyrics window which displays lyrics as a label in a scrollable frame
-everything from 0.9 and more
-playlists functionality with sql db
-robust mechanism for play,pause,stop,next and previous song [DONE]
-proper queue system [DONE] 
-search mechanism to be more accurate and to provide more options to choose from after searching instead of just one
-settings window to change dark/light mode , quality of songs downloaded etc
-ability for users to delete songs and metadata they dont need anymore


Version 1.5:

-everything in 1.0 and more
-better integration with windows like the windows media controls (play pause buttons on keyboard) should work with app
-better theming
-more efficient code for faster execution
-cache management system aka delete music file if not in any playlist or recently played
-remote control music playback like spotify connect using flask [DONE]


Version 2.0:
(extreme optimism)

-db storage on server side (cloud like oracle or AWS)
-login features with email and codename (sm sort of a username)
-db stores all of ur preferences ,recently played liked etc 
-if new sign in on a device, auto download user's preferences
-give user option to download all songs in playlists at once
-make friends with someone using their app codename (sm sort of a username)
-see what your friends are listening to

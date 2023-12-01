import os
import time
import tkinter
import customtkinter as ctk
import CTkMenuBar
import CTkTable
from PIL import Image, ImageTk
import CTkListbox
import app.music as music
import app.functions as functions
import app.theme as theme

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
master_theme=functions.current_theme #USE LIGHTMODE AT RISK OF BLINDING YOURSELF
if master_theme=="dark":
    current_theme=theme.dark_mode
else:
    current_theme=theme.light_mode

app = ctk.CTk(fg_color=current_theme["color1"])  # create CTk window like you do with the Tk window
app.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,), weight=1)
app.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)

scale_factor=1920/app.winfo_screenwidth()

current_time=time.localtime()
warn_win=None
# thumbnails folder path
thumbs_folder_path = os.path.join("thumbs")


# buttons folder path
icon_folder_path = os.path.join(
    os.path.join(os.path.dirname(
        os.path.realpath(__file__)), "assets", "icons")

)
garfield_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "garfield.png")), size=(225//scale_factor, 225//scale_factor)
)
library_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "library_icon.png")), size=(30//scale_factor, 30//scale_factor)
)


# button icons
play_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "play_btn.png")), size=(30, 30)
)
pause_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "pause_btn.png")), size=(30, 30)
)
next_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "next_btn.png")), size=(26, 26)
)
previous_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "previous_btn.png")), size=(26, 26)
)
search_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "search_btn.png")), size=(30, 30)
)
lyrics_button_icon_white=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path,"song_lyrics_white.png")),size=(30,30)
)
lyrics_button_icon_orange=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path,"song_lyrics_orange.png")),size=(30,30)
)
disliked_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "disliked_btn.png")), size=(30, 30)
)
like_button_icon = ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "like_btn.png")), size=(30, 30)
)
add_to_queue_button_icon= ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "add_queue_btn.png")), size=(30, 30)
)
delete_from_queue_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "delete_queue_btn.png")), size=(30, 30)
)
delete_from_queue_tk_button_icon=ImageTk.PhotoImage(
    Image.open(os.path.join(icon_folder_path, "delete_queue_btn.png")).resize((30,30))
)
add_to_playlist_button_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "add_to_playlist_icon.png")), size=(30, 30)
)
add_to_playlist_tk_button_icon=ImageTk.PhotoImage(
    Image.open(os.path.join(icon_folder_path, "add_to_playlist_icon.png")).resize((30,30))
)

information_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "info_icon.png")), size=(30, 30)
)
volume_full_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_full.png")), size=(30, 30)
)
volume_2bar_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_2bar.png")), size=(30, 30)
)
volume_1bar_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "volume_1bar.png")), size=(30, 30)
)
mute_icon=ctk.CTkImage(
    Image.open(os.path.join(icon_folder_path, "mute_icon.png")), size=(30, 30)
)

#define top level import window
def import_win_launch():
    global import_entry
    global import_window
    global import_progress
    
    import_window=ctk.CTkToplevel(app,fg_color=current_theme["color1"])
    import_window.geometry("300x300")
    import_window.title('Import tracks from Spotify playlist')

    import_entry=ctk.CTkEntry(import_window,placeholder_text="Enter playlist URL",fg_color=current_theme["color1"],border_color=current_theme["color4"],text_color=current_theme["color3"],placeholder_text_color=current_theme["color3"])
    import_entry.pack(pady=20)

    import_progress=ctk.CTkProgressBar(import_window,mode="indeterminate",fg_color=current_theme["color1"],border_color=current_theme["color2"],progress_color=current_theme["color3"])
    import_progress.pack(fill="x",padx=20)


    import_button=ctk.CTkButton(
        import_window,
        text="Import to Queue",
        command=music.import_sp_playlist,
        fg_color=current_theme["color4"],
        hover_color=current_theme["color4"],
        border_color=current_theme["color3"],
        border_width=1,
        text_color=current_theme["color6"],)
    
    import_button.pack(pady=20)
    import_button=ctk.CTkButton(
        import_window,
        text="Import to Playlist",
        command=music.import_sp_playlist_to_new_playlist,
        fg_color=current_theme["color4"],
        hover_color=current_theme["color4"],
        border_color=current_theme["color3"],
        border_width=1,
        text_color=current_theme["color6"],)
    import_button.pack(pady=20)
# toggling theme
def toggle_theme(t):
    global current_theme
    global warn_win
    print(current_theme)
    if t=='dark':
        functions.change_mode("dark")
        ctk.set_appearance_mode('dark')
    else:
        functions.change_mode("light")
        ctk.set_appearance_mode('light')
    if warn_win is None:
        warn_win=ctk.CTkToplevel(app)
        warn_win.resizable(False,False)
        app.eval(f'tk::PlaceWindow {str(warn_win)} center')
        warn_win.geometry('200x100')
        text_label=ctk.CTkLabel(master=warn_win,
                                text='Restart Required',
                                image=information_icon,
                                compound='left',
                                anchor='center',)
        text_label.pack(pady=(20,20), padx=(10,10), anchor='center')

        # put the toplevel on top of all windows
        warn_win.attributes('-topmost',True)
        warn_win.focus()

# rightclickmenu pops up on calling this function
def do_popup(_event, frame):
    # print('EVENT IS ', event)
    x1 = song_list_frame.winfo_rootx()
    y1 = song_list_frame.winfo_rooty()
    x2=song_list_frame.winfo_width()+x1
    y2=song_list_frame.winfo_height()+y1
    abs_coord_x = app.winfo_pointerx() - app.winfo_vrootx()
    abs_coord_y = app.winfo_pointery() - app.winfo_vrooty()
    print(x1,y1,x2,y2,abs_coord_x,abs_coord_y)
    if (550<=abs_coord_x and abs_coord_x<=1261) and (157<=abs_coord_y and abs_coord_y<=450) and master_tab.get()=='Queue' and music.loaded:
        try: 
            frame.tk_popup(abs_coord_x, abs_coord_y)
        finally: 
            frame.grab_release()

def return_pressed(event=None):
    print(event)
    print('RETURN PRESSED')

def on_mouse_click(_event=None):
    '''
    Focusses the widget that is clicked (mouse1). 
    Deletes all playlist tabs (if open)
    '''
    _event.widget.focus_set()

    current_focus=(str(app.focus_get()).split('.'))

    # print(master_tab._tab_dict)

    # check if currently focussed widget is not a playlist tab
    if current_focus[-3]=='!ctksegmentedbutton' and current_focus[-2] in ['!ctkbutton5','!ctkbutton4','!ctkbutton3','!ctkbutton2','!ctkbutton']:
        try:
            # try to delete the playlist tab
            for name in master_tab._tab_dict:
                if name not in ['Home', 'Queue', 'Search', 'Your Library', 'Liked Songs',"Discover"]:
                    master_tab._name_list.remove(name)
                    master_tab._tab_dict[name].grid_forget()
                    master_tab._tab_dict.pop(name)
                    master_tab._segmented_button.delete(name)
        except RuntimeError: 
            # runtime error is flashed as the master_tab._tab_dict changes size while the function is called
            pass

# menu
menu = CTkMenuBar.CTkMenuBar(app)
menu.lift()
file_button = menu.add_cascade("File")
edit_button = menu.add_cascade("Edit")
options_button = menu.add_cascade("Options")
about_button = menu.add_cascade("About")

# file tab
file_dropdown = CTkMenuBar.CustomDropdownMenu(widget=file_button)
file_dropdown.add_option(option="Open", command=music.add_songs)
file_dropdown.add_option(option="Import Spotify Playlist", command=import_win_launch)
file_dropdown.add_option(option="Save")

file_dropdown.add_separator()

sub_menu = file_dropdown.add_submenu("Export As")
sub_menu.add_option(option=".TXT")
sub_menu.add_option(option=".PDF")

# options tab
options_dropdown=CTkMenuBar.CustomDropdownMenu(widget=options_button)
# light and dark mode toggle button
theme_switch=ctk.CTkSwitch(
    master=options_dropdown,
    onvalue='dark',
    offvalue='light',
    text='Dark Mode',
    command=lambda: toggle_theme(theme_switch.get()),
)
theme_switch.pack(pady=(10,10), padx=(10,10), anchor='center',fill='x',)
if master_theme=="dark":
    theme_switch.select()
else:
    theme_switch.deselect()
#frame for tabview and metadata and misc frame
big_frame = ctk.CTkFrame(master=app, height=800,fg_color=current_theme["color1"],border_width=0)
big_frame.pack(pady=(20, 20), anchor='center', fill='x', ipadx=10)
big_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10), weight=1)
big_frame.lower()

# Create Tabview
master_tab = ctk.CTkTabview(
    master=big_frame,
    width=800//scale_factor,
    height=550//scale_factor,
    corner_radius=10,
    border_width=2,
    border_color=current_theme["color3"],
    fg_color=current_theme["color2"],
    segmented_button_selected_color=current_theme["color1"],
    segmented_button_selected_hover_color=current_theme["color2"],
    segmented_button_unselected_hover_color=current_theme["color4"],
)
master_tab.grid(pady=(10,10), row=0, column=1, columnspan=8, padx=(30,10),)
master_tab._segmented_button.configure(font=('Helvetica', 22,))

# Create tabs
home_tab = master_tab.add('Home')
queue_tab = master_tab.add('Queue')
search_tab = master_tab.add('Search')
liked_songs_tab = master_tab.add('Liked Songs')
your_library_tab=master_tab.add('Your Library')
discover_tab=master_tab.add("Discover")
# home tab stuff
home_tab.grid_columnconfigure((0, 1, 2, 3, 4, 5,), weight=1)

# checking for morning, afternoon, evening
if current_time[3] >= 7 and current_time[3] < 12:
    greeting_text = 'Good Morning'
elif current_time[3] >= 12 and current_time[3] <= 16:
    greeting_text = 'Good Afternoon'
else:
    greeting_text = 'Good Evening'
greeting_label = ctk.CTkLabel(
    master=home_tab, text=greeting_text, font=('Helvetica', 20),text_color=current_theme["color3"],width=20,height=20)
greeting_label.grid(row=0, column=5, sticky='ew', pady=(20, 20), columnspan=3,)

# division home tab into two frames
home_tab_recently_played = ctk.CTkFrame(
    master=home_tab, border_color='black', border_width=2)
home_tab_recently_played.grid(
    row=1, columnspan=3, column=6, rowspan=5, sticky='ew' , padx=(20,10))

recently_played_listbox = CTkListbox.CTkListbox(master=home_tab_recently_played,
                                                width=500//scale_factor,
                                                height=200//scale_factor,
                                                border_width=2,
                                                corner_radius=10,
                                                label_text='Recently Played',
                                                label_font=('Helvetica', 22) ,
                                                font=('Helvetica',18),
                                                label_anchor='center',
                                                border_color=current_theme["color3"],
                                                fg_color=current_theme["color3"],
                                                text_color=current_theme["color6"],
                                                hightlight_color=current_theme["color6"],
                                                hover_color=current_theme["color4"],
                                                select_color=current_theme["color5"],)
if functions.get_recents():
    for i in functions.get_recents():
        recently_played_listbox.insert('END', i,onclick=music.load_recents)
recently_played_listbox.grid(columnspan=5, sticky='ew',)

#buttons on home page
home_tab_buttons_frame=ctk.CTkFrame(
    master=home_tab, border_color=current_theme["color3"], border_width=2,fg_color=current_theme["color2"]
)
home_tab_buttons_frame.grid(row=1, column=0, columnspan=3, rowspan=5, sticky='ew', padx=(10,10) ,)
home_tab_buttons_frame.grid_columnconfigure(0, weight=1)

home_tab_your_library_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//scale_factor,
    height=50//scale_factor,
    text='Your Library',
    image=library_button_icon,
    fg_color=current_theme["color4"],
    hover_color=current_theme["color4"],
    border_color=current_theme["color6"],
    border_width=1,
    text_color=current_theme["color6"],
    anchor='center',
    command=music.show_your_library
)
home_tab_your_library_button.grid(row=0, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')

home_tab_liked_songs_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//scale_factor,
    height=50//scale_factor,
    text='Liked Songs',
    image=like_button_icon,
    anchor='center',
    command=music.show_liked_songs,
    fg_color=current_theme["color4"],
    hover_color=current_theme["color4"],
    border_color=current_theme["color6"],
    border_width=1,
    text_color=current_theme["color6"]
)
home_tab_liked_songs_button.grid(row=1, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')

discover_button=ctk.CTkButton(
    master=home_tab_buttons_frame,
    width=200//scale_factor,
    height=50//scale_factor,
    text='Discover',
    anchor='center',
    command=music.show_discover,
    fg_color=current_theme["color4"],
    hover_color=current_theme["color4"],
    border_color=current_theme["color6"],
    border_width=1,
    text_color=current_theme["color6"]
)
discover_button.grid(row=2, column=0, columnspan=3, padx=(10,10), pady=(10,10), sticky='ew')
# Search Frame
search_frame = ctk.CTkFrame(search_tab,fg_color=current_theme["color1"])
search_frame.pack(fill='x', expand=True, padx=10, pady=10)

# Create a search bar
search_bar = ctk.CTkEntry(search_frame,fg_color=current_theme["color1"],border_color=current_theme["color4"],text_color=current_theme["color3"],placeholder_text="Search",placeholder_text_color=current_theme["color3"])
search_bar.pack(fill='x', expand=True, padx=10, pady=10)

search_progress=ctk.CTkProgressBar(search_frame,mode="indeterminate",fg_color=current_theme["color1"],border_color=current_theme["color2"],progress_color=current_theme["color3"])
search_progress.pack(fill="x",padx=10)


# Create a search button
search_button = ctk.CTkButton(
    search_frame, 
    text="Search", 
    command=music.search, 
    image=search_button_icon,
    fg_color=current_theme["color4"],
    hover_color=current_theme["color4"],
    border_color=current_theme["color3"],
    border_width=1,
    text_color=current_theme["color6"],)  
search_button.pack(fill='x', expand=True, padx=10, pady=10)



# song list frame
song_list_frame = ctk.CTkFrame(master=queue_tab, height=500,fg_color=current_theme["color2"],border_width=0)
song_list_frame.grid(row=1, pady=20, sticky='ew', padx=(20, 20))

# Media Controls Frame
playback_controls_frame = ctk.CTkFrame(master=app, fg_color=current_theme["color2"], corner_radius=20 , width=1250//scale_factor)
playback_controls_frame.pack(side='bottom', pady=(20, 20), ipadx=10, expand=True, anchor='center')  # removed fill='x'
playback_controls_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11,12), weight=1)
# liked songs frame
liked_songs_frame = ctk.CTkFrame(master=liked_songs_tab,fg_color=current_theme["color2"],border_width=0)
liked_songs_frame.grid(row=1, pady=(20, 20), padx=(20, 20), sticky='ew')

# song metadata frame
song_metadata_frame = ctk.CTkFrame(
    master=big_frame,
    width=350//scale_factor,
    height=400//scale_factor,
    fg_color=current_theme["color2"],
    border_color=current_theme["color3"],
    border_width=2
)
song_metadata_frame.grid(row=0, column=7, columnspan=3, rowspan=3,sticky="e")
song_metadata_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

# misc functions frame (add to playlist, delete from queue, add to queue)
misc_frame=ctk.CTkFrame(
    master=big_frame,
    fg_color=current_theme["color2"],
    corner_radius=20,
    border_width=2,
    border_color=current_theme["color3"],
)

misc_frame.grid(row=0, column=0, columnspan=3, padx=(10,10) )
misc_frame.grid_columnconfigure(0, weight=1)
misc_frame.grid_rowconfigure((0,1,2), weight=1)

# unmap misc_frame, add to playlist and delete from queue are available in context menu
misc_frame.grid_forget()

# your library stuff
your_library_tab.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1)

your_library_frame=ctk.CTkScrollableFrame(
    master=your_library_tab,
    width=700,
    height=250,
    border_width=0,
    border_color='black',
    corner_radius=10,
    label_text='Playlists',
    label_anchor='center',
    fg_color=current_theme["color3"],
)
your_library_frame.grid(row=0, pady=(20,20), padx=(10,10),sticky='ew')
your_library_frame.grid_columnconfigure((0,1,2,3,4,5),weight=1)

playlist_table_values=[
    ['Name', 'Date Created','Songs','Duration'],
]

for i in functions.get_playlists():
    t=functions.get_playlist_details(i)
    print('playlist_details',t,i)
    playlist_table_values.append(t)

def open_playlist(value):
    #value is dictionary of kwargs of CTkTable
    music.show_playlist(value)

playlists_table=CTkTable.CTkTable(
    master=your_library_frame,
    values=playlist_table_values,
    command=open_playlist,
    fg_color=current_theme["color2"]
)
playlists_table.grid(row=0, columnspan=9, sticky='ew')

discover_tab.grid_columnconfigure((0,1,2,3,4,5,6,7), weight=1)

discover_frame=ctk.CTkScrollableFrame(
    master=discover_tab,
    width=700,
    height=250,
    border_width=0,
    border_color='black',
    corner_radius=10,
    label_text='Recommended Playlists',
    label_anchor='center',
    fg_color=current_theme["color3"],
)
discover_frame.grid(row=0, pady=(20,20), padx=(10,10),sticky='ew')
discover_frame.grid_columnconfigure((0,1,2,3,4,5),weight=1)

discover_table_values=[] 
rec_playlists=functions.get_recommmended_playlist()
for name in rec_playlists.keys():
    discover_table_values.append([name])

def open_discover_playlist(value):
    music.show_discover_playlist(value)

discover_table=CTkTable.CTkTable(
    master=discover_frame,
    values=discover_table_values,
    command=open_discover_playlist,
    fg_color=current_theme["color2"]
)
discover_table.grid(row=0, columnspan=9, sticky='ew')

# misc frame buttons
add_to_playlist_label_text=ctk.StringVar(value='Add to Playlist')
print(functions.get_playlists())
add_to_playlist_options=['Create New Playlist'] + [x[0] for x in functions.get_playlists()]

add_to_playlist_menu=ctk.CTkOptionMenu(
    misc_frame,
    width=200//scale_factor,
    height=35//scale_factor,
    command=music.add_to_playlist,
    variable=add_to_playlist_label_text,
    values=add_to_playlist_options,
    state='disabled',
    fg_color=current_theme["color4"],
    text_color=current_theme["color6"]
)
add_to_playlist_menu.grid(row=0, column=0, columnspan=2,  padx=(10,10), pady=(20,10), sticky='ew')

# add to queue
# add_to_queue_button=ctk.CTkButton(
#     misc_frame,
#     width=200,
#     height=30,
#     command=music.add_to_queue,
#     text='Add to Queue',
#     image=add_to_queue_button_icon,
#     anchor='center'
# )
# add_to_queue_button.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=(10,20), sticky='ew')

# delete from queue
delete_from_queue_button=ctk.CTkButton(
    misc_frame,
    width=30//scale_factor,
    height=30//scale_factor,
    command=music.delete_from_queue,
    text='Delete from Queue',
    #image=delete_from_queue_button_icon,
    anchor='center',
    state='disabled',
    fg_color=current_theme["color4"],
    hover_color=current_theme["color4"],
    border_color=current_theme["color3"],
    border_width=1,
    text_color=current_theme["color6"]
)
delete_from_queue_button.grid(row=1, column=0, columnspan=2, padx=(10,10), pady=(10,20), sticky='ew')

#playback controls buttons
like_button = ctk.CTkButton(
    playback_controls_frame,
    text='',
    command=lambda: music.like(like_button),
    image=disliked_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
like_button.grid(row=0, column=0, padx=(30, 10),)

previous_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.song_previous,
    image=previous_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state="disabled"
)
previous_button.grid(row=0, column=6, padx=(10, 10), sticky='ew')

play_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=lambda: music.play_pause(play_button),
    image=play_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
play_button.grid(row=0, column=7, padx=(10, 10), sticky='ew')

next_button = ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.song_next,
    image=next_button_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
next_button.grid(row=0, column=8, padx=(10, 10), sticky='ew')

lyrics_button=ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.main_lyrics,
    image=lyrics_button_icon_white,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
lyrics_button.grid(row=0,column=9,padx=(10,30),sticky="ew")

volume_button=ctk.CTkButton(
    playback_controls_frame,
    text="",
    command=music.mute_unmute,
    image=volume_full_icon,
    border_width=0,
    corner_radius=100,
    fg_color="transparent",
    hover=False,
    width=0,
    height=0,
    state='disabled'
)
volume_button.grid(row=0,column=11,padx=(10,10),sticky="ew")

volume_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=150//scale_factor,
    orientation="horizontal",
    progress_color=current_theme["color3"],
    button_color=current_theme["color4"],
    button_hover_color=current_theme["color5"],
    command=music.volume,
    state='disabled'
)
volume_slider.grid(row=0, column=12, columnspan=3, pady=5, sticky='ew', padx=(10,30))
volume_slider.set(100)

song_slider = ctk.CTkSlider(
    master=playback_controls_frame,
    from_=0,
    to=100,
    width=500//scale_factor,
    orientation="horizontal",
    progress_color=current_theme["color3"],
    button_color=current_theme["color4"],
    button_hover_color=current_theme["color5"],
    command=music.slide,
    state='disabled'
)
song_slider.grid(row=0, column=2, columnspan=3, pady=20, sticky='ew')

# Songs List
song_list = CTkListbox.CTkListbox(
    master=song_list_frame,
    width=700//scale_factor,
    height=120//scale_factor,
    border_width=2,
    corner_radius=10,
    label_text="Songs",
    label_anchor='center',
    border_color=current_theme["color2"],
    fg_color=current_theme["color3"],
    text_color=current_theme["color6"],
    hightlight_color=current_theme["color2"],
    hover_color=current_theme["color4"],
    select_color=current_theme["color5"],
)

song_list.grid(row=0, columnspan=9, pady=(10, 30), sticky='ew')


# context menu to add songs to playlist and delete them from queue
RightClickMenu = tkinter.Menu(song_list, tearoff=False, background='#565b5e', fg='white', borderwidth=0, bd=0)
# adding delete from queue command
RightClickMenu.add_command(
    label=" Delete From Queue",
    command=music.delete_from_queue,
    image=delete_from_queue_tk_button_icon,
    compound='left',
)

# submenu for add to playlist commands
add_to_playlist_submenu=tkinter.Menu(RightClickMenu)

# create a cascade for adding to playlist
RightClickMenu.add_cascade(
    label=' Add to Playlist',
    menu=add_to_playlist_submenu,
    image=add_to_playlist_tk_button_icon,
    compound='left',
)

# add all playlists into the cascade
for playlist_name in add_to_playlist_options:
    add_to_playlist_submenu.add_command(label=playlist_name,command= lambda name=playlist_name:music.add_to_playlist(name))


# liked songs listbox
liked_songs_listbox = CTkListbox.CTkListbox(
    master=liked_songs_frame,
    width=700//scale_factor,
    height=120//scale_factor,
    border_width=2,
    corner_radius=10,
    label_text='Liked Songs',
    label_anchor='center',
    fg_color=current_theme["color3"],
    text_color=current_theme["color6"],
    hightlight_color=current_theme["color2"],
    hover_color=current_theme["color4"],
    select_color=current_theme["color5"],
)

liked_songs_listbox.grid(row=0, columnspan=9, pady=(20, 20), sticky='ew')

for i in functions.get_liked_songs():
    liked_songs_listbox.insert("END",i["pretty_name"],onclick=music.load_liked)


# time labels
time_elapsed_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
time_elapsed_label.grid(row=0, column=1, sticky='w', padx=(50, 20))


total_time_label = ctk.CTkLabel(
    master=playback_controls_frame, text="--:--", text_color='white')
total_time_label.grid(row=0, column=5, sticky='e', padx=(20, 50))


# song metadata labels

# album art label
song_metadata_image_label = ctk.CTkLabel(
    song_metadata_frame, text='', image=garfield_icon,)
song_metadata_image_label.grid(row=0, columnspan=3, sticky='new', )

# artist name label
song_metadata_artist_label = ctk.CTkLabel(
    song_metadata_frame, text='Artist: Garfield', text_color='white')
song_metadata_artist_label.grid(row=1, columnspan=3, sticky='ew', pady=(20, 10))

# now playing label
status_bar = ctk.CTkTextbox(
    master=song_metadata_frame,
    height=40,
    text_color='white',
    wrap='none',
    fg_color = current_theme["color2"],
)

status_bar.grid(row=2, columnspan=3, pady=(10, 20), padx=(10, 10), sticky='ew')
status_bar.tag_config('center', justify='center')
status_bar.insert('end', 'Status Bar', 'center')
status_bar.configure(state='disabled')


'''Key Bindings'''

# bind mouse1
# <1> is a synonym for <ButtonPress-1> (aka left mouse button)
app.bind("<1>", lambda event: on_mouse_click(_event=event))

# bind space key to play/pause
app.bind('<space>', lambda event: music.play_pause(play_button, _event=event) if type(app.focus_get())!=tkinter.Entry else print('Focus in EntryBox'))
# bind f8 to song_next
app.bind('<F8>', lambda event: music.song_next(_event=event))
# bind f6 to song_previous
app.bind('<F6>', lambda event: music.song_previous(_event=event))
# bind enter key to search the song
app.bind('<Return>', lambda event: music.search())
# bind mouserightclick to popup the context menu
song_list.bind("<Button-3>", lambda event: do_popup(event, frame=RightClickMenu))
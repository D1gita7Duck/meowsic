import customtkinter as ctk
import pygame.mixer
from PIL import Image , ImageTk
import os

pygame.mixer.init()
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green



app = ctk.CTk()  # create CTk window like you do with the Tk window
app.geometry("500x500")
app.title('meowsic')
app.iconbitmap('H:\Arnav\Python\Python Workspace\meowsic\\assets\icons\\app_icon.ico')


playing=0

def load_music():
    song_path="H:\Arnav\Python\Python Workspace\meowsic\Audio\song1.mp3"
    pygame.mixer.music.load(song_path)

def song_previous():
    pass

def song_next():
    pass





def play_pause(btn:ctk.CTkButton):

    global playing

    if playing==1 :
        pygame.mixer.music.pause()
        btn.configure(image=play_button_icon)
        playing = 2

    elif playing == 2:
        pygame.mixer.music.unpause()
        btn.configure(image=pause_button_icon)
        playing = 1
    elif playing == 0:
        pygame.mixer.music.play()
        btn.configure(image=pause_button_icon)
        playing = 1



load_music()


#Frames
master_frame=ctk.CTkFrame(app)
master_frame.pack(pady=20)

playback_controls_frame=ctk.CTkFrame(master_frame)
playback_controls_frame.grid(row=1,column =0 )









icon_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets\icons")
play_button_icon = ctk.CTkImage(Image.open(os.path.join(icon_folder_path, "play_btn.png")),size=(30,30))
pause_button_icon= ctk.CTkImage(Image.open(os.path.join(icon_folder_path, "pause_btn.png")),size=(30,30))
next_button_icon= ctk.CTkImage(Image.open(os.path.join(icon_folder_path, "next_btn.png")),size=(26,26))
previous_button_icon= ctk.CTkImage(Image.open(os.path.join(icon_folder_path, "previous_btn.png")),size=(26,26))

previous_button= ctk.CTkButton(playback_controls_frame, text='', command= song_previous , image = previous_button_icon, border_width= 0 , fg_color= 'transparent' , hover= False )
previous_button.grid(row=0, column = 0 , padx=10)

play_button = ctk.CTkButton(playback_controls_frame, text='', command=lambda : play_pause(play_button), image=play_button_icon, border_width=0,  fg_color= 'transparent',  hover= False )
play_button.grid(row=0, column= 1 , padx=10)

next_button= ctk.CTkButton(playback_controls_frame, text='', command= song_next , image = next_button_icon, border_width= 0 , fg_color= 'transparent' , hover= False )
next_button.grid(row=0, column=2, padx=10)

app.mainloop()

import os
import customtkinter as ctk
import pygame.mixer
import remote.server as server
from app.widgets import app

app.geometry(f'{str(app.winfo_screenwidth())}x{str(app.winfo_screenheight())}')
app.title("meowsic")
app.iconbitmap(os.path.join(os.getcwd(),"app","assets", "icons", "app_icon.ico"))

pygame.mixer.init()
server.start()

def kill_all():
    """
    destroys app and kills flask
    """
    app.destroy()
    server.kill_app()


app.protocol("WM_DELETE_WINDOW", kill_all)
app.after(0, lambda: app.state('zoomed'))

app.mainloop()

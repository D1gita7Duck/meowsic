import pygame.mixer
import remote.server as server
from app.widgets import app, _kill_all

pygame.mixer.init()
server.start()


app.protocol("WM_DELETE_WINDOW", _kill_all)
app.after(0, lambda: app.state('zoomed'))

app.mainloop()

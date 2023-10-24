import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import PrettyPrinter
pp=PrettyPrinter()
#Authentication - without user
client_credentials_manager = SpotifyClientCredentials(client_id="e75a7570a4a64aa9bb953f2c05f7f136", client_secret="fac7299b84854f459874bcb149c7df40")
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

pp.pprint(sp.search(q="ordinary person leo",limit=1,type="track"))
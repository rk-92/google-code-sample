"""A video playlist class."""


from .video_library import VideoLibrary
# from .video_player import VideoPlayer

class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, playlist_name, videos):
        self._video_library = VideoLibrary()
        self.playlist_name = playlist_name
        self.playlist_videos=[]


    def set_playlist_name(self, playlist_name):
        self.playlist_name= playlist_name

    def get_playlist_name(self):
        return self.playlist_name
    # def add_videos(self, video_id):

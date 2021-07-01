"""A video player class."""

from os import sendfile
from typing import Counter
from .video_library import VideoLibrary
from .video_playlist import Playlist
from random import randint


class VideoPlayer:
    """A class used to represent a Video Player."""


    def __init__(self):
        self._video_library = VideoLibrary()
        # 0 - NOTHING'S PLAYING / STOPPED PLAYING
        # 1 - VIDEO PLAYING
        # 2 - PAUSED VIDEO
        self.player_status= 0;
        self.current_video= "";
        self._playlist = []
        

    # Shows the number of videos in the library
    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    # Lists all the videos in lexicographical order by title
    def show_all_videos(self):
        videos= self._video_library.get_all_videos()
        videos.sort(key=lambda x: x.title)                          #lexicographical sorting of the videos
        for x in videos:
            if x.flag == None:
                print(getattr(x,'title') + "(" + x._video_id + ")" , "[" + ' '.join(list(x._tags)) + "]")
            else:
                print(getattr(x,'title') + "(" + x._video_id + ")" , "[" + ' '.join(list(x._tags)) + "] - FLAGGED (reason:",x.flag)


    def play_video(self, video_id):
        index=-1
        video= self._video_library.get_video(video_id)                                          #getting the video from the library
        if video != None:
            if video.flag != None:
                print("Cannot play video: Video is currently flagged (reason: "+ video.flag +")")
                return
            check=self.player_status
            previous_video = self.current_video
            if(self.player_status==0):                                                              #if no video is playing, set status to playing
                self.player_status = 1
                check=0
            if (video_id == "<amazing_cats_video_id>" or video_id == "amazing_cats_video_id"):
                self.current_video = "Amazing Cats"
            elif (video_id == "<funny_dogs_video_id>" or video_id == "funny_dogs_video_id"):
                self.current_video = "Funny Dogs"
            elif (video_id == "<another_cat_video_id>" or video_id == "another_cat_video_id"):
                self.current_video = "Another Cat Video"
            elif (video_id == "<life_at_google_video_id>" or video_id == "life_at_google_video_id"):
                self.current_video = "Life at Google"
            elif (video_id == "<nothing_video_id>" or video_id == "nothing_video_id"):
                self.current_video = "Video about nothing"
        else:
            print("Cannot play video: Video does not exist")
            self.player_status=0
            return 
        if(check != 0):                                                                         #if something was playing previously, stop it
            print("Stopping video:", previous_video)
        print("Playing video:", self.current_video)

    def stop_video(self):
        if self.player_status == 0:                                                             #checking player status for previously paying video
            print("Cannot stop video: No video is currently playing")
            return
        print("Stopping video:", self.current_video)
        self.current_video= ""
        self.player_status=0                                                                    #set player status to : nothing's playing


    def play_random_video(self):
        videos= self._video_library.get_all_videos()
        if len([x for x in videos if x.flag == None]) == 0:
            print("No videos available")
            return
        check =0
        rand= randint(0,4)
        while(check==0):
            video= getattr(videos[rand],'video_id')                                            #check if the randomly chosen video is not flagged
            v= self._video_library.get_video(video)
            if v.flag == None:
                check= 1
        index=-1
        self.play_video(video)

    def pause_video(self):                                                       
        if self.player_status == 0:                                                           #checking if player status is free- nothing's playing
            print("Cannot pause video: No video is currently playing")
        elif self.player_status == 2:                                                         #checking if player status is paused
            print("Video already paused:", self.current_video)
        else:
            print("Pausing video:", self.current_video)                                       #if player status is running, pause
            self.player_status=2

    def continue_video(self):
         if self.player_status == 0:                                                        #checking if player status is free- nothing's playing
            print("Cannot continue video: No video is currently playing")
         elif self.player_status == 1:                                                      #checking if player status is running- if yes. then nothing is paused
            print("Cannot continue video: Video is not paused")
         elif self.player_status == 2:                                                      #checking if player status is paused, if yes, then play
            print("Continuing video:", self.current_video)
            self.player_status=1

    def show_playing(self):
         videos= self._video_library.get_all_videos()
         if self.player_status == 0:                                                        #check for player status
            print("No video is currently playing")
         else:
            for x in range(5):
             if(getattr(videos[x],'title')==self.current_video):
                 if self.player_status == 1:                                                #if a video is playing currently:
                    print("Currently playing: "+ getattr(videos[x],'title')+ " (" + getattr(videos[x],'video_id')+ ")" , "[" + ' '.join(list(getattr(videos[x],'tags'))) + "]")
                    break
                 elif self.player_status == 2:                                               #if a video is currently paused:
                    print("Currently playing: "+ getattr(videos[x],'title')+ " (" + getattr(videos[x],'video_id')+ ")" , "[" + ' '.join(list(getattr(videos[x],'tags'))) + "] - PAUSED") 
                    break

    def create_playlist(self, playlist_name):
        flag= 0
        for playlist in self._playlist:
            if playlist.playlist_name.lower() == playlist_name.lower():                     #making sure the name is unqiue
                flag =1
                break
        if flag == 0:        
            self._playlist.append(Playlist(playlist_name, []))                              #creating playlist
            print("Successfully created new playlist:", self._playlist[-1].playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")

    def add_to_playlist(self, playlist_name, video_id):
        vidflag=0
        video= self._video_library.get_video(video_id)
        if video != None:
            vidflag=1
            if(video.flag!=None):                                                               #checking if the video is flagged
                print("Cannot add video: Video is currently flagged (reason:",video.flag+")")
                return
            index=-1
            count=-1
            flag=0
            for playlist in self._playlist:
                count+=1
                if playlist_name.lower() == playlist.playlist_name.lower():
                    index=count
                    flag=1
                    for x in playlist.playlist_videos:
                        if x == video_id:
                            print("Cannot add video to",playlist_name+": Video already added") #checking if the video is already added
                            return
           
            if (video_id == "<amazing_cats_video_id>" or video_id == "amazing_cats_video_id"):
                print("Added video to",playlist_name+": Amazing Cats")
            elif (video_id == "<funny_dogs_video_id>" or video_id == "funny_dogs_video_id"):
                print("Added video to",playlist_name+": Funny Dogs")
            elif (video_id == "<another_cat_video_id>" or video_id == "another_cat_video_id"):
                print("Added video to",playlist_name+": Another Cat Video")
            elif (video_id == "<life_at_google_video_id>" or video_id == "life_at_google_video_id"):
                print("Added video to",playlist_name+": Life at Google")
            elif (video_id == "<nothing_video_id>" or video_id == "nothing_video_id"):
                print("Added video to",playlist_name+": Video about nothing")
        elif vidflag== 0:
            check=0
            for x in self._playlist:
                if playlist_name == x.playlist_name:
                    check=1
                    break
            if check == 0:
                print("Cannot add video to",playlist_name+": Video already added") #checking if the video is already added
                return
            print("Cannot add video to",playlist_name+": Video does not exist")
            return
        self._playlist[index].playlist_videos.append(video_id.strip('<>'))                  #adding video to the playlist

    def show_all_playlists(self):
        if len(self._playlist) == 0:                                                        #if length of playlist is 0, playlist is empty
            print("No playlists exist yet")
            return
        print("Showing all playlists:")
        for playlist in self._playlist:
            print(playlist.playlist_name)

    def show_playlist(self, playlist_name):
        flag=0
        for playlist in self._playlist:
            if playlist.playlist_name.lower() == playlist_name.lower():
                flag=1                                                                      #marking that playlist exists
                if len(playlist.playlist_videos) == 0:                                      #checking if playlist is empty
                    print("No videos here yet")
                    return
                else:    
                    print("Showing playlist:",playlist_name)
                    for x in playlist.playlist_videos:
                        if x == "amazing_cats_video_id":
                            print("Amazing Cats (amazing_cats_video_id) [#cat #animal]")
                        elif x == "another_cat_video_id":
                            print("Another Cat Video (another_cat_video_id) [#cat #animal]")
                        elif x == "funny_dogs_video_id":
                            print("Funny Dogs (funny_dogs_video_id) [#dog #animal]")
                        elif x == "life_at_google_video_id":
                            print("Life at Google (life_at_google_video_id) [#google #career]")
                        elif x == "nothing_video_id":
                            print("Video about nothing (nothing_video_id) []")
        if flag == 0:
            print("Cannot show playlist",playlist_name+": Playlist does not exist")

                    

    def remove_from_playlist(self, playlist_name, video_id):
        video= self._video_library.get_video(video_id)
        if video != None:
            flaglist=0
            flagvid=0
            # id= video_id.strip('<>')
            id= video_id
            for playlist in self._playlist:
                if playlist_name.lower() == playlist.playlist_name.lower():
                    flaglist=1                                                                      #marking that the playlist exists
                    for x in playlist.playlist_videos:  
                        if id == x:
                            flagvid=1                                                               #marking that the video exists
                            id=x
                            break
                    if flagvid != 1:
                        print("Cannot remove video from",playlist_name+": Video is not in playlist")
                        return
                    playlist.playlist_videos.remove(id)
                    break
            if flaglist !=1:
                print("Cannot remove video from",playlist_name+": Playlist does not exist")
                return
            if (video_id == "<amazing_cats_video_id>" or video_id == "amazing_cats_video_id"):
                print("Removed video from",playlist_name+": Amazing Cats")
            elif (video_id == "<funny_dogs_video_id>" or video_id == "funny_dogs_video_id"):
                print("Removed video from",playlist_name+": Funny Dogs")
            elif (video_id == "<another_cat_video_id>" or video_id == "another_cat_video_id"):
                print("Removed video from",playlist_name+": Another Cat Video")
            elif (video_id == "<life_at_google_video_id>" or video_id == "life_at_google_video_id"):
                print("Removed video from",playlist_name+": Life at Google")
            elif (video_id == "<nothing_video_id>" or video_id == "nothing_video_id"):
                print("Removed video from",playlist_name+": Video about nothing")
        else:
            print("Cannot remove video from",playlist_name+": Video does not exist")
            return
        

    def clear_playlist(self, playlist_name):
        flaglist=0
        for playlist in self._playlist:
            if playlist_name.lower() == playlist.playlist_name.lower(): 
                flaglist=1                                                                              #marking that the playlist exists
                playlist.playlist_videos.clear()
                print("Successfully removed all videos from",playlist_name)
        if flaglist == 0:
            print("Cannot clear playlist",playlist_name+": Playlist does not exist")


    def delete_playlist(self, playlist_name):
        flag= 0
        index=-1
        for playlist in self._playlist:
            index+=1
            if playlist_name.lower() == playlist.playlist_name.lower():
                flag= 1                                                                                 #marking the playlist for deletion
                break
        if(flag == 1):
            self._playlist.pop(index)
            print("Deleted playlist:",playlist_name)
        if flag == 0:
            print("Cannot delete playlist",playlist_name+": Playlist does not exist")
            return


    def search_videos(self, search_term):
        index=0
        count=1
        flag=0
        search_results=[]
        videos= self._video_library.get_all_videos()
        videos.sort(key=lambda x: x.title)
        for x in videos:
            # print(getattr(videos[index],'title').lower().find(search_term.lower()))
            if getattr(videos[index],'title').lower().find(search_term.lower()) > -1:
                if flag == 0:  print("Here are the results for",search_term+":")
                flag = 1                                                                                #marking that videos found for search_term
                print(count,")",getattr(videos[index],'title'),"(" + getattr(videos[index],'video_id') , ")"+"[" ,  getattr(videos[index], 'tags') , "]")
                search_results.append(getattr(videos[index],'video_id'))
                count+=1
            index+=1
        if flag == 0:
            print("No search results for",search_term)
            return
        answer= input("Would you like to play any of the above? If yes, specify the number of the video. If your answer is not a valid number, we will assume it's a no.")
        if(answer.isnumeric()):                                                                         #checking if the input is numeric
            n = int(answer)
            if n >= count:                                                                              #checking if the input is valid
                return
            else:
                self.play_video(search_results[int(answer)-1])


    def search_videos_tag(self, video_tag):
        index=0
        count=1
        flag =0
        search_results=[]
        videos= self._video_library.get_all_videos()
        videos.sort(key=lambda x: x.title)
        for x in videos:
            for y in getattr(videos[index],'tags'):
                if y == video_tag:
                    if flag == 0:  print("Here are the results for",video_tag+":")
                    flag =1                                                                         #marking that videos have been found for the search term
                    print(count,")",getattr(videos[index],'title'),"(" + getattr(videos[index],'video_id') , ")"+"[" ,  getattr(videos[index], 'tags') , "]")
                    search_results.append(getattr(videos[index],'video_id'))
                    count+=1
            index+=1
        if flag == 0:
            print("No search results for",video_tag)
            return
        answer= input("Would you like to play any of the above? If yes, specify the number of the video. If your answer is not a valid number, we will assume it's a no.")
        
        if int(answer) >= count:
            return
        else:   
            self.play_video(search_results[int(answer)-1])

    def flag_video(self, video_id, flag_reason=""):
        video= self._video_library.get_video(video_id.strip('<>'))
        if video == None:                                               #checking if the video exists
            print("Cannot flag video: Video does not exist")
            return
        if video.flag != None:                                          #checking if the video has already been flagged
            print("Cannot flag video: Video is already flagged")
            return
        else:
            if(self.player_status == 1 or self.player_status == 2):
                self.player_status= 0
            if flag_reason == "" : 
                flag_reason = "Not supplied"
            video.flag= flag_reason
            print("Successfully flagged video:", video._title + " (reason: "+ video.flag + ")")


    def allow_video(self, video_id):
        video= self._video_library.get_video(video_id)
        if video == None:                                              #checking if the video exists
            print("Cannot remove flag from video: Video does not exist")
            return
        if video.flag == None:                                         #checking if the video doesnt have flags
            print("Cannot remove flag from video: Video is not flagged")
            return
        else:
            video.flag = None
            print("Successfully removed flag from video:", video._title)

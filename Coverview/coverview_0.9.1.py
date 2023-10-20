#!/bin/python
import os
import io
from mpd import MPDClient, CommandError
import pixcat
from pixcat import Image as PixImage
import time
from PIL import Image, ImageDraw
import math
from pathlib import Path
import termios
import tty
import signal
from signal import SIGUSR1
import sys
import threading
import mutagen.id3
import mutagen.flac
import mutagen.mp4

RESOLUTION = "500, 500"
MPDHOST = "localhost"
MPDPORT = "6600"
MPDPASS = False
music_library = "/path/to/mpd/music/library"
cover_formats = ["cover.jpg", "folder.jpg", "folder.png", "folder.jpeg", "cover.jpeg", "cover.png"]

 # Album art location
album_art_loc = "/location/of/coverview/.aartminip.png"
# Album art placeholder location
placeholder_loc = "/location/of/coverview/.placeholder.png"

      
class Exceptor: 
      #tracks failed attempts at loading artwork, loads fallback after 3 times!   
   def __init__(self):
      self.exception_no = 1
   
   def exception_counter(self):
      
       if self.exception_no <= 3:    
          print("failed retrieving artwork, retrying 3 times")
          print(self.exception_no)
          time.sleep(1)
          self.exception_no+=1
          fetcher.getAlbumArt(tracker.current_song["file"], tracker.client)
          
          
       else:
          print("third try, fallback")
          time.sleep(1)
          os.system('clear')
          executor.drawDefaultAlbumArt()
          tracker.client.idle("player")
          self.exception_no = 1
          executor.loop()
       


class Fetcher:
    """
    responsible for fetching artwork from currently playing song
    """
    
       
    def find_album_cover(self, album_dir_list, cover_formats):
       """
       Searches Through album directory for defined coverfiles
       """
       try:
         for item in album_dir_list:
           file_name = item['file']
           if file_name in cover_formats:
              return file_name
         return None
       except KeyError:
         return None
    
    def mutagen_fetcher(self, song_path):
       """
       mutagen proved to be way faster than fetching through python_mpd2, especially with larger artworks
       cycles through mp3 flac and mp4 
       """
       try:
           id3 = mutagen.id3.ID3(song_path)
           self.imginterpret = 2
           return id3.getall('APIC')[0].data
       except mutagen.id3.ID3NoHeaderError:
           try:
              flac = mutagen.flac.FLAC(song_path)
              self.imginterpret = 2
              return flac.pictures[0].data
           except mutagen.flac.FLACNoHeaderError:
              
              try:
                 mp4 = mutagen.mp4.MP4(song_path)
                 self.imginterpret = 2
                 return mp4['covr'][0]
              except:
                 self.imginterpret = 3
                 print("mutagen fail")
                 return None
          
    
    def getAlbumArt(self, song_file, mpd_client):
        """
        A function that fetches the album art and saves
        it to self.album_art_loc
        """
        self.success =False
        self.placeholder=placeholder_loc
       
        img = Image.open(self.placeholder)                                
        img.thumbnail((500, 500))                
        img.save(album_art_loc, "PNG")
        
        try:
           #checks first for any folder files in album directory, since this is often the best quality file, and convenient as an ovverride.        
           album_directory = os.path.dirname(song_file)
          
           #list of files in album directory        
           album_dir_list = tracker.client.listfiles(album_directory)
        
           #check if file matching coverfile exist
           cover_file = self.find_album_cover(album_dir_list, cover_formats)
          
           
           
           if cover_file is not None:
               #path for cover file if found:
               
               albumart_data = music_library+album_directory+"/"+cover_file
               #tell interpreter to expect image file
               self.imginterpret = 1 
           
           else:               
               #
               song_path = music_library+song_file
               albumart_data = self.mutagen_fetcher(song_path)
          
          
           if not albumart_data:  
             
             try:
                albumart_data = tracker.client.readpicture(song_file)
                #tell interpreter to expect binary
                self.imginterpret = 3              
             except CommandError:
                exception_counter
                     
                  # If readpicture fails, try mpd's albumart function
          
           elif not albumart_data: 
              try:
                  
                  albumart_data = tracker.client.albumart(song_file)
                  #last resort, never seen it actually work
                  self.imginterpret = 3

              except CommandError:
                 # If this also fails, just draw fallback image
                  exceptor.exception_counter()
           
       
           try:   
             """
             Image interpreter: 1 for coverfile in directory
             			2 for mutagen
             			else is binary from mpd
             """
             
             if self.imginterpret == 1:
                img = Image.open(albumart_data)                                
                img.thumbnail((500, 500))                
                img.save(album_art_loc, "PNG")
                self.success = True
             
             elif self.imginterpret == 2:   
                  with io.BytesIO(albumart_data) as f:
                       img = Image.open(f)                                     
                       img.thumbnail((500, 500))
                       # Save the image as a png file
                       img.save(album_art_loc, "PNG")
                       self.success = True
             else:
                with io.BytesIO(albumart_data["binary"]) as f:
                     img = Image.open(f)                                     
                     img.thumbnail((500, 500))
                     # Save the image as a png file
                     img.save(album_art_loc, "PNG")
                     self.success = True
                     
           except:
             print("failure retrieving album art")
             time.sleep(1)
             exceptor.exception_counter()
          
          
                        
        except:
             exceptor.exception_counter()

class Tracker:
    """tracks song information and player status changes from mpd"""

    def __init__(self):
        
        # MPD init
        self.client = MPDClient()
        self.client.connect(MPDHOST, MPDPORT)
        if MPDPASS:
            self.client.password(MPDPASS)
        self.current_song = None
        self.last_song = None
        self.last_album = None
        # Album art only flag       
       
        self.control_cycle = 0
    
        
       
            

    def getSongInfo(self, song):
        """
        A function that returns a tuple of the given songs
        album, artist, title
        if they do not exist, the function will return
        "", "", filename respectively
        """
        try:
            album = song["album"]
        except KeyError:
            album = ""

        try:
            artist = song["artist"]
        except KeyError:
            artist = ""

        if type(artist) is list:
            artist = ", ".join(artist)

        try:
            title = song["title"]
        except KeyError:
            # If no title, use base file name
            aux = song["file"]
            aux = os.path.basename(aux)
            title = aux

        return album, artist, title
    
    
    
    
    def checkSongUpdate(self):
        """
        Checks if there is a new song playing
        Returns:
            3 -- if song state is "stop"
            2 -- if theres no song change
            1 -- if there is song change, but no change in album
            0 -- if there is a new song and change in album
            
        """
        status = self.client.status()

        if status["state"] == "stop":
           
            return 3
        self.current_song = self.client.currentsong()
        self.current_album = self.getSongInfo(self.current_song)[0]
      
        if self.last_song != self.current_song:
                       
            if self.control_cycle == 0:           

               self.album, self.artist, self.title = self.getSongInfo(self.current_song)
            
            if self.last_album != self.current_album:
               self.last_song = self.current_song
               self.last_album =self.current_album
               return 0
            else: 
               self.last_song = self.current_song              
               return 1
        else:
            return 2        



class Executor: 
    """Main program loop, draws album art. runs through actions, idles until player change from mpd, through mpd.ifdle function"""
                    
    
    def songUpdateOptions(self, song_state):
                           
        if song_state == 0:
           
           os.system('clear')
           fetcher.getAlbumArt(tracker.current_song["file"], tracker.client)           
           self.last_album = tracker.current_album               
           
           if fetcher.success == True:          
              
              self.drawAlbumArt()
           
           else:
              
              self.drawDefaultAlbumArt()           
        elif song_state == 1 or song_state == 2:           
           
           os.system('clear')
           self.drawAlbumArt()
        
        else:
           
           os.system('clear')
           self.drawDefaultAlbumArt()
         
            
    def drawAlbumArt(self):
        """
        draw the album art
        """
        try:
            PixImage(album_art_loc).fit_screen(enlarge=True).show()
             
        except:
            print ("failure rendering image")
            exception_counter()
            
    def drawDefaultAlbumArt(self):
        
        try:
            PixImage(placeholder_loc).fit_screen(enlarge=True).show()
            
        except:
            print ("mistakes were made, exiting")
            time.sleep(6)
            # Enable input stream and exit somewhatgracefully
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.exit(0)
    
    def loop(self):
            
        # Disable input stream
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        os.system('setterm -cursor off')
        
        try:
             while True:
                #time.sleep(0.100)
                song_state = tracker.checkSongUpdate()
                self.songUpdateOptions(song_state)
                tracker.client.idle("player")
                continue
        except KeyboardInterrupt:
             # Enable input stream and exit gracefully on keyboard interrupt
             termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
             sys.exit(0)
           


try:
    tracker = Tracker()    
    exceptor =Exceptor() 
    fetcher = Fetcher()
    executor = Executor()    
    executor.loop()


except ConnectionRefusedError:
    print(f"Could not connect to mpd on {MPDHOST}:{MPDPORT}")


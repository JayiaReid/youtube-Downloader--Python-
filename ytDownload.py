#This is a python program that allows the user to download a video, audio as a single 
# or allow for the creation of playlists from youtube by entering the url

import os #library to access downloads folder
from pytube import YouTube #library to access youtube video
from moviepy.editor import VideoFileClip #video converter
from pytube import Playlist #dealing with playlists

#modules for downloading video(s)
def downloadVideo(url, outputDir):
    yt = YouTube(url)
    print(f"Title: {yt.title}") #get title of video
    print(f'downloading {yt.title}...')
    
    yd = yt.streams.get_highest_resolution()  #getting in highest resolution
    
    videoFilePath = yd.download(output_path=outputDir)
    print("Video download complete:", videoFilePath)
    return videoFilePath

def downloadPlaylist(url, outputDir, playlistName=None):
    playlist = Playlist(url)
    
    # Use playlist title if no custom name is provided
    if not playlistName:
        playlistName = playlist.title

    playlistDir = os.path.join(outputDir, playlistName)

    if not os.path.exists(playlistDir):
        os.makedirs(playlistDir)

    print(f"Downloading playlist: {playlistName}...")

    for video in playlist.videos:
        video.streams.first().download(output_path=playlistDir)

    print("Playlist download complete: ", playlistDir)
    return playlistDir


#module for downloading audio(s)
def downloadAudio(videoFilePath):
    video = VideoFileClip(videoFilePath)
    audioFilePath = os.path.splitext(videoFilePath)[0] + '.mp3'
    video.audio.write_audiofile(audioFilePath)
    print("Audio conversion complete:", audioFilePath)
    return audioFilePath

def downloadPlaylistAudio(url, outputDir, playlistName=None):
    playlist = Playlist(url)
    
    # Use playlist title if no custom name is provided
    if not playlistName:
        playlistName = playlist.title

    playlistDir = os.path.join(outputDir, playlistName)

    if not os.path.exists(playlistDir):
        os.makedirs(playlistDir)

    print(f"Downloading playlist: {playlistName}...")

    audioPaths = []  # List to store paths of downloaded audio files

    for video in playlist.videos:
        videoFilePath = video.streams.first().download(output_path=playlistDir)
        audioFilePath = downloadAudio(videoFilePath, playlistDir)
        audioPaths.append(audioFilePath)
        os.remove(videoFilePath) #removes video after audio conversion

    print("Playlist audio conversion complete: ", playlistDir)
    return audioPaths, playlistDir


#main
try:
    downloadTypeChoice = input("Would you like to download (S)just a video or (P)playlist?").lower() #is it going to be just a video or a playlist?
    fileTypeChoice = input("Do you want to download (V)video or (A)audio ").lower() #video or audio?
    url = input("Enter the YouTube URL: ")
    
    downloadsDir = os.path.join(os.path.expanduser('~'), 'Downloads')
    youtubeDownloadsDir = os.path.join(downloadsDir, 'Youtube Downloads')
    
    if not os.path.exists(youtubeDownloadsDir):
        os.makedirs(youtubeDownloadsDir) #if folder does not exist make it

    if fileTypeChoice == 'v':
        if downloadTypeChoice == 's':
            downloadVideo(url, youtubeDownloadsDir)
        elif downloadTypeChoice == 'p':
            playlistName = input("Enter the name for the playlist or press Enter to keep the title: ")
            downloadPlaylist(url, youtubeDownloadsDir, playlistName)
        else:
            print("Invalid choice for download type. Please choose either S or P.")            
    elif fileTypeChoice == 'a':
        videoFilePath = downloadVideo(url, youtubeDownloadsDir)
        downloadAudio(videoFilePath)
        os.remove(videoFilePath) #removes video after audio is downloaded
    elif fileTypeChoice == 'b':
        videoFilePath = downloadVideo(url, youtubeDownloadsDir)
        downloadAudio(videoFilePath)
    else:
        print("Invalid choice. Please choose either V, A, or B.")
except Exception as e:
    print("An error occurred:", str(e)) #error handling

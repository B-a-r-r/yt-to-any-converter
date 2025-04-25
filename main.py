from __future__ import unicode_literals
from pytubefix import Playlist, YouTube
from pytubefix.exceptions import RegexMatchError
from sys import exit
import re
from os import path, makedirs
    
def is_playlist_empty(playlist: Playlist) -> bool:
    return len(playlist.video_urls) == 0

def download_video(url: str | YouTube, extension: str, location: str) -> None:
    try:
        path.exists(location) or makedirs(location)
        
        video = YouTube(url).streams
        if extension == 'mp3':
            video = video.filter(only_audio=extension == 'mp3').first()
        else:
            video = video.first()
        
        filename = f"{video.title}.{extension}"
        
        video.download(
            output_path= location, 
            filename= filename,
            skip_existing= True,
        )
            
        print(f"Téléchargée: {filename}.{extension} OK!")
            
    except Exception as e:
        print(f"Erreur lors du téléchargement de {url}: {e}")
        raise
        
def run():
    url = ''
    tentatives = 0 #nombre d'erreurs limitées
    while url == '' and tentatives < 5:
        url = input ("Entrez le lien de la vidéo, du son, ou de la playlist YouTube: ")
        if url == '':
            print("Vous devez spécifier un lien.")
            continue
        tentatives += 1
    if tentatives == 5:
        print("Trop de tentatives, le programme va s'arrêter.")
        exit(1)
    
    extension = input("Entrez l'extension de sortie souhaité (mp4, mp3, ou gif) [mp3 par défaut]: ")
    if extension == '':
        extension = 'mp3'
        print("Extension par défaut mp3 utilisée.")
    
    location = input("Entrez le chemin de destination [le dossier 'yt_downloads' est créé et/ou utilisé par défaut]: ")
    if location == '':
        location = './yt_downloads'
        print("Dossier par défaut 'yt_downloads' utilisé.")

    downloads_count = 0
    try:
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        
        for video in playlist.videos:
            try:
                download_video(video.watch_url, extension, location)
                downloads_count += 1
                
            except Exception as e:
                print(f"Erreur lors du téléchargement: {e}")
                continue
            
    except (RegexMatchError, KeyError) as e:
        try:
            download_video(url, extension, location)
            downloads_count += 1
            
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url}: {e}")
            exit(1)
    
    finally:  
        print(f"Total téléchargements: {downloads_count}")
        

if __name__=='__main__':
    run()


from __future__ import unicode_literals
from pytubefix import Playlist, YouTube
from pytubefix.exceptions import RegexMatchError
from sys import exit
import re
from os import path, makedirs
import subprocess

def reencode_video(input_path: str) -> None:
    command = [
        'ffmpeg',
        '-i', "0000.mp3",
        '-c:v', 'libx264',
        '-crf', '18',
        '-preset', 'slow',
        '-c:a', 'aac',
        input_path
    ]
    
    try:
        subprocess.run(command, check=True)
        
        print(f"Vidéo ré-encodée avec succès : {input_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du ré-encodage de la vidéo : {e}")
        exit(1)
    
def is_playlist_empty(playlist: Playlist) -> bool:
    return len(playlist.video_urls) == 0

def download_video(url: str | YouTube, extension: str, location: str) -> None:
    try:
        to_reencode = False
        path.exists(path.join(location)) or makedirs(path.join(location))
        
        video = YouTube(url).streams
        # print(video.filter(type='audio'))
        if extension == 'mp3':
            video = video.filter(type='audio', mime_type="audio/webm").first()
            
            # print("\n")
            # print(video.__str__())
                
        elif extension == 'mp4':
            video = video.get_highest_resolution()
                
        else:
            video = video.filter(progressive=True).order_by('resolution').desc().first()
        
        filename = f"{video.title.replace(' ', '_').replace('.', '_')}.{extension}"
        
        video.download(
            output_path= path.join(location), 
            filename= filename,
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
        location = 'yt_downloads'
        print("Dossier par défaut 'yt_downloads' utilisé.")

    print(f"\nLancement du téléchargement de {url} vers {location} au format {extension}.")
    
    downloads_count = 0
    try:
        playlist = Playlist(url)
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        
        i = 1
        for video in playlist.videos:
            print(f"\n[{i}]---------------------")
            try:
                download_video(video.watch_url, extension, location)
                downloads_count += 1
                
            except Exception as e:
                print(f"Erreur lors du téléchargement: {e}")
                continue
            
            finally:
                i += 1
            
    except (RegexMatchError, KeyError) as e:
        print("\n---------------------")
        try:
            download_video(url, extension, location)
            downloads_count += 1
            
        except Exception as e:
            print(f"Erreur lors du téléchargement de {url}: {e}")
            exit(1)
    
    finally:  
        print(f"\nTotal téléchargements: {downloads_count}")
        

if __name__=='__main__':
    run()


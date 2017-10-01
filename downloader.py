import multiprocessing
import time
import youtube_dl
import os, sys

TIMEOUT_DURATION = 1800

def get_links( file_path ):
    file = open( file_path, 'r')
    urls = file.read()
    urls = urls.split('\n')
    return urls

def download_video( link ):
    options = {'format' : 'hls-1361'}
    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([link])

def run(file_path):
    urls = get_links( file_path )
    incomplete = []
    for url in urls:
        if url == '':
            continue
        downloader = multiprocessing.Process(target=download_video, args=(url,))
        downloader.start()
        downloader.join( TIMEOUT_DURATION )
        if downloader.is_alive:
            downloader.terminate()
            downloader.join()
            incomplete.append(url)
    print("Incomplete downloads: ")
    print(incomplete)

if __name__ == "__main__":
    run(sys.argv[1])

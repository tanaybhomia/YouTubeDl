# Main program

import os
import requests
import locale
from pytube import YouTube
from tqdm import tqdm
import re

# Introduction 
print("")
print(r""" 
     
.,+*??%%%%%%%%%%%%%%%%%%??*+,.       /$$     /$$                    /$$               /$$                       /$$$$$$$  /$$
,%%%%%%%%%%%%%%%%%%%%%%%%%%%?,      |  $$   /$$/                   | $$              | $$                      | $$__  $$| $$              
+%%%%%%%%%%%%%%%%%%%%%%%%%%%%;       \  $$ /$$//$$$$$$  /$$   /$$ /$$$$$$   /$$   /$$| $$$$$$$   /$$$$$$       | $$  \ $$| $$               
*%%%%%%%%%%%::+?%%%%%%%%%%%%%*        \  $$$$//$$__  $$| $$  | $$|_  $$_/  | $$  | $$| $$__  $$ /$$__  $$      | $$  | $$| $$              
?%%%%%%%%%%%,...,;*%%%%%%%%%%?         \  $$/| $$  \ $$| $$  | $$  | $$    | $$  | $$| $$  \ $$| $$$$$$$$      | $$  | $$| $$     
?%%%%%%%%%%%,...,;*%%%%%%%%%%?          | $$ | $$  | $$| $$  | $$  | $$ /$$| $$  | $$| $$  | $$| $$_____/      | $$  | $$| $$        
*%%%%%%%%%%%::+?%%%%%%%%%%%%%*          | $$ |  $$$$$$/|  $$$$$$/  |  $$$$/|  $$$$$$/| $$$$$$$/|  $$$$$$$      | $$$$$$$/| $$$$$$$$ 
+%%%%%%%%%%%%%%%%%%%%%%%%%%%%;          |__/  \______/  \______/    \___/   \______/ |_______/  \_______/      |_______/ |________/    
.,+*??%%%%%%%%%%%%%%%%%%??*+,.                                         

 """)

print("")
print("Welcome to YouTubeDl :)")
print("Download Any YouTube Video . . .")
print("")

DOWNLOADS_DIR =  downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads","Youtube_Downloads") # Specify the download directory

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    return re.sub(r'[\\/:*?"<>|]', '_', filename)

def download_video(url):

    locale.setlocale(locale.LC_NUMERIC, 'en_IN')
    video = YouTube(url)
    views = locale.format_string("%d", video.views, grouping=True)

    print("")
    print("Video Info :")
    print("")
    print("Title: ", video.title)
    print("Video by: ", video.author)
    print("Views: ", views)
    print("")

    print("Checking / Downloading . . .")
    print("")

    yd = video.streams.get_highest_resolution()
    video_url = yd.url
    
    # Get the total file size in bytes
    response = requests.get(video_url, stream=True)
    total_size = int(response.headers.get("Content-Length"))
    
	# Define the progress bar
    progress_bar = tqdm(total=total_size, unit='bytes', unit_scale=True)

    # Create the downloads directory if it doesn't exist
    if not os.path.exists(DOWNLOADS_DIR):
        os.makedirs(DOWNLOADS_DIR)

    # Generate the filename based on the video title
    filename = video.title + '.mp4'

    # Sanitize the filename
    filename = sanitize_filename(filename)
    
	# Replace invalid characters in the filename
    filename = filename.replace('/', '_')
    filename = filename.replace('|','_')

    # Check if the file already exists
    filepath = os.path.join(DOWNLOADS_DIR, filename)
    if os.path.exists(filepath):
        print("Video already exists at:")
        print(filepath)
        print("")
        while True:
            new_url = input("Enter another YouTube video link (or 'q' to quit): ")
            if new_url.lower() == 'q':
                return
            download_video(new_url)
            return
    else:
        # Download the video in chunks and update the progress bar
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    progress_bar.update(len(chunk))

        # Close the progress bar
        progress_bar.close()

        print("")
        print("Download Complete")
        print("The video is saved in the following directory:")
        print(filepath)
        print("")

# Entry point of the program
if __name__ == '__main__':
    while True:
        url = input("Enter the YouTube video link (or 'q' to quit): ")
        if url.lower() == 'q':
            break
        download_video(url)

print("Exiting YouTubeDl. . .")

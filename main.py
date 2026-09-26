import yt_dlp
import os
import json
import datetime
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Scopes for YouTube API (Upload videos)
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def download_tiktok_profile(username):
    print(f"Downloading videos from TikTok profile: {username}")
    os.makedirs('downloads', exist_ok=True)
    
    import subprocess
    import sys
    
    command = [
        sys.executable, "-m", "yt_dlp",
        f"https://www.tiktok.com/@{username}",
        "--impersonate", "chrome",
        "-o", "downloads/%(id)s.%(ext)s",
        "--write-info-json",
        "--ignore-errors"
    ]
    
    print("Running yt-dlp downloader...")
    subprocess.run(command)
    print("Download complete.")

def authenticate_youtube():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                print("ERROR: credentials.json is missing.")
                print("Please create a Google Cloud Project, enable YouTube Data API v3, and download the OAuth 2.0 Client ID as credentials.json")
                return None
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('youtube', 'v3', credentials=creds)

def schedule_uploads(youtube):
    if not os.path.exists('downloads'):
        print("No downloads folder found.")
        return

    # Load history to avoid duplicate uploads
    history_file = 'history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
    else:
        history = []

    # Get list of info json files
    files = os.listdir('downloads')
    json_files = [f for f in files if f.endswith('.info.json')]
    
    # Calculate starting date (tomorrow 9:30 AM)
    start_date = datetime.datetime.now() + datetime.timedelta(days=1)
    start_date = start_date.replace(hour=9, minute=30, second=0, microsecond=0)
    
    days_added = 0

    for json_file in json_files:
        video_id = json_file.replace('.info.json', '')
        if video_id in history:
            print(f"Skipping {video_id} (already uploaded)")
            continue
            
        with open(f"downloads/{json_file}", 'r', encoding='utf-8') as f:
            info = json.load(f)
            
        title = info.get('title', 'TikTok Video')
        description = info.get('description', '')
        ext = info.get('ext', 'mp4')
        
        video_path = f"downloads/{video_id}.{ext}"
        if not os.path.exists(video_path):
            print(f"Video file {video_path} not found.")
            continue
            
        # Add #Shorts to title or description
        if '#Shorts' not in title and '#shorts' not in title:
            description += "\n\n#Shorts #TikTok"
            
        # Calculate publish date for this video
        publish_time = start_date + datetime.timedelta(days=days_added)
        publish_time_iso = publish_time.isoformat() + 'Z'
        
        print(f"Uploading {video_id} - Scheduled for {publish_time_iso}")
        
        try:
            body = {
                'snippet': {
                    'title': title[:100], # YouTube title limit is 100
                    'description': description,
                    'tags': ['Shorts', 'TikTok']
                },
                'status': {
                    'privacyStatus': 'private',
                    'publishAt': publish_time_iso,
                    'selfDeclaredMadeForKids': False
                }
            }
            
            media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%")
            
            print(f"Upload complete! Video ID: {response['id']}")
            history.append(video_id)
            days_added += 1
            
        except Exception as e:
            print(f"Error uploading {video_id}: {e}")
            print("Note: If you get a quota error, you have reached the daily 6-video upload limit. Try again tomorrow.")
            break
            
    # Save history
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f)
        
    print(f"Finished processing. Scheduled {days_added} videos.")

if __name__ == '__main__':
    print("--- TikTok to YouTube Shorts Scheduler ---")
    username = input("Enter your TikTok username (without @) or leave empty to skip downloading: ")
    
    if username.strip():
        download_tiktok_profile(username.strip())
        
    print("\nStarting YouTube upload process...")
    youtube = authenticate_youtube()
    if youtube:
        schedule_uploads(youtube)

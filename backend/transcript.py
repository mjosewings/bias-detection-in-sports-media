#This file handles the comments for both NBA and WNBA videos
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

load_dotenv()  # Make sure .env is loaded

# Function to get video comments from YouTube API
def get_video_comments(video_id):
    API_KEY = os.getenv("YOUTUBE_API_KEY")
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    comments = []  # ✅ define the list before appending

    try:
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        )
        response = request.execute()

        while response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=response['nextPageToken'],
                    maxResults=100
                )
                response = request.execute()
            else:
                break

        return comments

    except Exception as e:
        print(f"[ERROR] Failed to fetch comments: {e}")
        return []

def save_comments(video_id, comments):
    filename = f'{video_id}_comments.txt'
    with open(filename, 'w', encoding='utf-8') as f:
        for c in comments:
            f.write(c + '\n')
    return filename

#This fule is responsible for fetching comments from a YouTube video using the YouTube Data API v3.
from googleapiclient.discovery import build
import os

API_KEY = os.getenv('YOUTUBE_API_KEY')

# Function to get video comments
def get_video_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    comments = []

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
            # Check if there are more comments to fetch
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

# Function to save comments to a file
def save_comments(video_id, comments):
    safe_title = f"{video_id}_comments.txt"
    with open(safe_title, 'w', encoding='utf-8') as f:
        for comment in comments:
            f.write(comment + "\n")
    return safe_title

# If running standalone for test
if __name__ == '__main__':
    test_id = 'dQw4w9WgXcQ'  # Replace with any test ID
    comments = get_video_comments(test_id)
    file_path = save_comments(test_id, comments)
    print(f"[INFO] Saved {len(comments)} comments to {file_path}")

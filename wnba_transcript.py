import os
from googleapiclient.discovery import build

# Your YouTube API key
API_KEY = 'AIzaSyAeeKtwWRG2emgFThexqfqHtNmGPP9cuYI'

# YouTube video ID (from the URL)
VIDEO_ID = 'AYn-yTHOBOY'  # Replace with your video ID

# Set up the YouTube API client
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_comments(video_id):
    comments = []
    try:
        # Get the first page of comments
        request = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText'
        )
        response = request.execute()

        # Loop through the comment threads and collect the comments
        while response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # If there's more than one page of comments, get the next page
            if 'nextPageToken' in response:
                request = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    pageToken=response['nextPageToken']
                )
                response = request.execute()
            else:
                break

        return comments

    except Exception as e:
        print(f"Error fetching comments: {e}")
        return None

def save_comments_to_file(comments, video_title):
    # Clean video title for filename
    clean_title = video_title.replace(' ', '_').replace('/', '_').replace('\\', '_')

    # Save comments to a .txt file
    with open(f"{clean_title}_comments.txt", 'w', encoding='utf-8') as file:
        for comment in comments:
            file.write(comment + "\n")

    print(f"Comments saved to {clean_title}_comments.txt")

# Get video details to fetch title
video_info = youtube.videos().list(part='snippet', id=VIDEO_ID).execute()
video_title = video_info['items'][0]['snippet']['title']

# Fetch comments for the video
comments = get_video_comments(VIDEO_ID)

# If comments were fetched, save them to a file
if comments:
    save_comments_to_file(comments, video_title)
else:
    print("No comments found or unable to fetch comments.")

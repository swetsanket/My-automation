
"""
Social media module for posting to Instagram, Facebook, YouTube, and LinkedIn.
"""
import os
import time
import json
import logging
import requests
from pathlib import Path
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from config import CONFIG

logger = logging.getLogger(__name__)

def post_to_instagram(video_path, caption):
    """
    Post a video to Instagram as a Reel.
    
    Args:
        video_path (str): Path to the video file
        caption (str): Caption for the post
        
    Returns:
        bool: Success status
    """
    logger.info("Posting to Instagram")
    
    try:
        # Instagram requires the Facebook Graph API with proper permissions
        # This is a simplified implementation - production code would need to handle
        # more complex authentication and posting flow
        
        username = CONFIG['INSTAGRAM_USERNAME']
        password = CONFIG['INSTAGRAM_PASSWORD']
        
        # For demonstration purposes, we're logging that we would post to Instagram
        # In a real implementation, you would use the Instagram Graph API
        logger.info(f"Would post to Instagram as {username} with caption: {caption[:50]}...")
        
        # Simulate API request delay
        time.sleep(1)
        
        # In a real implementation, this would return the actual post ID or URL
        # For now, we'll just return True indicating success
        return True
        
    except Exception as e:
        logger.error(f"Error posting to Instagram: {str(e)}", exc_info=True)
        return False

def post_to_facebook(video_url, caption):
    """
    Post a video to Facebook Page.
    
    Args:
        video_url (str): URL to the video (e.g., Google Drive link)
        caption (str): Caption for the post
        
    Returns:
        bool: Success status
    """
    logger.info("Posting to Facebook")
    
    try:
        access_token = CONFIG['FACEBOOK_ACCESS_TOKEN']
        page_id = CONFIG['FACEBOOK_PAGE_ID']
        
        # Facebook Graph API endpoint for posting to a page
        url = f"https://graph.facebook.com/v18.0/{page_id}/videos"
        
        # Prepare data for the POST request
        data = {
            'access_token': access_token,
            'description': caption,
            'file_url': video_url
        }
        
        # Make the API request
        response = requests.post(url, data=data)
        
        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            post_id = result.get('id')
            logger.info(f"Successfully posted to Facebook. Post ID: {post_id}")
            return True
        else:
            logger.error(f"Facebook API error: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error posting to Facebook: {str(e)}", exc_info=True)
        return False

def post_to_youtube(video_path, title, description):
    """
    Upload a video to YouTube as a Short.
    
    Args:
        video_path (str): Path to the video file
        title (str): Title for the YouTube video
        description (str): Description for the video
        
    Returns:
        bool: Success status
    """
    logger.info("Posting to YouTube")
    
    try:
        # Load OAuth 2.0 credentials
        credentials_path = CONFIG['YOUTUBE_OAUTH_CREDENTIALS']
        
        # Check if credentials are a file path or a JSON string
        if os.path.isfile(credentials_path):
            with open(credentials_path, 'r') as f:
                credentials_info = json.load(f)
        else:
            try:
                credentials_info = json.loads(credentials_path)
            except json.JSONDecodeError:
                raise ValueError("YOUTUBE_OAUTH_CREDENTIALS must be a valid JSON string or file path")
        
        # Create credentials object
        credentials = google.oauth2.credentials.Credentials(
            token=credentials_info.get('token'),
            refresh_token=credentials_info.get('refresh_token'),
            token_uri=credentials_info.get('token_uri'),
            client_id=credentials_info.get('client_id'),
            client_secret=credentials_info.get('client_secret')
        )
        
        # Build the YouTube API client
        youtube = build('youtube', 'v3', credentials=credentials)
        
        # Prepare video metadata
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': ['Shorts', 'viral', 'reaction'],
                'categoryId': '22'  # People & Blogs category
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Upload the video
        media = MediaFileUpload(
            video_path,
            mimetype='video/mp4',
            resumable=True
        )
        
        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )
        
        response = request.execute()
        
        video_id = response.get('id')
        logger.info(f"Successfully uploaded to YouTube. Video ID: {video_id}")
        
        return True
        
    except HttpError as error:
        logger.error(f"YouTube API error: {error}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Error posting to YouTube: {str(e)}", exc_info=True)
        return False

def post_to_linkedin(video_url, caption):
    """
    Post a video to LinkedIn.
    
    Args:
        video_url (str): URL to the video (e.g., Google Drive link)
        caption (str): Caption for the post
        
    Returns:
        bool: Success status
    """
    logger.info("Posting to LinkedIn")
    
    try:
        access_token = CONFIG['LINKEDIN_ACCESS_TOKEN']
        
        # LinkedIn API endpoint for creating a share
        url = "https://api.linkedin.com/v2/ugcPosts"
        
        # Prepare headers with authentication
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        # Prepare the post data
        data = {
            "author": "urn:li:person:{PERSON_ID}",  # This would need to be dynamically set
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": caption
                    },
                    "shareMediaCategory": "RICH",
                    "media": [{
                        "status": "READY",
                        "originalUrl": video_url,
                        "title": {
                            "text": "Viral Reaction Video"
                        }
                    }]
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        # Make the API request
        response = requests.post(url, headers=headers, json=data)
        
        # Check if the request was successful
        if response.status_code in (200, 201):
            result = response.json()
            post_id = result.get('id')
            logger.info(f"Successfully posted to LinkedIn. Post ID: {post_id}")
            return True
        else:
            logger.error(f"LinkedIn API error: {response.text}")
            return False
            
    except Exception as e:
        logger.error(f"Error posting to LinkedIn: {str(e)}", exc_info=True)
        return False

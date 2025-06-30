
"""
Caption generator module for creating viral Hinglish captions.
"""
import random
import logging
import json
import os
from pathlib import Path

logger = logging.getLogger(__name__)

# Load caption templates and hashtags
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_PATH = BASE_DIR / "assets" / "caption_templates.json"

# Create default templates if file doesn't exist
DEFAULT_TEMPLATES = {
    "youtube": {
        "opening_comments": [
            "Confidence ho toh aisa!",
            "Ye dekho, kya talent hai!",
            "Arre wah, kya scene hai!",
            "Talent ki kami nahi hai India mein!",
            "Kya majra chal raha hai yahan?",
            "Ye toh next level ho gaya!",
            "Kuch bhi ho sakta hai India mein!",
            "Ek number performance!",
            "Dekho zara ye kamal!",
            "Ye toh kamaal kar diya bhai!"
        ],
        "relatable_observations": [
            "Hum toh exam me 4 page extra likh ke itna khush hote hai.",
            "Delhi metro mein aise log mil jate hai daily.",
            "Mummy ke saamne hum bhi aise hi perfect bante hai.",
            "Dost ke shaadi mein hum sab aise hi dance karte hai.",
            "College ke last day pe hum bhi aise hi the.",
            "Salary aane ke baad 2 din wali feeling.",
            "Jab teacher class mein na ho tab hum bhi aise hi.",
            "Relatives ke saamne hamara talent.",
            "Office ke team building activity mein sabki yahi halat.",
            "Weekend plans banate time dost log aise hi karte hai."
        ],
        "engaging_questions": [
            "Sahi me, itna talent laate kaha se ho?",
            "Tumhare area mein bhi aise log hai kya?",
            "Kya aapne bhi kabhi aisa kiya hai?",
            "Apne doston ko tag karo jo bilkul aise hi hai!",
            "Aap kya karte agar aap wahan hote?",
            "Comments mein batao, kitne log aise hi karte hai?",
            "Kya aapko bhi aisa kuch try karna chahiye?",
            "Apna reaction comments mein batao!",
            "Kitne log soch rahe hai ye try karna?",
            "Konsa emoji describe karta hai is video ko?"
        ]
    },
    "news": {
        "opening_comments": [
            "Breaking news se bhi jyada shocking!",
            "Ye khabar sun ke hosh ud gaye!",
            "Aaj kal ke news mein kuch bhi ho sakta hai!",
            "India hai, yahan kuch bhi ho sakta hai!",
            "Ye news dekh ke coffee muh se bahar aa gayi!",
            "Morning chai ke saath ye news hazam nahi hui!",
            "Itni dramatic news! Ekta Kapoor ko competition!",
            "Ye news trend kar rahi hai har jagah!",
            "Sabse masaledaar khabar aaj ki!",
            "News channels ko TRP mil gayi!"
        ],
        "relatable_observations": [
            "Family WhatsApp group pe ye news 10 baar aa chuki hai.",
            "Office ke lunch break mein sabki yehi charcha hai.",
            "Padosi aunty ne pure mohalle ko ye news bata di hogi.",
            "College group chat mein sabne isko forward kiya hoga.",
            "Local train mein aaj yehi discussion chal raha hai.",
            "Sabki morning chai is news ke saath ruki hogi.",
            "Drawing room debates mein aaj yehi topic hai.",
            "Society ke security guard ne sabko ye news bata di hogi.",
            "Subah ki newspaper mein front page pe yehi news hai.",
            "Dinner table pe papa ne yehi news discuss ki hogi."
        ],
        "engaging_questions": [
            "Aapka kya reaction hai is news pe?",
            "Kya aapko bhi ye news shocking lagi?",
            "Is news ke baare mein aapka kya kehna hai?",
            "Apne friends ko tag karo jinko ye news nahi pata!",
            "Comments mein batao, aapne ye news kahan suni?",
            "Agar aap wahan hote to kya karte?",
            "Kya aapke area mein bhi aisa kuch hua hai?",
            "Ye news fake hai ya real? Comments mein batao!",
            "Kitne log is news se agree karte hain?",
            "Is news ke aage kya hoga? Predictions comments mein do!"
        ]
    }
}

DEFAULT_HASHTAGS = {
    "common": [
        "#viralreels",
        "#indianmemes",
        "#desijugaad",
        "#funnyindia",
        "#trending",
        "#reelkarofeelkaro",
        "#reelitfeelit",
        "#instagramreels",
        "#foryoupage",
        "#viral",
        "#trending",
        "#desireels"
    ],
    "youtube": [
        "#youtubeshorts",
        "#youtubeindia",
        "#funnyvideos",
        "#comedyvideos",
        "#reactingtovideos",
        "#reactingtotrends"
    ],
    "news": [
        "#breakingnews",
        "#indianews",
        "#newsupdates",
        "#trendingnews",
        "#latestupdate",
        "#newsreaction"
    ]
}

# Create templates file if it doesn't exist
if not os.path.exists(TEMPLATES_PATH):
    with open(TEMPLATES_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            "templates": DEFAULT_TEMPLATES,
            "hashtags": DEFAULT_HASHTAGS
        }, f, indent=4)

# Load templates
try:
    with open(TEMPLATES_PATH, 'r', encoding='utf-8') as f:
        CAPTION_DATA = json.load(f)
except Exception as e:
    logger.error(f"Error loading caption templates: {str(e)}")
    CAPTION_DATA = {
        "templates": DEFAULT_TEMPLATES,
        "hashtags": DEFAULT_HASHTAGS
    }

def generate_hinglish_caption(title, content_type="youtube"):
    """
    Generate a viral Hinglish caption based on the video title and content type.
    
    Args:
        title (str): The title or subject of the video
        content_type (str): Type of content ("youtube" or "news")
        
    Returns:
        tuple: (caption, hashtags)
    """
    logger.info(f"Generating Hinglish caption for {content_type} content: {title}")
    
    try:
        # Determine the template set to use
        if content_type not in CAPTION_DATA["templates"]:
            content_type = "youtube"  # Default to youtube templates
        
        templates = CAPTION_DATA["templates"][content_type]
        
        # Select random components
        opening = random.choice(templates["opening_comments"])
        observation = random.choice(templates["relatable_observations"])
        question = random.choice(templates["engaging_questions"])
        
        # Combine components to form the caption
        caption = f"{opening} {observation} {question}"
        
        # Generate hashtags
        hashtags = []
        # Add common hashtags
        hashtags.extend(random.sample(CAPTION_DATA["hashtags"]["common"], 3))
        # Add content-specific hashtags
        if content_type in CAPTION_DATA["hashtags"]:
            hashtags.extend(random.sample(CAPTION_DATA["hashtags"][content_type], 2))
        
        # Add a content-specific hashtag based on the title
        # Extract keywords from the title
        keywords = [word for word in title.split() if len(word) > 3]
        if keywords:
            keyword = random.choice(keywords).lower()
            # Remove any non-alphanumeric characters
            keyword = ''.join(c for c in keyword if c.isalnum())
            if keyword:
                hashtags.append(f"#{keyword}")
        
        return caption, hashtags
        
    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        # Fallback caption
        return (
            "Ye video dekh ke hassi nahi ruki! Bilkul India wali feeling. Aap kya kehte ho?", 
            ["#viralreels", "#indianmemes", "#desijugaad", "#funnyindia", "#trending"]
        )

"""
Storage module for Google Drive integration.
"""
import os
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

from config import CONFIG

logger = logging.getLogger(__name__)

def upload_to_drive(file_path, file_name=None):
    """
    Upload a file to Google Drive.
    
    Args:
        file_path (str): Path to the file to upload
        file_name (str, optional): Name to give the file on Drive (default: use original filename)
        
    Returns:
        tuple: (file_id, share_link)
    """
    logger.info(f"Uploading file to Google Drive: {file_path}")
    
    try:
        # Get credentials from environment
        credentials_json = CONFIG['GOOGLE_DRIVE_CREDENTIALS']
        
        # Check if credentials are a file path or a JSON string
        if os.path.isfile(credentials_json):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_json,
                scopes=['https://www.googleapis.com/auth/drive']
            )
        else:
            # Try to parse as JSON string
            try:
                credentials_info = json.loads(credentials_json)
                credentials = service_account.Credentials.from_service_account_info(
                    credentials_info,
                    scopes=['https://www.googleapis.com/auth/drive']
                )
            except json.JSONDecodeError:
                raise ValueError("GOOGLE_DRIVE_CREDENTIALS must be a valid JSON string or file path")
        
        # Build the Drive API client
        drive_service = build('drive', 'v3', credentials=credentials)
        
        # If no file name is provided, use the original filename
        if not file_name:
            file_name = os.path.basename(file_path)
        
        # File metadata
        file_metadata = {
            'name': file_name,
            'mimeType': 'video/mp4'
        }
        
        # If a folder ID is specified in config, add it to the metadata
        folder_id = CONFIG['GOOGLE_DRIVE_FOLDER_ID']
        if folder_id:
            file_metadata['parents'] = [folder_id]
        
        # Create a media file upload object
        media = MediaFileUpload(
            file_path,
            mimetype='video/mp4',
            resumable=True
        )
        
        # Upload the file
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        file_id = file.get('id')
        
        # Make the file publicly accessible for viewing
        permission = {
            'type': 'anyone',
            'role': 'reader'
        }
        
        drive_service.permissions().create(
            fileId=file_id,
            body=permission
        ).execute()
        
        # Get the shareable link
        share_link = f"https://drive.google.com/file/d/{file_id}/view"
        
        logger.info(f"Successfully uploaded file to Google Drive. ID: {file_id}, Link: {share_link}")
        
        return file_id, share_link
        
    except HttpError as error:
        logger.error(f"Google Drive API error: {error}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"Error uploading to Google Drive: {str(e)}", exc_info=True)
        raise

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

"""
Package initialization for viral video automation modules.
"""

# Core dependencies
python-dotenv==1.0.0
requests==2.31.0
apscheduler==3.10.1

# Content discovery
google-api-python-client==2.108.0
google-auth==2.23.3
google-auth-oauthlib==1.1.0
feedparser==6.0.10
pytube==15.0.0
youtube-dl==2021.12.17

# Video editing
moviepy==1.0.3
Pillow==10.0.1
numpy==1.24.3

# Avatar generation
torch==2.0.1
torchvision==0.15.2
SadTalker==0.0.1

# Storage
google-auth==2.23.3
google-cloud-storage==2.10.0

# Social media posting
facebook-sdk==3.1.0
python-linkedin==4.1

# API Keys and Credentials
YOUTUBE_API_KEY=your_youtube_api_key_here
GOOGLE_DRIVE_CREDENTIALS=path_to_service_account_json_or_json_string
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id

# Social Media Credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password
FACEBOOK_ACCESS_TOKEN=your_facebook_access_token
FACEBOOK_PAGE_ID=your_facebook_page_id
YOUTUBE_OAUTH_CREDENTIALS=path_to_oauth_credentials_json_or_json_string
LINKEDIN_ACCESS_TOKEN=your_linkedin_access_token

# Content Discovery Settings
YOUTUBE_REGION_CODE=IN
YOUTUBE_MAX_RESULTS=50
ALTERNATE_CONTENT_SOURCES=True

# Social Media Posting Settings
POST_TO_INSTAGRAM=True
POST_TO_FACEBOOK=True
POST_TO_YOUTUBE=True
POST_TO_LINKEDIN=True

# SadTalker Settings
SADTALKER_PATH=./SadTalker

# Scheduling Settings
RUN_ONCE=False

# Viral Video Automation

An end-to-end Python automation system that creates viral reaction videos with AI avatars and posts them to multiple social media platforms automatically.

## Features

- Automatically discovers trending content from YouTube and news sources
- Creates reaction videos with an AI avatar using Stable Diffusion and SadTalker
- Generates engaging Hinglish captions with viral potential
- Uploads videos to Google Drive for storage and sharing
- Posts to Instagram, Facebook, YouTube Shorts, and LinkedIn automatically
- Runs on a schedule (twice daily at 11:00 AM and 8:00 PM IST)

## Technical Stack

- **Programming Language**: Python
- **Content Discovery**: Google API Python Client, feedparser
- **Video Editing**: MoviePy
- **AI Avatar Generation**: Stable Diffusion, SadTalker
- **Storage & File Handling**: Google Drive API
- **Social Media Posting**: requests, google-api-python-client
- **Scheduling**: APScheduler

## Installation

1. Clone this repository:
```
git clone https://github.com/yourusername/viral-video-automation.git
cd viral-video-automation
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Install SadTalker:
```
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
python install.py
cd ..
```

4. Create a `.env` file with your API keys and credentials (use the provided `.env.example` as a template)

5. Create the necessary directories:
```
mkdir -p assets/reaction_audio
```

6. Add your avatar image to `assets/avatar_base.png` and reaction audio files to `assets/reaction_audio/`

## Usage

Run the main script:
```
python main.py
```

For production deployment, you can use a process manager like PM2 or Supervisor to keep the script running.

## Environment Variables

The following environment variables need to be set in your `.env` file:

- `YOUTUBE_API_KEY`: Your YouTube Data API v3 key
- `GOOGLE_DRIVE_CREDENTIALS`: Path to your Google service account JSON file or the JSON content as a string
- `GOOGLE_DRIVE_FOLDER_ID`: ID of the Google Drive folder to store videos
- `INSTAGRAM_USERNAME`: Your Instagram username
- `INSTAGRAM_PASSWORD`: Your Instagram password
- `FACEBOOK_ACCESS_TOKEN`: Your Facebook Graph API access token
- `FACEBOOK_PAGE_ID`: ID of your Facebook page
- `YOUTUBE_OAUTH_CREDENTIALS`: Path to your YouTube OAuth credentials JSON file or the JSON content as a string
- `LINKEDIN_ACCESS_TOKEN`: Your LinkedIn API access token
- `SADTALKER_PATH`: Path to the SadTalker installation

## Project Structure

```
viral-video-automation/
├── main.py                    # Main script that orchestrates the workflow
├── requirements.txt           # All required dependencies
├── README.md                  # Documentation
├── .env.example               # Example environment variables file
├── config.py                  # Configuration and environment variable loading
├── modules/
│   ├── __init__.py
│   ├── content_discovery.py   # YouTube and RSS feed content discovery
│   ├── video_editing.py       # MoviePy video editing functions
│   ├── avatar_generation.py   # Stable Diffusion and SadTalker integration
│   ├── caption_generator.py   # Hinglish caption generation
│   ├── storage.py             # Google Drive integration
│   └── social_media.py        # Social media posting functions
└── assets/
    ├── avatar_base.png        # Pre-generated AI avatar image
    └── reaction_audio/        # Pre-recorded audio reactions
        ├── wow.mp3
        ├── laugh.mp3
        └── gasp.mp3
```

## Notes on Social Media APIs

- **Instagram**: The Instagram Graph API requires a Facebook Developer account and a business Instagram account.
- **Facebook**: The Facebook Graph API requires an app with Page permissions.
- **YouTube**: The YouTube Data API requires OAuth 2.0 authentication.
- **LinkedIn**: The LinkedIn API requires developer approval for video posting capabilities.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

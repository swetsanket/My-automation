
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

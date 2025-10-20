"""
Personal Google Drive Service for OAuth2 Authentication
Handles personal Google account authentication for unlimited storage access
"""

import os
import pickle
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from loguru import logger

# Scopes for Google Drive and Sheets access
SCOPES = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.metadata.readonly'
]


class PersonalGoogleDriveService:
    """Personal Google Drive service with OAuth2 authentication."""
    
    def __init__(self, credentials_file: str = "personal_credentials.json", token_file: str = "personal_google_token.pickle"):
        """
        Initialize the personal Google Drive service.
        
        Args:
            credentials_file: Path to OAuth2 credentials JSON file
            token_file: Path to store/load OAuth2 token
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.credentials = None
        self.service = None
        
        # Initialize authentication
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google using OAuth2 flow."""
        try:
            # Check if credentials file exists
            if not os.path.exists(self.credentials_file):
                logger.error(f"❌ Credentials file not found: {self.credentials_file}")
                logger.info("📝 Please download OAuth2 credentials from Google Cloud Console")
                logger.info("📖 See: docs/PERSONAL_GOOGLE_SETUP.md for setup instructions")
                return
            
            # Load existing token if available
            if os.path.exists(self.token_file):
                try:
                    with open(self.token_file, 'rb') as token:
                        self.credentials = pickle.load(token)
                    logger.info("✅ Loaded existing OAuth2 token")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to load existing token: {e}")
                    self.credentials = None
            
            # If no valid credentials, start OAuth2 flow
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    # Try to refresh the token
                    try:
                        self.credentials.refresh(Request())
                        logger.info("✅ Refreshed OAuth2 token")
                    except Exception as e:
                        logger.warning(f"⚠️ Failed to refresh token: {e}")
                        self.credentials = None
                
                if not self.credentials:
                    # Start OAuth2 flow
                    logger.info("🔐 Starting OAuth2 authentication flow...")
                    logger.info("🌐 A browser window will open for Google authentication")
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_file, SCOPES
                    )
                    
                    # Run the OAuth2 flow
                    self.credentials = flow.run_local_server(port=0)
                    logger.info("✅ OAuth2 authentication completed")
                
                # Save the credentials for next time
                try:
                    with open(self.token_file, 'wb') as token:
                        pickle.dump(self.credentials, token)
                    logger.info(f"💾 Saved OAuth2 token to {self.token_file}")
                except Exception as e:
                    logger.warning(f"⚠️ Failed to save token: {e}")
            
            # Create the Google Drive service
            if self.credentials:
                self.service = build('drive', 'v3', credentials=self.credentials)
                logger.info("✅ Personal Google Drive service initialized successfully")
                logger.info("🎉 You now have unlimited 2TB storage access!")
            else:
                logger.error("❌ Failed to obtain valid credentials")
                self.service = None
                
        except Exception as e:
            logger.error(f"❌ Authentication failed: {str(e)}")
            logger.info("🔧 Troubleshooting steps:")
            logger.info("   1. Verify personal_credentials.json exists and is valid")
            logger.info("   2. Delete personal_google_token.pickle and try again")
            logger.info("   3. Check internet connection")
            logger.info("   4. See docs/PERSONAL_GOOGLE_SETUP.md for detailed setup")
            self.credentials = None
            self.service = None
    
    def is_authenticated(self) -> bool:
        """Check if the service is properly authenticated."""
        return self.credentials is not None and self.service is not None
    
    def get_service(self):
        """Get the Google Drive service instance."""
        return self.service
    
    def get_credentials(self):
        """Get the OAuth2 credentials."""
        return self.credentials
    
    def test_connection(self) -> Dict[str, Any]:
        """Test the Google Drive connection."""
        try:
            if not self.service:
                return {
                    "success": False,
                    "error": "Service not initialized",
                    "authenticated": False
                }
            
            # Try to get about information
            about = self.service.about().get(fields="user,storageQuota").execute()
            
            user_info = about.get('user', {})
            storage_quota = about.get('storageQuota', {})
            
            # Calculate storage usage
            used_bytes = int(storage_quota.get('usage', 0))
            total_bytes = int(storage_quota.get('limit', 0))
            
            used_gb = used_bytes / (1024**3) if used_bytes > 0 else 0
            total_gb = total_bytes / (1024**3) if total_bytes > 0 else 0
            
            return {
                "success": True,
                "authenticated": True,
                "user": {
                    "email": user_info.get('emailAddress', 'Unknown'),
                    "name": user_info.get('displayName', 'Unknown')
                },
                "storage": {
                    "used_gb": round(used_gb, 2),
                    "total_gb": round(total_gb, 2),
                    "unlimited": total_bytes == 0  # 0 means unlimited
                },
                "message": "Personal Google account connected successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "authenticated": False
            }
    
    def revoke_credentials(self):
        """Revoke the OAuth2 credentials and delete token file."""
        try:
            if self.credentials:
                self.credentials.revoke(Request())
                logger.info("✅ OAuth2 credentials revoked")
            
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
                logger.info(f"🗑️ Deleted token file: {self.token_file}")
            
            self.credentials = None
            self.service = None
            logger.info("🔄 Service reset - restart required for re-authentication")
            
        except Exception as e:
            logger.error(f"❌ Failed to revoke credentials: {e}")
    
    def get_quota_info(self) -> Dict[str, Any]:
        """Get detailed quota information."""
        try:
            if not self.service:
                return {"error": "Service not available"}
            
            about = self.service.about().get(fields="storageQuota").execute()
            quota = about.get('storageQuota', {})
            
            limit = int(quota.get('limit', 0)) if quota.get('limit') else 0
            usage = int(quota.get('usage', 0)) if quota.get('usage') else 0
            usage_in_drive = int(quota.get('usageInDrive', 0)) if quota.get('usageInDrive') else 0
            
            # Convert to GB
            limit_gb = limit / (1024**3) if limit > 0 else 0
            usage_gb = usage / (1024**3) if usage > 0 else 0
            usage_in_drive_gb = usage_in_drive / (1024**3) if usage_in_drive > 0 else 0
            
            # Calculate percentages
            usage_percentage = (usage_gb / limit_gb * 100) if limit_gb > 0 else 0
            drive_usage_percentage = (usage_in_drive_gb / limit_gb * 100) if limit_gb > 0 else 0
            
            return {
                "limit_gb": round(limit_gb, 2),
                "usage_gb": round(usage_gb, 2),
                "usage_in_drive_gb": round(usage_in_drive_gb, 2),
                "usage_percentage": round(usage_percentage, 2),
                "drive_usage_percentage": round(drive_usage_percentage, 2),
                "unlimited": limit == 0,
                "available_gb": round(limit_gb - usage_gb, 2) if limit_gb > 0 else "Unlimited"
            }
            
        except Exception as e:
            return {"error": str(e)}


# Convenience function for easy import
def get_personal_google_service() -> PersonalGoogleDriveService:
    """Get a PersonalGoogleDriveService instance."""
    return PersonalGoogleDriveService()


if __name__ == "__main__":
    # Test the service
    logger.info("🧪 Testing Personal Google Drive Service...")
    
    service = PersonalGoogleDriveService()
    
    if service.is_authenticated():
        logger.info("✅ Service initialized successfully")
        
        # Test connection
        result = service.test_connection()
        if result["success"]:
            logger.info(f"👤 User: {result['user']['email']}")
            logger.info(f"💾 Storage: {result['storage']['used_gb']:.2f} GB used")
            if result['storage']['unlimited']:
                logger.info("🎉 Unlimited storage available!")
            else:
                logger.info(f"📊 Total: {result['storage']['total_gb']:.2f} GB")
        else:
            logger.error(f"❌ Connection test failed: {result['error']}")
    else:
        logger.error("❌ Service initialization failed")
        logger.info("🔧 Please check your credentials and try again")

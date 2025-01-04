import requests
from typing import Optional, Dict
from app.core.config import settings

def authenticate_user(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate a user with username and password
    """
    try:
        response = requests.post(
            f"{settings.API_V1_STR}/auth/login",
            data={"username": username, "password": password}
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
        return None
    except Exception as e:
        print(f"Authentication error: {str(e)}")
        return None

def get_facebook_user(access_token: str) -> Optional[Dict]:
    """
    Get user information from Facebook using access token
    """
    try:
        response = requests.get(
            'https://graph.facebook.com/v12.0/me',
            params={
                'access_token': access_token,
                'fields': 'id,name,email'
            }
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
        return None
    except Exception as e:
        print(f"Facebook API error: {str(e)}")
        return None

def get_google_user(access_token: str) -> Optional[Dict]:
    """
    Get user information from Google using access token
    """
    try:
        response = requests.get(
            'https://www.googleapis.com/oauth2/v3/userinfo',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        if response.status_code == 200:
            data = response.json()
            if data:
                return data
        return None
    except Exception as e:
        print(f"Google API error: {str(e)}")
        return None

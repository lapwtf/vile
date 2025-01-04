import aiohttp
from bs4 import BeautifulSoup
import json
from typing import Optional, Dict, List, Union
import asyncio
import re

class RobloxAPI:
    def __init__(self):
        self._session = None
        self.base_url = "https://www.roblox.com"
        self.api_url = "https://api.roblox.com"
        
    @property
    def session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
        
    async def close(self):
        if self._session:
            await self._session.close()

    async def get_user_by_username(self, username: str) -> Optional[Dict]:
        try:
            async with self.session.get(f"{self.api_url}/users/get-by-username?username={username}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return None
        except:
            return None

    async def get_user_profile(self, user_id: int) -> Optional[Dict]:
        try:
            async with self.session.get(f"{self.base_url}/users/{user_id}/profile") as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    profile_data = {
                        'id': user_id,
                        'username': None,
                        'display_name': None,
                        'description': None,
                        'created': None,
                        'badges': [],
                        'friends': 0,
                        'followers': 0,
                        'following': 0,
                        'place_visits': 0
                    }
                    
                    header = soup.find('div', {'class': 'profile-header'})
                    if header:
                        profile_data['username'] = header.find('h2').text.strip() if header.find('h2') else None
                        profile_data['display_name'] = header.find('div', {'class': 'profile-display-name'}).text.strip() if header.find('div', {'class': 'profile-display-name'}) else None
                    
                    about = soup.find('span', {'class': 'profile-about-content-text'})
                    if about:
                        profile_data['description'] = about.text.strip()
                    
                    stats = soup.find_all('div', {'class': 'profile-stat'})
                    for stat in stats:
                        label = stat.find('p', {'class': 'text-label'}).text.strip().lower() if stat.find('p', {'class': 'text-label'}) else ''
                        value = stat.find('p', {'class': 'text-lead'}).text.strip() if stat.find('p', {'class': 'text-lead'}) else '0'
                        value = int(''.join(filter(str.isdigit, value)) or 0)
                        
                        if 'friends' in label:
                            profile_data['friends'] = value
                        elif 'followers' in label:
                            profile_data['followers'] = value
                        elif 'following' in label:
                            profile_data['following'] = value
                        elif 'place visits' in label:
                            profile_data['place_visits'] = value
                    
                    return profile_data
                return None
        except:
            return None

    async def get_user_badges(self, user_id: int) -> List[Dict]:
        try:
            async with self.session.get(f"{self.api_url}/users/{user_id}/badges") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                return []
        except:
            return []

    async def get_user_friends(self, user_id: int, page_size: int = 100) -> List[Dict]:
        try:
            async with self.session.get(f"{self.api_url}/users/{user_id}/friends?page=1&pageSize={page_size}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                return []
        except:
            return []

    async def get_user_groups(self, user_id: int) -> List[Dict]:
        try:
            async with self.session.get(f"{self.api_url}/users/{user_id}/groups") as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return []
        except:
            return []

    async def get_last_online(self, user_id: int) -> Optional[str]:
        try:
            async with self.session.get(f"{self.base_url}/users/{user_id}/profile") as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    last_online = soup.find('div', {'class': 'profile-status'})
                    if last_online:
                        return last_online.text.strip()
                return None
        except:
            return None

    async def search_users(self, keyword: str, limit: int = 10) -> List[Dict]:
        try:
            async with self.session.get(f"{self.api_url}/users/search?keyword={keyword}&limit={limit}") as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get('data', [])
                return []
        except:
            return []

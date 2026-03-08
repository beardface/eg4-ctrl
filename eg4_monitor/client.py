import json
import logging
import os
from typing import Optional, Dict, Any

import requests
import httpx

from .exceptions import AuthError, APIError, SessionError
from .models import InverterData

logger = logging.getLogger(__name__)

class EG4BaseClient:
    """Base functionality for EG4 Monitor clients."""
    BASE_URL = "https://monitor.eg4electronics.com/WManage"
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/5.37.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/5.37.',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://monitor.eg4electronics.com',
    }

    def __init__(self, username: str, password: str, serial_num: str, session_file: Optional[str] = None):
        self.username = username
        self.password = password
        self.serial_num = serial_num
        self.session_file = session_file

    def _get_cookies_from_file(self) -> Dict[str, str]:
        if not self.session_file or not os.path.exists(self.session_file):
            return {}
        try:
            with open(self.session_file, 'r') as f:
                cookies = json.load(f)
                if isinstance(cookies, dict):
                    return {k: v for k, v in cookies.items() if isinstance(v, str)}
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load session from {self.session_file}: {e}")
        return {}

    def _save_cookies_to_file(self, cookies: Dict[str, str]) -> None:
        if not self.session_file:
            return
        try:
            with open(self.session_file, 'w') as f:
                json.dump(cookies, f)
        except IOError as e:
            logger.error(f"Failed to save session to {self.session_file}: {e}")

class EG4Client(EG4BaseClient):
    """Synchronous client for interacting with the EG4 Monitor API."""

    def __init__(self, username: str, password: str, serial_num: str, session_file: Optional[str] = None):
        super().__init__(username, password, serial_num, session_file)
        self.session = requests.Session()
        self.session.headers.update(self.DEFAULT_HEADERS)
        
        cookies = self._get_cookies_from_file()
        for name, value in cookies.items():
            self.session.cookies.set(name, value)

    def login(self) -> bool:
        """Authenticates with the EG4 Monitor website."""
        login_url = f"{self.BASE_URL}/web/login"
        payload = {'account': self.username, 'password': self.password}
        try:
            response = self.session.post(login_url, data=payload, allow_redirects=True)
            if "login" in response.url:
                raise AuthError("Authentication failed. Check username and password.")
            self._save_cookies_to_file(self.session.cookies.get_dict())
            return True
        except requests.RequestException as e:
            raise AuthError(f"Login request failed: {e}")

    def get_inverter_data(self) -> InverterData:
        """Fetches the current status and battery data from the API."""
        if "JSESSIONID" not in self.session.cookies:
            self.login()

        api_url = f"{self.BASE_URL}/api/battery/getBatteryInfo"
        payload = {'serialNum': self.serial_num}
        try:
            response = self.session.post(api_url, data=payload)
            if response.status_code == 401:
                self.session.cookies.clear()
                self.login()
                response = self.session.post(api_url, data=payload)

            if response.status_code != 200:
                raise APIError(f"API HTTP Error: {response.status_code}")

            data = response.json()
            if not data.get('success'):
                self.session.cookies.clear()
                if self.session_file and os.path.exists(self.session_file):
                    os.remove(self.session_file)
                raise APIError(f"API Error: {data.get('msg', 'Unknown error')}")

            return InverterData.model_validate(data)
        except requests.RequestException as e:
            raise APIError(f"API connection error: {e}")

class AsyncEG4Client(EG4BaseClient):
    """Asynchronous client for interacting with the EG4 Monitor API."""

    def __init__(self, username: str, password: str, serial_num: str, session_file: Optional[str] = None):
        super().__init__(username, password, serial_num, session_file)
        cookies = self._get_cookies_from_file()
        self.client = httpx.AsyncClient(headers=self.DEFAULT_HEADERS, cookies=cookies)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    async def close(self):
        await self.client.aclose()

    async def login(self) -> bool:
        """Authenticates with the EG4 Monitor website."""
        login_url = f"{self.BASE_URL}/web/login"
        payload = {'account': self.username, 'password': self.password}
        try:
            response = await self.client.post(login_url, data=payload, follow_redirects=True)
            if "login" in str(response.url):
                raise AuthError("Authentication failed. Check username and password.")
            
            cookies_dict = {name: value for name, value in self.client.cookies.items()}
            self._save_cookies_to_file(cookies_dict)
            return True
        except httpx.RequestError as e:
            raise AuthError(f"Login request failed: {e}")

    async def get_inverter_data(self) -> InverterData:
        """Fetches the current status and battery data from the API."""
        if "JSESSIONID" not in self.client.cookies:
            await self.login()

        api_url = f"{self.BASE_URL}/api/battery/getBatteryInfo"
        payload = {'serialNum': self.serial_num}
        try:
            response = await self.client.post(api_url, data=payload)
            if response.status_code == 401:
                self.client.cookies.clear()
                await self.login()
                response = await self.client.post(api_url, data=payload)

            if response.status_code != 200:
                raise APIError(f"API HTTP Error: {response.status_code}")

            data = response.json()
            if not data.get('success'):
                self.client.cookies.clear()
                if self.session_file and os.path.exists(self.session_file):
                    os.remove(self.session_file)
                raise APIError(f"API Error: {data.get('msg', 'Unknown error')}")

            return InverterData.model_validate(data)
        except httpx.RequestError as e:
            raise APIError(f"API connection error: {e}")

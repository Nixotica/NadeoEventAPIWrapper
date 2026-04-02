import os
import requests
from ..environment import NADEO_AUTH
from .enums import NadeoService

from ..constants import NADEO_AUTH_URL, NADEO_REFRESH_AUTH_URL


class UbiTokenManager:
    _instance = None
    _nadeo_live_token = None
    _nadeo_live_refresh_token = None
    _nadeo_club_token = None
    _nadeo_club_refresh_token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UbiTokenManager, cls).__new__(cls)
        return cls._instance

    def authenticate(self, service: NadeoService, authorization: str = None) -> str: # type: ignore
        """
        Authenticates with the provided Nadeo service given authorization
        and returns an access token.

        :param service: Audience (e.g. "NadeoClubServices", "NadeoLiveServices")
        :param authorization: Override authorization (Basic <user:pass> base 64) if not defined in environment.
        :return: Access token
        """
        refreshed_auth = self.__authenticate_with_refresh_token(service)
        if refreshed_auth:
            return refreshed_auth

        auth = os.getenv(NADEO_AUTH) if not authorization else authorization
        headers = {
            "Content-Type": "application/json",
            "Authorization": auth,
            "User-Agent": "https://github.com/Nixotica/NadeoEventAPIWrapper",
        }
        body = {"audience": service.value}
        result = requests.post(NADEO_AUTH_URL, headers=headers, json=body).json()
        return self.__set_tokens(service, result)
    
    def __authenticate_with_refresh_token(self, service: NadeoService) -> str | None:
        try:
            token: str = None
            if service == NadeoService.LIVE:
                token = self._nadeo_live_refresh_token
            elif service == NadeoService.CLUB:
                token = self._nadeo_club_refresh_token
            
            if token:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": f"nadeo_v1 t={token}",
                    "User-Agent": "https://github.com/Nixotica/NadeoEventAPIWrapper",
                }
                body = {"audience": service.value}
                result = requests.post(NADEO_REFRESH_AUTH_URL, headers=headers, json=body).json()
                return self.__set_tokens(service, result)

            return None
        except:
            return None
        
    def __set_tokens(self, service: NadeoService, tokens: dict) -> None:
        if service == NadeoService.LIVE:
            self._nadeo_live_token = tokens["accessToken"]
            self._nadeo_live_refresh_token = tokens["refreshToken"]
        elif service == NadeoService.CLUB:
            self._nadeo_club_token = tokens["accessToken"]
            self._nadeo_club_refresh_token = tokens["refreshToken"]
        return tokens["accessToken"]

    @property
    def nadeo_live_token(self) -> str:
        if self._nadeo_live_token is None:
            self._nadeo_live_token = self.authenticate(NadeoService.LIVE)
        return self._nadeo_live_token

    @property
    def nadeo_club_token(self) -> str:
        if self._nadeo_club_token is None:
            self._nadeo_club_token = self.authenticate(NadeoService.CLUB)
        return self._nadeo_club_token

    @nadeo_live_token.setter
    def nadeo_live_token(self, value):
        self._nadeo_live_token = value

    @nadeo_club_token.setter
    def nadeo_club_token(self, value):
        self._nadeo_club_token = value

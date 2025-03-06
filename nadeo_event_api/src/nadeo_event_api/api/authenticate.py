import os
import requests
from ..environment import UBI_AUTH
from .enums import NadeoService

from ..constants import NADEO_AUTH_URL, UBI_SESSION_URL


class UbiTokenManager:
    _instance = None
    _nadeo_live_token = None
    _nadeo_club_token = None
    _nadeo_prod_token = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UbiTokenManager, cls).__new__(cls)
        return cls._instance

    def authenticate(self, service: NadeoService, authorization: str = None) -> str: # type: ignore
        """
        Authenticates with the provided Nadeo service given authorization
        and returns an access token.

        :param service: Audience (e.g. "NadeoClubServices", "NadeoLiveServices", "NadeoServices")
        :param authorization: Override authorization (Basic <user:pass> base 64) if not defined in environment.
        :return: Access token
        """
        auth = os.getenv(UBI_AUTH) if not authorization else authorization
        headers = {
            "Content-Type": "application/json",
            "Ubi-AppId": "86263886-327a-4328-ac69-527f0d20a237",
            "Authorization": auth,
            "User-Agent": "https://github.com/Nixotica/NadeoEventAPIWrapper",
        }
        result = requests.post(UBI_SESSION_URL, headers=headers).json()

        ticket = result["ticket"]
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"ubi_v1 t={ticket}",
        }
        body = {"audience": service.value}
        auth = requests.post(NADEO_AUTH_URL, headers=headers, json=body).json()[
            "accessToken"
        ]
        if service == NadeoService.LIVE:
            self._nadeo_live_token = auth
        elif service == NadeoService.CLUB:
            self._nadeo_club_token = auth
        elif service == NadeoService.PROD:
            self._nadeo_prod_token = auth
        return auth

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
    
    @property
    def nadeo_prod_token(self) -> str:
        if self._nadeo_prod_token is None:
            self._nadeo_prod_token = self.authenticate(NadeoService.PROD)
        return self._nadeo_prod_token

    @nadeo_live_token.setter
    def nadeo_live_token(self, value):
        self._nadeo_live_token = value

    @nadeo_club_token.setter
    def nadeo_club_token(self, value):
        self._nadeo_club_token = value

    @nadeo_prod_token.setter
    def nadeo_prod_token(self, value):
        self._nadeo_prod_token = value

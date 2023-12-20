from __future__ import annotations
from ..authenticate import UbiTokenManager
import requests
from ...constants import CLUB_CAMPAIGN_URL_FMT

from ..structure.maps import PlaylistMap


class Campaign:
    def __init__(
        self,
        club_id: int,
        campaign_id: int,
    ):
        self._club_id = club_id
        self._campaign_id = campaign_id
        self._playlist = None

        token = UbiTokenManager().nadeo_live_token
        response = requests.get(
            url=CLUB_CAMPAIGN_URL_FMT.format(club_id, campaign_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
        ).json()
        if isinstance(response, list):
            print("Failed to get campaign: ", response)
            return
        campaign_info = response["campaign"]

        self._playlist = PlaylistMap._list_from_campaign_response(
            campaign_info["playlist"]
        )

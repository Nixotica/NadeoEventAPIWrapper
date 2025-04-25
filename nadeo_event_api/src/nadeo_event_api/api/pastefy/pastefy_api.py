# Hosted by Matrix, requires dedicated IP whitelist to work.

import datetime
import json
import requests
from base64 import b64encode

from nadeo_event_api.api.endpoints import PASTEFY_SKIFF_CREATE_URL, PASTEFY_SKIFF_RAW_URL_FMT
from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Paste


def get_auth(username: str, password: str) -> str:
    return b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")


def post_tmwt_2v2(tmwt_2v2_pastebin: Tmwt2v2Paste, title: str, basic_auth: str) -> str:
    """Posts a TMWT 2v2 paste to pastes.skiff.dev and returns the URL of the raw paste. Expires in 1 hour.
        NOTE: Contact Matrix/skiff for API credentials

    Args:
        tmwt_2v2_pastebin (Tmwt2v2Pastebin): The TMWT paste.
        title (str): The title of the paste.
        auth (str): HTTP Basic Authentication header value

    Returns:
        str: The raw URL of the paste. 
    """
    content = json.dumps(tmwt_2v2_pastebin.as_jsonable_dict(), indent=4)
    expiry_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    formatted = expiry_date.strftime('%Y-%m-%d %H:%M:%S') + '.0'
    data = {
        "type": "PASTE",
        "title": title,
        "content": content,
        "expire_at": formatted,
        "visibility": "PUBLIC",
    }

    headers = {
        "Authorization": f"Basic {basic_auth}"
    }

    response = requests.post(
        url=PASTEFY_SKIFF_CREATE_URL,
        headers=headers,
        data=data,
    )
    if response.status_code != 200:
        raise Exception(f"Failed to post to pastes.skiff.dev API - {response.content}")
    
    paste_id = response.json()["paste"]["id"]
    paste_url = PASTEFY_SKIFF_RAW_URL_FMT.format(paste_id)
    return paste_url
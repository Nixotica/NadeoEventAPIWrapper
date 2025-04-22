# Hosted by Matrix, requires dedicated IP whitelist to work.

import datetime
import json
import requests

from nadeo_event_api.api.endpoints import PASTEFY_SKIFF_CREATE_URL, PASTEFY_SKIFF_RAW_URL_FMT
from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Paste

def post_tmwt_2v2(tmwt_2v2_pastebin: Tmwt2v2Paste, title: str) -> str:
    """Posts a TMWT 2v2 paste to pastes.skiff.dev and returns the URL of the raw paste. Expires in 1 hour.
        NOTE: Must have a whitelisted IP -- contact Matrix/Skiff for this if needed. 

    Args:
        tmwt_2v2_pastebin (Tmwt2v2Pastebin): The TMWT paste.
        title (str): The title of the paste.

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

    response = requests.post(
        url=PASTEFY_SKIFF_CREATE_URL,
        data=data,
    )
    if response.status_code != 200:
        print(response.text)
        raise Exception(f"Failed to post to pastes.skiff.dev API.")
    
    paste_id = response.json()["paste"]["id"]
    paste_url = PASTEFY_SKIFF_RAW_URL_FMT.format(paste_id)
    return paste_url
import json
import requests

from nadeo_event_api.api.endpoints import PASTES_IO_CREATE_URL, PASTES_IO_LOGIN_URL
from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Paste


def login(username: str, password: str) -> str:
    """Logs in to the pastes.io API and returns the token.

    Args:
        username (str): Your username.
        password (str): Your password.

    Returns:
        str: The API token used to authenticate requests.
    """

    header = {"Accept": "application/json"}
    data = {
        "username": username,
        "password": password,
    }
    response = requests.post(
        url=PASTES_IO_LOGIN_URL,
        headers=header,
        data=data,
    )

    print('response in token:', response.content)

    if response.status_code != 200:
        error = response.json()["error"]
        raise Exception(f"Failed to login to pastes.io API: {error}")
    
    return response.json()["success"]["api_token"]

def post_tmwt_2v2(tmwt_2v2_pastebin: Tmwt2v2Paste, title: str, token: str) -> str:
    """Posts a TMWT 2v2 paste to pastes.io and returns the URL of the raw paste. Expires in 1 hour.

    Args:
        tmwt_2v2_pastebin (Tmwt2v2Pastebin): The TMWT paste.
        title (str): The title of the paste.
        token (str): The API token to make the request.

    Returns:
        str: The raw URL of the paste. 
    """
    content = json.dumps(tmwt_2v2_pastebin.as_jsonable_dict(), indent=4)
    data = {
        "content": content,
        "status": 1, # 0 = public, 1 = unlisted, 2 = private
        "expire": "1H", # 1H = 1 hour
        "title": title,
    }
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
    }

    response = requests.post(
        url=PASTES_IO_CREATE_URL,
        headers=headers,
        data=data,
    )
    if response.status_code != 200:
        error = response.json()["error"]
        raise Exception(f"Failed to post to pastes.io API: {error}")
    
    print(response.json())
    paste_url = response.json()["success"]["paste_url"]

    raw_url = paste_url.replace("https://pastes.io/", "https://pastes.io/raw/")
    return raw_url
import json
import requests
from nadeo_event_api.api.endpoints import PASTEBIN_POST_URL
from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Paste


def post_tmwt_2v2(tmwt_2v2_pastebin: Tmwt2v2Paste, api_dev_key: str) -> str:
    """Posts a TMWT 2v2 Pastebin and returns the URL of the pastebin.

    Args:
        tmwt_2v2_pastebin (Tmwt2v2Pastebin): The TMWT pastebin
        api_dev_key (str): The API key to make the request

    Returns:
        str: The raw URL of the pastebin.
    """

    content = json.dumps(tmwt_2v2_pastebin.as_jsonable_dict(), indent=4)

    data = {
        "api_dev_key": api_dev_key,
        "api_paste_code": content,
        "api_option": "paste",
        "api_paste_expire_data": "1D",
    }

    response = requests.post(
        url=PASTEBIN_POST_URL,
        data=data,
    )
    if response.status_code == 200:
        paste_url = response.text
        raw_url = paste_url.replace("https://pastebin.com/", "https://pastebin.com/raw/")
        return raw_url
    else:
        raise RuntimeError(
            f"Error posting pastebin: {response.status_code} {response.text}"
        )
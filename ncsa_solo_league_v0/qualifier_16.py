from datetime import timedelta
import datetime
import os
from pathlib import Path
import sys

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.constants import CLUB_AUTO_EVENTS_STAGING


### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "TestSoloPlayoff"
club_id = CLUB_AUTO_EVENTS_STAGING
campaign_id = 57253  # "Test Solo League"

# This MUST be 8 players in order of seed (1-8)
players = [
    "dadbaf28-e7b5-429b-bf37-8c8c1419fcf4",  # That_Ski_Freak
    "bd45204c-80f1-4809-b983-38b3f0ffc1ef",  # WirtualTM
    "6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # RandomizeTM
    "ef39801d-e749-4068-821a-8670602f2f24",  # xavier_b
    "a76653e1-998a-4c53-8a91-0a396e15bfb5",  # MrDarrek
    "39be7ebf-2517-4c59-8091-53daec796e89",  # Ubi-Alinoa
    "b981e0b1-2d6a-4470-9b52-c1f6b0b1d0a6",  # longi.tm
    "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
]

now = datetime.utcnow()
ta_qualifier = now + timedelta(minutes=5)

quarter_1_start = now + timedelta(minutes=5)
quarter_2_start = now + timedelta(hours=10)
quarter_3_start = now + timedelta(hours=15)
quarter_4_start = now + timedelta(hours=20)
semi_1_start = now + timedelta(hours=25)
semi_2_start = now + timedelta(hours=30)
grand_start = now + timedelta(hours=35)
### NOTE END ###
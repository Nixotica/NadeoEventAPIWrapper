import datetime as dt
import os
from pathlib import Path
import sys

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.event_api import get_event_leaderboard, get_match_results, get_matches_for_round, get_rounds_for_event
from nadeo_event_api.api.structure.enums import AutoStartMode, ScriptType
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import SeedMatchSpot
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.settings.plugin_settings import ClassicPluginSettings
from nadeo_event_api.api.structure.settings.script_settings import (
    BaseScriptSettings,
    CupScriptSettings,
)

# # Event info
# event_name = "BetterMMTest"
# club_id = 69352 # "Auto Events Staging"
# campaign_id = 58885 # "Fast Cup Test"

# players = [
#     # "dadbaf28-e7b5-429b-bf37-8c8c1419fcf4",  # That_Ski_Freak
#     "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
#     "9851b4af-d6f1-4aa9-8fe4-cbcbfb05f2b4",  # CD 
#     "df9448f1-a8d5-4682-9003-1c2777c62b91",  # alxshaer
# ]

# now = dt.datetime.utcnow()
# match_start = now + dt.timedelta(minutes=1)

# # Get the map pool
# campaign_playlist = Campaign(club_id, campaign_id)._playlist
# map_pool = [Map(campaign_playlist[3]._uuid)] # type: ignore

# # Create the event
# event = Event(
#     name=event_name,
#     club_id=club_id,
#     rounds=[Round(
#         name="Better Match",
#         start_date=match_start,
#         end_date=match_start + dt.timedelta(hours=1),
#         matches=[Match(spots=[SeedMatchSpot(x) for x in range(1,4)])],
#         config=RoundConfig(
#             map_pool=map_pool,
#             script=ScriptType.CUP_CLASSIC,
#             max_players=3,
#             script_settings=CupScriptSettings(
#                 base_script_settings=BaseScriptSettings(),
#                 points_repartition="10,5,3,0",
#                 finish_timeout=15,
#                 points_limit=40,
#             ),
#             plugin_settings=ClassicPluginSettings(
#                 auto_start_mode=AutoStartMode.DELAY,
#                 use_auto_ready=False,
#                 auto_start_delay=300,
#             )
#         )
#     )],
# )
# event.post()

# # Add the players to the event
# for player_idx in range(len(players)):
#     event.add_participant(players[player_idx], player_idx + 1)

event_id = 21511
print(f'match leaderboard {get_event_leaderboard(event_id, 5, 0)}')

# Before match opened up:
# match leaderboard [{"participant":"df9448f1-a8d5-4682-9003-1c2777c62b91","rank":1,"score":0,"zone":"World"},{"participant":"9851b4af-d6f1-4aa9-8fe4-cbcbfb05f2b4","rank":2,"score":0,"zone":"World"},{"participant":"2e34c3cb-9548-4815-aee3-c68518a1fd88","rank":3,"score":0,"zone":"World"}]

# After players joined match before starting:
# 
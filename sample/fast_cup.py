import datetime
from datetime import datetime, timedelta
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
from nadeo_event_api.api.structure.enums import AutoStartMode, LeaderboardType, ParticipantType, ScriptType
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import SeedMatchSpot, TeamMatchSpot
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.settings.plugin_settings import ClassicPluginSettings, TMWTPluginSettings
from nadeo_event_api.api.structure.settings.script_settings import CupSpecialScriptSettings, TMWTScriptSettings
from nadeo_event_api.constants import CLUB_AUTO_EVENTS_STAGING

# Event info
event_name = "FastCupTest"
club_id = CLUB_AUTO_EVENTS_STAGING
campaign_id = 58885	  # "Fast Cup Test"

players = [
    "dadbaf28-e7b5-429b-bf37-8c8c1419fcf4",  # That_Ski_Freak
    "2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
    "ec0269d5-2d19-41eb-a931-01b8a11c2784",  # Random.TX
    "f5e37115-d85a-4f3e-bc5a-969d6e29fede",  # tewbs
]

now = datetime.utcnow()
match_start = now + timedelta(minutes=1)

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

# Create the event
event = Event(
    name=event_name,
    club_id=club_id,
    rounds=[Round(
        name="Round 1",
        start_date=match_start,
        end_date=match_start + timedelta(hours=1),
        matches=[Match(spots=[SeedMatchSpot(x) for x in range(1,5)])],
        leaderboard_type=LeaderboardType.BRACKET,
        config=RoundConfig(
            map_pool=map_pool,
            script=ScriptType.CUP_LONG,
            max_players=4,
            script_settings=CupSpecialScriptSettings(
                warmup_number=1,
                warmup_duration=60,
                points_repartition="10,5,3,0",
                cup_points_limit=30,
                match_points_limit=2,
                number_of_winners=3,
                finish_timeout=10,
            ),
            plugin_settings=ClassicPluginSettings(
                auto_start_mode=AutoStartMode.DISABLED,
                use_auto_ready=False,
                pick_ban_order="p:0,p:1,p:2,p:3,p:r,p:r",
                pick_ban_start_auto=True,
            )
        )
    )]
)
event.post()

# Add the players to the event
for player_idx in range(len(players)):
    event.add_participant(players[player_idx], player_idx+1)
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
from nadeo_event_api.api.structure.enums import (
    ParticipantType,
    ScriptType,
)
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import TeamMatchSpot
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.settings.plugin_settings import TMWTPluginSettings
from nadeo_event_api.api.structure.settings.script_settings import TMWTScriptSettings, BaseScriptSettings
from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Pastebin, Tmwt2v2PastebinTeam
from nadeo_event_api.api.pastebin.pastebin_api import post_tmwt_2v2

# Event info
event_name = "pastebin2v2"
match_club_id = 69352  # "Auto Events Staging"
campaign_club_id = 68298  # "NCSA Trackmania"
campaign_id = 81781  # "NAC #3 Campaign"

# Create teams of two by UID
blue_team = Tmwt2v2PastebinTeam(
    team_name="Blue",
    p1_tm_account_id="2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
    p2_tm_account_id="6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # Randomize
)

red_team = Tmwt2v2PastebinTeam(
    team_name="Red",
    p1_tm_account_id="c7818ba0-5e85-408e-a852-f658e8b90eec",  # Dummy
    p2_tm_account_id="551dd1f5-2380-417d-98a5-8e2244f9287f",  # Revants
)

pastebin = Tmwt2v2Pastebin(
    team_a=blue_team,
    team_b=red_team,
)

pastebin_url = post_tmwt_2v2(pastebin, os.environ.get("PASTEBIN_API_DEV_KEY")) # type: ignore

now = datetime.utcnow()
match_start = now + timedelta(minutes=1)

# Get the map pool
campaign_playlist = Campaign(campaign_club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist] # type: ignore

# Create the event
event = Event(
    name=event_name,
    club_id=match_club_id,
    rounds=[
        Round(
            name="Round 1",
            start_date=match_start,
            end_date=match_start + timedelta(hours=1),
            matches=[
                Match(
                    spots=[TeamMatchSpot(1), TeamMatchSpot(2)],
                )
            ],
            config=RoundConfig(
                map_pool=[map_pool[2]],
                script=ScriptType.TMWT_TEAMS,
                max_players=4,
                script_settings=TMWTScriptSettings(
                    base_script_settings=BaseScriptSettings(
                        warmup_number=1,
                        warmup_duration=60,
                    ),
                    teams_url=pastebin_url,
                    match_points_limit=1,
                    match_info="Hello Twitch"
                ),
                plugin_settings=TMWTPluginSettings(
                    ready_minimum_team_size=2,
                    pick_ban_start_auto=False,
                    pick_ban_order="",
                ),
            ),
        )
    ],
    participant_type=ParticipantType.TEAM,
)
event.post()

# Add teams
event.add_team(blue_team.team_name, blue_team.members(), 1)
event.add_team(red_team.team_name, red_team.members(), 2)

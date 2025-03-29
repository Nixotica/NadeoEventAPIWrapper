import datetime
from datetime import datetime, timedelta
import json
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
from nadeo_event_api.api.structure.settings.script_settings import TMWT2025ScriptSettings, TMWC2023ScriptSettings, BaseTMWTScriptSettings, BaseScriptSettings
from nadeo_event_api.objects.outbound.pastebin.tmwt_2v2 import Tmwt2v2Pastebin, Tmwt2v2PastebinTeam
from nadeo_event_api.api.pastebin.pastebin_api import post_tmwt_2v2
from nadeo_event_api.objects.outbound.settings.pick_ban_style import PickBanStyle

# Event info
event_name = "tmwt2025"
match_club_id = 69352  # "Auto Events Staging"
campaign_club_id = 68298  # "NCSA Trackmania"
campaign_id = 81781  # "NAC #3 Campaign"

# Create teams of two by UID
blue_team = Tmwt2v2PastebinTeam(
    team_name="Blue",
    p1_tm_account_id="febeaf4d-f340-4954-9fe2-88390959ae53",  # Charles
    p2_tm_account_id="6e3bf3f9-7dcb-47d4-bdae-037ab66628f2",  # Randomize
)

red_team = Tmwt2v2PastebinTeam(
    team_name="Red",
    p1_tm_account_id="2e34c3cb-9548-4815-aee3-c68518a1fd88",  # Nixotica
    p2_tm_account_id="da244fe1-a978-449e-8a06-1362bce8b203",  # Slorpie
)

pastebin = Tmwt2v2Pastebin(
    team_a=blue_team,
    team_b=red_team,
)

# pastebin_url = post_tmwt_2v2(pastebin, os.environ.get("PASTEBIN_API_DEV_KEY")) # type: ignore

now = datetime.utcnow()
match_start = now + timedelta(minutes=1)

# Get the map pool
# campaign_playlist = Campaign(campaign_club_id, campaign_id)._playlist
# map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist] # type: ignore

map_pool = [
    Map("0J5dIC0oJ2zQuBe0nvn1io6armb"),
    Map("9m_hRxynCoM5fnw6A7gCMhp_QVc"),
    Map("yS2Hr7wAjNGC16Y49tVU_Ppu_A2"),
    Map("9wgjCAiTwAJu1USs8VO6CGBq8P7"),
    Map("9ra9rUfOyLGfuOpUI9TfmcU8Up6"),
]

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
                map_pool=map_pool,
                script=ScriptType.TMWT_2025,
                max_players=4,
                script_settings=TMWT2025ScriptSettings(
                    base_tmwt_script_settings=BaseTMWTScriptSettings(
                        base_script_settings=BaseScriptSettings(
                            warmup_number=1,
                            warmup_duration=30,
                            pick_ban_enable=True,
                        ),
                        match_points_limit=2,
                        match_info="2025 THE YEAR",
                        teams_url="https://pastebin.com/raw/hSLVPj1c",
                    ),
                    map_points_limit=5,
                    loading_screen_image_url="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/AM_Stream_BG_Nologo.png",
                    header_logo_url="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/Americas_Masters.png",
                    intro_background_url="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/AM_Stream_BG_Nologo.png",
                    intro_logo_url="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/Americas_Masters.png",
                    pick_ban_style=PickBanStyle(
                        background="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/AM_Stream_BG_Nologo.png",
                        top_left_logo="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/AM_Stream_BG_Nologo.png",
                        top_right_logo="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/AM_Stream_BG_Nologo.png",
                        bottom_logo="https://download.dashmap.live/6e3bf3f9-7dcb-47d4-bdae-037ab66628f2/AM_Stream_BG_Nologo.png",
                    ),
                    finish_timeout=15,
                    disable_match_intro=False,
                    is_matchmaking=True,
                ),
                plugin_settings=TMWTPluginSettings(
                    ready_minimum_team_size=1,
                    pick_ban_start_auto=True,
                    use_auto_ready=True,
                    pick_ban_order="b:1,b:0,p:0,p:1,p:r",
                    pick_ban_use_gamepad_version=True,
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

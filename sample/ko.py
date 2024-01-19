from datetime import datetime, timedelta
import json
import os
from pathlib import Path
import random
import sys
from typing import List
import pytz

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.authenticate import UbiTokenManager
from nadeo_event_api.api.enums import NadeoService
from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.qualifier import Qualifier, QualifierConfig
from nadeo_event_api.api.structure.enums import LeaderboardType, ScriptType, PluginType
from nadeo_event_api.api.structure.round.round import Round, RoundConfig
from nadeo_event_api.api.structure.enums import AutoStartMode
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import SeedMatchSpot
from nadeo_event_api.api.structure.settings.script_settings import (
    TimeAttackScriptSettings,
    KnockoutScriptSettings,
)
from nadeo_event_api.api.structure.settings.plugin_settings import (
    ClassicPluginSettings,
    QualifierPluginSettings,
)


def get_qualifier(
    start_date: datetime, end_date: datetime, map_pool: List[Map]
) -> Qualifier:
    return Qualifier(
        name="Qualifier",
        start_date=start_date,
        end_date=end_date,
        leaderboard_type=LeaderboardType.SUMSCORE,
        config=QualifierConfig(
            map_pool=map_pool,
            script=ScriptType.TIME_ATTACK,
            script_settings=TimeAttackScriptSettings(
                time_limit=300,
            ),
            plugin_settings=QualifierPluginSettings(
                use_playlist_complete=True,
            ),
            plugin=PluginType.CLUB,
        ),
    )


def get_round(
    start_date: datetime, end_date: datetime, qualifier: Qualifier, map_pool: List[Map]
) -> Round:
    return Round(
        name="Knockout",
        start_date=start_date,
        end_date=end_date,
        qualifier=qualifier,
        config=RoundConfig(
            map_pool=map_pool,
            script=ScriptType.KNOCKOUT,
            script_settings=KnockoutScriptSettings(
                warmup_number=1,
                warmup_duration=75,
                finish_timeout=15,
                rounds_without_elimination=1,
            ),
            plugin_settings=ClassicPluginSettings(
                auto_start_mode=AutoStartMode.DELAY,
                auto_start_delay=120,
            ),
            max_players=64,
            plugin=PluginType.CLUB,
        ),
        matches=[Match([SeedMatchSpot(x) for x in range(1, 65)])],
    )


event_name = "TestKOEvent"
club_id = 69352 # "Auto Events Staging"
campaign_id = 57253  # "Test Solo League"

# Get a random map from the campaign
campaign_playlist = Campaign(club_id, campaign_id)._playlist
random_map = Map(random.choice(campaign_playlist)._uuid)

# Create registration at now plus some offset so it's not in the past
registration_start = datetime.utcnow() + timedelta(minutes=1)
start_time = registration_start + timedelta(minutes=3)

# Qualifier
qualifier = get_qualifier(
    start_time, start_time + timedelta(minutes=6), [random_map]
)

# Knockout round 
ko_round = get_round(
    qualifier._end_date + timedelta(minutes=1),
    qualifier._end_date + timedelta(minutes=60),
    qualifier,
    [random_map],
)

# Event
event = Event(
    name=event_name,
    club_id=club_id,
    registration_start_date=registration_start,
    registration_end_date=qualifier._end_date,
    rounds=[ko_round],
    description="This is a Pan-American daily KO event on the seasonal map pool! It is automatically hosted every night 1 hour after COTN. Join the discord: $lhttps://discord.gg/pj9C5znHzf",
)
event.post()

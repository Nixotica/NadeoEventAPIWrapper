from datetime import datetime, timedelta
import os
from pathlib import Path
import sys
from typing import List

from pytz import timezone

# NOTE we do this for now since the api package is still WIP, will separate this into a different
# repo which consumes that package eventually
event_api_pkg = os.path.join(
    Path(__file__).resolve().parent.parent, "nadeo_event_api/src/"
)
sys.path.append(str(event_api_pkg))

from nadeo_event_api.api.structure.settings.plugin_settings import (
    ClassicPluginSettings,
    QualifierPluginSettings,
)
from nadeo_event_api.api.structure.settings.script_settings import (
    BaseScriptSettings,
    CupSpecialScriptSettings,
    TimeAttackScriptSettings,
)
from nadeo_event_api.api.structure.round.qualifier import Qualifier, QualifierConfig
from nadeo_event_api.api.structure.event import Event
from nadeo_event_api.api.club.campaign import Campaign
from nadeo_event_api.api.structure.enums import (
    AutoStartMode,
    LeaderboardType,
    ScriptType,
)
from nadeo_event_api.api.structure.maps import Map
from nadeo_event_api.api.structure.round.match import Match
from nadeo_event_api.api.structure.round.match_spot import (
    MatchParticipantMatchSpot,
    QualificationMatchSpot,
)
from nadeo_event_api.api.structure.round.round import Round, RoundConfig


def get_round_config(
    map_pool: List[Map],
    num_winners: int,
) -> RoundConfig:
    return RoundConfig(
        map_pool=map_pool,
        script=ScriptType.CUP_LONG,
        max_players=4,
        script_settings=CupSpecialScriptSettings(
            base_script_settings=BaseScriptSettings(
                warmup_number=1,
                warmup_duration=60,
            ),
            points_repartition="10,5,3,0",
            cup_points_limit=30,
            match_points_limit=2,
            number_of_winners=num_winners,
            finish_timeout=10,
        ),
        plugin_settings=ClassicPluginSettings(
            auto_start_mode=AutoStartMode.DELAY,
            auto_start_delay=300,
            pick_ban_start_auto=True,
            pick_ban_order="b:3,b:2,b:1,b:0,p:0,p:1,p:2,p:3,p:r,p:r,p:r",
            use_auto_ready=False,
        ),
    )


def get_match_from_prev_round(
    prev_round: int,
    prev_first_seed_match: int,
    prev_first_seed_rank: int,
    prev_second_seed_match: int,
    prev_second_seed_rank: int,
    prev_third_seed_match: int,
    prev_third_seed_rank: int,
    prev_fourth_seed_match: int,
    prev_fourth_seed_rank: int,
) -> Match:
    return Match(
        spots=[
            MatchParticipantMatchSpot(
                prev_round, prev_first_seed_match, prev_first_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_second_seed_match, prev_second_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_third_seed_match, prev_third_seed_rank
            ),
            MatchParticipantMatchSpot(
                prev_round, prev_fourth_seed_match, prev_fourth_seed_rank
            ),
        ]
    )


def get_match_from_quali(
    first_seed: int,
    second_seed: int,
    third_seed: int,
    fourth_seed: int,
) -> Match:
    return Match(
        spots=[
            QualificationMatchSpot(0, first_seed),
            QualificationMatchSpot(0, second_seed),
            QualificationMatchSpot(0, third_seed),
            QualificationMatchSpot(0, fourth_seed),
        ]
    )


def get_round_1(
    quali_start_date: datetime,
    round_start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Round 1",
        start_date=round_start_date,
        end_date=round_start_date + timedelta(hours=1),
        matches=[
            get_match_from_quali(1, 16, 17, 32),
            get_match_from_quali(2, 15, 18, 31),
            get_match_from_quali(3, 14, 19, 30),
            get_match_from_quali(4, 13, 20, 29),
            get_match_from_quali(5, 12, 21, 28),
            get_match_from_quali(6, 11, 22, 27),
            get_match_from_quali(7, 10, 23, 26),
            get_match_from_quali(8, 9, 24, 25),
        ],
        config=get_round_config(map_pool=map_pool, num_winners=2),
        qualifier=Qualifier(
            name="Seeding Qualifier",
            start_date=quali_start_date,
            end_date=quali_start_date + timedelta(minutes=len(map_pool) * 6), # 6 minutes per map roughly
            leaderboard_type=LeaderboardType.SUMSCORE,
            config=QualifierConfig(
                map_pool=map_pool,
                script=ScriptType.TIME_ATTACK,
                plugin_settings=QualifierPluginSettings(
                    use_playlist_complete=True,
                ),
                script_settings=TimeAttackScriptSettings(
                    base_script_settings=BaseScriptSettings(
                        warmup_number=1,
                        warmup_duration=20,
                    ),
                    time_limit=300, 
                ),
            ),
        ),
    )


def get_round_2(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Round 2",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_from_prev_round(0, 0, 1, 7, 1, 3, 2, 4, 2),
            get_match_from_prev_round(0, 1, 1, 6, 1, 2, 2, 5, 2),
            get_match_from_prev_round(0, 2, 1, 5, 1, 1, 2, 6, 2),
            get_match_from_prev_round(0, 3, 1, 4, 1, 0, 2, 7, 2),
            get_match_from_prev_round(0, 0, 3, 7, 3, 3, 4, 4, 4),
            get_match_from_prev_round(0, 1, 3, 6, 3, 2, 4, 5, 4),
            get_match_from_prev_round(0, 2, 3, 5, 3, 1, 4, 6, 4),
            get_match_from_prev_round(0, 3, 3, 4, 3, 0, 4, 7, 4),
        ],
        config=get_round_config(map_pool=map_pool, num_winners=2),
    )


def get_round_3(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Round 3",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_from_prev_round(1, 0, 1, 2, 1, 1, 2, 3, 2),
            get_match_from_prev_round(1, 1, 1, 3, 1, 0, 2, 2, 2),
            get_match_from_prev_round(1, 4, 1, 5, 2, 2, 3, 3, 4),
            get_match_from_prev_round(1, 5, 1, 6, 2, 3, 3, 0, 4),
            get_match_from_prev_round(1, 6, 1, 7, 2, 0, 3, 1, 4),
            get_match_from_prev_round(1, 7, 1, 0, 2, 1, 3, 2, 4),
        ],
        config=get_round_config(map_pool=map_pool, num_winners=3),
    )


def get_round_4(
    start_date: datetime,
    map_pool: List[Map],
) -> Round:
    return Round(
        name="Round 4",
        start_date=start_date,
        end_date=start_date + timedelta(hours=1),
        matches=[
            get_match_from_prev_round(2, 2, 1, 3, 2, 4, 3, 0, 4),
            get_match_from_prev_round(2, 3, 1, 4, 2, 5, 3, 1, 4),
            get_match_from_prev_round(2, 4, 1, 5, 2, 2, 3, 0, 3),
            get_match_from_prev_round(2, 5, 1, 2, 2, 3, 3, 1, 3),
        ],
        config=get_round_config(map_pool=map_pool, num_winners=3),
    )


### NOTE fill these out as appropriate each time the script is run! You shouldn't need to modify anything else! ###
event_name = "PASL Qualifier"
club_id = 68298 # "NCSA Trackmania"
campaign_id = 60108 # "PASL Winter 2024"

now = datetime.utcnow()
registration_start = now + timedelta(minutes=1)
r1_quali_start = datetime(2024, 2, 25, 18)
r1_start = datetime(2024, 2, 25, 19, 25)
r2_start = datetime(2024, 2, 25, 20, 30)
r3_start = datetime(2024, 2, 25, 22)
r4_start = datetime(2024, 2, 25, 23, 30)
### NOTE END ###

# Get the map pool
campaign_playlist = Campaign(club_id, campaign_id)._playlist
map_pool = [Map(campaign_map._uuid) for campaign_map in campaign_playlist]

r1 = get_round_1(r1_quali_start, r1_start, map_pool)
r2 = get_round_2(r2_start, map_pool)
r3 = get_round_3(r3_start, map_pool)
r4 = get_round_4(r4_start, map_pool)

# Create and post the event
event = Event(
    name=event_name,
    club_id=club_id,
    registration_start_date=registration_start,
    registration_end_date=r1_quali_start,
    rounds=[r1, r2, r3, r4],
)
event.post()

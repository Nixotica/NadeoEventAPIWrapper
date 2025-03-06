from typing import List, Optional
import requests

from ..objects.inbound.event_players import Participant, Team
from ..objects.inbound.match_info import MatchInfo

from ..objects.inbound.round import Round
from ..objects.inbound.match import Match
from ..objects.inbound.match_results import MatchResults

from .endpoints import (
    CREATE_COMP_URL,
    GET_EVENT_LEADERBOARD_URL_FMT,
    GET_MATCH_RESULTS_URL_FMT,
    GET_MATCHES_FOR_ROUND_URL_FMT,
    GET_ROUNDS_FOR_EVENT_URL_FMT,
    GET_MATCH_INFO_URL_FMT,
    GET_EVENT_PARTICIPANTS_URL_FMT,
    GET_EVENT_TEAMS_URL_FMT,
    GET_DISPLAY_NAMES_FMT
)
from .authenticate import UbiTokenManager
from .structure.event import Event


def post_event(event: Event) -> int | None:
    """
    Posts an event and returns the ID.
    """
    if not event.valid():
        print("Event is not valid, and therefore will not post.")
        return None
    token = UbiTokenManager().nadeo_club_token
    response = requests.post(
        url=CREATE_COMP_URL,
        headers={"Authorization": "nadeo_v1 t=" + token},
        json=event._as_jsonable_dict(),
    ).json()
    if "exception" in response:
        print("Failed to post event: ", response)
        return
    event._registered_id = response["competition"]["id"]
    event._live_id = response["competition"]["liveId"]
    return event._registered_id


def get_rounds_for_event(event_id: int) -> List[Round]:
    """
    Gets the rounds for an given event by ID.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_ROUNDS_FOR_EVENT_URL_FMT.format(event_id),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()
    # TODO exception handling
    return [Round.from_dict(round_info) for round_info in response]


def get_matches_for_round(round_id: int, length: int, offset: int) -> List[Match]:
    """
    Gets the matches for a given round by ID.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_MATCHES_FOR_ROUND_URL_FMT.format(round_id, length, offset),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()
    return [Match.from_dict(match_info) for match_info in response["matches"]]


def get_match_results(match_id: int, length: int, offset: int) -> MatchResults:
    """
    Gets the match results for a given match by ID.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_MATCH_RESULTS_URL_FMT.format(match_id, length, offset),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()
    return MatchResults.from_dict(response)


def get_match_info(match_live_id: str) -> MatchInfo:
    """
    Gets the match info for a given match by LiveID.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_MATCH_INFO_URL_FMT.format(match_live_id),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()
    return MatchInfo.from_dict(response)


def get_event_leaderboard(event_id: int, length: int, offset: int) -> str:
    """
    Gets the leaderboard for a given event by ID.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_EVENT_LEADERBOARD_URL_FMT.format(event_id, length, offset),
        headers={"Authorization": "nadeo_v1 t=" + token},
    )
    # TODO - return as object
    return response.content.decode("utf-8")


def get_event_participants(event_id: int, length: int, offset: int) -> List[Participant]:
    """
    Gets the individual participants of an event.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_EVENT_PARTICIPANTS_URL_FMT.format(event_id, length, offset),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()

    return [Participant.from_dict(p) for p in response]

def get_event_teams(event_id: int) -> List[Team]:
    """
    Gets the teams of an event.
    """
    token = UbiTokenManager().nadeo_club_token
    response = requests.get(
        url=GET_EVENT_TEAMS_URL_FMT.format(event_id),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()

    return [Team.from_dict(t) for t in response]

def get_display_name(account_id: str) -> Optional[str]:
    """ 
    Gets the display name for a given account id if exists.
    """
    token = UbiTokenManager().nadeo_prod_token
    response = requests.get(
        url=GET_DISPLAY_NAMES_FMT.format(account_id),
        headers={"Authorization": "nadeo_v1 t=" + token},
    ).json()

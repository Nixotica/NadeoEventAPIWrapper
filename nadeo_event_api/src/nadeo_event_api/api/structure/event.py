from datetime import datetime
from typing import List
import requests

from .enums import ParticipantType
from ...utils import dt_standardize
from .round.spot_structure import SpotStructure
from ...constants import (
    ADD_LOGO_URL_FMT,
    ADD_PARTICIPANT_URL_FMT,
    ADD_TEAM_URL_FMT,
    CREATE_COMP_URL,
    DELETE_COMP_URL_FMT,
    GET_PARTICIPANTS_URL_FMT,
    NADEO_DATE_FMT,
)

from ..authenticate import UbiTokenManager

from .round.round import Round


class Event:
    def __init__(
        self,
        name: str,
        club_id: int,
        rounds: List[Round],
        description: str = None,
        registration_start_date: datetime = None,
        registration_end_date: datetime = None,
        participant_type: ParticipantType = ParticipantType.PLAYER,
    ):
        self._name = name
        self._club_id = club_id
        self._rounds = rounds
        self._description = description
        self._registration_start_date = dt_standardize(registration_start_date) if registration_start_date else None
        self._registration_end_date = dt_standardize(registration_end_date) if registration_end_date else None
        self._participant_type = participant_type

        self._registered_id = None
        """ The ID this event is registered under in Nadeo's database. None if not registered. """

        self._live_id = None
        """ The LiveID this event is registered under in NadeoClubServices. """

        self._personal_logo_url = None
        """ The URL of the logo that was posted to this event. This is the source of the logo, not the address stored by the event in Nadeo services. """

        self._registered_logo_url = None
        """ The URL of the logo for this event. This will be stored in s3 after it's posted to the event. """

    def post(self) -> None:
        """
        Posts the event if valid.
        """
        if not self.valid():
            print("Event is not valid, and therefore will not post.")
            return
        token = UbiTokenManager().nadeo_club_token
        response = requests.post(
            url=CREATE_COMP_URL,
            headers={"Authorization": "nadeo_v1 t=" + token},
            json=self._as_jsonable_dict(),
        ).json()
        if "exception" in response:
            print("Failed to post event: ", response)
            return
        self._registered_id = response["competition"]["id"]
        self._live_id = response["competition"]["liveId"]
        print(
            f"Your event is viewable at https://www.trackmania.com/competition/{self._registered_id}"
        )

    def delete(self) -> None:
        """
        Deletes this event.
        """
        if not self._registered_id:
            print("Could not delete event since it hasn't been posted.")
            return
        token = UbiTokenManager().nadeo_club_token
        requests.post(
            url=DELETE_COMP_URL_FMT.format(self._registered_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
        )
        self._registered_id = None

    def add_participant(self, player_uuid: str, seed: int) -> None:
        """
        Adds a participant to the event.

        :param player_uuid: The account ID of the player (found on trackmania.io)
        :param seed: The seed of the player for the event (starts at 1)
        """
        if not self._registered_id:
            print("Could not add participant to event since it hasn't been posted.")
            return
        if self._participant_type != ParticipantType.PLAYER:
            print("Could not add participant since this event is not type PLAYER")
            return
        if seed == 0:
            print(
                "WARNING! You tried adding a player with seed zero, they will not be part of the event. Start at 1."
            )
            return
        token = UbiTokenManager().nadeo_club_token
        requests.post(
            url=ADD_PARTICIPANT_URL_FMT.format(self._registered_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
            json={"participant": player_uuid, "seed": seed},
        )

    def get_participants(self) -> List[str]:
        """
        Gets the participants registered to the event.

        :returns: A list of player UUIDs
        """
        if not self._registered_id:
            print("Could not get participants from event since it hasn't been posted.")
            return
        return Event.get_participants_from_id(self._registered_id)

    def add_team(self, name: str, members: List[str], seed: int) -> None:
        """
        Adds a team to the event.

        :param name: The name of the team
        :param members: The list of account IDs of the players in the team (found on trackmania.io)
        :param seed: The seed of the team for the event (starts at 1)
        """
        if not self._registered_id:
            print("Could not add participant to event since it hasn't been posted.")
            return
        if self._participant_type != ParticipantType.TEAM:
            print("Could not add team since this event is not type TEAM")
            return
        token = UbiTokenManager().nadeo_club_token
        members = [{"member": member} for member in members]
        requests.post(
            url=ADD_TEAM_URL_FMT.format(self._registered_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
            json={"id": name, "name": name, "seed": seed, "members": members},
        )

    def add_logo(self, logo_url: str) -> None:
        """
        Adds a logo to the event. 

        :param logo_url: The URL of the logo. 
        """
        if not self._registered_id:
            print("Could not add logo to event since it hasn't been posted.")
            return
        response = requests.get(logo_url)
        if response.status_code != 200:
            print(f"Failed to download logo from url: {logo_url}")
            return
        token = UbiTokenManager().nadeo_club_token
        response = requests.post(
            url=ADD_LOGO_URL_FMT.format(self._registered_id),
            headers={"Authorization": "nadeo_v1 t=" + token, "Content-Type": "application/binary"},
            data=response.content,
        ).json()
        self._personal_logo_url = logo_url
        self._registered_logo_url = response

    @staticmethod
    def delete_from_id(event_id: int) -> None:
        """
        Deletes the event with the given ID.

        :param event_id: The ID of the event to delete.
        """
        token = UbiTokenManager().nadeo_club_token
        requests.post(
            url=DELETE_COMP_URL_FMT.format(event_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
        )

    @staticmethod
    def get_participants_from_id(event_id: int) -> List[str]:
        # TODO return type Participant 
        token = UbiTokenManager().nadeo_club_token
        response = requests.get(
            url=GET_PARTICIPANTS_URL_FMT.format(event_id, 0, 50), # TODO pagination support
            headers={"Authorization": "nadeo_v1 t=" + token},
        ).json()
        uuids = []
        for participant_info in response:
            uuids.append(participant_info['participant'])
        return uuids

    def _as_jsonable_dict(self) -> dict:
        """
        Returns the event as a JSON-able dictionary.
        """
        event = {}
        event["name"] = self._name
        event["clubId"] = self._club_id
        event["description"] = self._description
        event["registrationStartDate"] = (
            self._registration_start_date.strftime(NADEO_DATE_FMT)
            if self._registration_start_date
            else None
        )
        event["registrationEndDate"] = (
            self._registration_end_date.strftime(NADEO_DATE_FMT)
            if self._registration_end_date
            else None
        )
        event["rounds"] = [round.as_jsonable_dict() for round in self._rounds]
        for i in range(len(self._rounds)):
            event["rounds"][i]["position"] = i
        event["rulesUrl"] = None
        event["spotStructure"] = SpotStructure(self._rounds).as_jsonable_dict()
        event["startDate"] = ""
        event["maxPlayers"] = 10000
        event["allowedZone"] = ""
        event["participantType"] = self._participant_type.value
        return event

    def valid(self) -> bool:
        """
        Ensures that event is valid to post. This is because we get very little
        insight as to why the event is invalid from the response, so we need to check
        against what we know is allowed/disallowed.

        :returns: True if valid, False otherwise.
        """
        now = dt_standardize(datetime.utcnow())
        if self._registration_start_date and self._registration_end_date:
            if now > self._registration_start_date or now > self._registration_end_date:
                print("Event registration must be later than current time.")
                return False
            if self._registration_start_date > self._registration_end_date:
                print("Event registration start must be before end.")
                return False
        elif self._registration_start_date or self._registration_end_date:
            print("Event registration start and end must be specified together.")
            return False
        else:
            if self._rounds[0]._qualifier is not None:
                print(
                    "Event with qualifier must have a registration period, else it won't start the match automatically. You've been warned!"
                )

        if len(self._name) > 16:
            print("Event name is probably too long and will break.")
            return False

        for round_idx in range(len(self._rounds)):
            if not self._rounds[round_idx].valid():
                print(f"Round {round_idx} is invalid.")
                return False
            if round_idx > 0:
                if self._rounds[round_idx - 1]._end_date >= self._rounds[round_idx]._start_date:
                    print(f"Round {round_idx - 1} must end ({self._rounds[round_idx - 1]._end_date}) before the next begins ({self._rounds[round_idx]._start_date}).")
                    return False
                if self._rounds[round_idx]._qualifier is not None:
                    print(f"Round {round_idx} has a qualifier, but only the first round may have one.")
                    return False

        # TODO check that maps are real

        # TODO check that matches requiring outcomes from previous rounds have ends before this match starts

        # TODO check that club id belongs to authorized user

        return True

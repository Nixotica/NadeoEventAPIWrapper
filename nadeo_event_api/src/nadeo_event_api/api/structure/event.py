from datetime import datetime
from typing import List
import requests

from nadeo_event_api.api.structure.enums import ParticipantType
from .round.spot_structure import SpotStructure
from ...constants import (
    ADD_PARTICIPANT_URL_FMT,
    ADD_TEAM_URL_FMT,
    CREATE_COMP_URL,
    DELETE_COMP_URL_FMT,
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
        self._registration_start_date = registration_start_date
        self._registration_end_date = registration_end_date
        self._participant_type = participant_type

        self._registered_id = None
        """ The ID this event is registered under in Nadeo's database. None if not registered. """

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
        self._registered_id = response["competition"]["id"]
        print(
            f"Your event is viewable at https://admin.trackmania.nadeo.club/competition/{self._registered_id}"
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
        """
        if not self._registered_id:
            print("Could not add participant to event since it hasn't been posted.")
            return
        if self._participant_type != ParticipantType.PLAYER:
            print("Could not add participant since this event is not type PLAYER")
            return
        token = UbiTokenManager().nadeo_club_token
        requests.post(
            url=ADD_PARTICIPANT_URL_FMT.format(self._registered_id),
            headers={"Authorization": "nadeo_v1 t=" + token},
            json={"participant": player_uuid, "seed": seed},
        )

    def add_team(self, name: str, members: List[str], seed: int) -> None:
        """
        Adds a team to the event.
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
            json={"id": name, "name": name, "seed": seed, "members": members}
        )

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

    """
    TODO Get the registered players from original competition (static method)
    get_participants_url = f"https://competition.trackmania.nadeo.club/api/competitions/{comp_id}/participants?offset=0&length=50"
    """

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
        now = datetime.utcnow()
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

        if len(self._name) > 16:
            print("Event name is probably too long and will break.")
            return False
        
        for round_idx in range(len(self._rounds)):
            if not self._rounds[round_idx].valid():
                print(f"Round {round_idx} is invalid.")
                return False
            if round_idx > 0:
                if self._rounds[round_idx - 1]._end_date >= self._rounds[round_idx]._start_date:
                    print(f"Round {round_idx - 1} must end before the next begins.")
                    return False
                if self._rounds[round_idx]._qualifier is not None:
                    print(f"Round {round_idx} has a qualifier, but is not the first.")
                    return False

        # TODO check that maps are real

        # TODO check that matches requiring outcomes from previous rounds have ends before this match starts

        # TODO check that club id belongs to authorized user

        return True

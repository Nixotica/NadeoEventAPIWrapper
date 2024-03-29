from abc import ABC

from ..enums import SpotType


class MatchSpot(ABC):
    def __init__(
        self,
        spot_type: SpotType,
    ):
        self._spot_type = spot_type


class QualificationMatchSpot(MatchSpot):
    def __init__(
        self,
        round_position: int,
        rank: int,
    ):
        super().__init__(SpotType.QUALIFICATION)
        self._round_position = round_position
        self._rank = rank

    def as_jsonable_dict(self) -> dict:
        spot = {}
        spot["spotType"] = self._spot_type.value
        spot["roundPosition"] = self._round_position
        spot["rank"] = self._rank
        return spot


class SeedMatchSpot(MatchSpot):
    def __init__(
        self,
        seed: int,
    ):
        """
        A match spot based on event seed. Event seed is determined at the start of a competition
        by either a qualifier or adding participants with seed explicitly.

        :param seed: The seed of the player in the event (first seed is 1).
        """
        super().__init__(SpotType.SEED)
        self._seed = seed

    def as_jsonable_dict(self) -> dict:
        spot = {}
        spot["spotType"] = self._spot_type.value
        spot["seed"] = self._seed
        return spot


class CompetitionMatchSpot(MatchSpot):
    def __init__(
        self,
        rank: int,
    ):
        super().__init__(SpotType.COMPETITION)
        self._rank = rank

    def as_jsonable_dict(self) -> dict:
        spot = {}
        spot["spotType"] = self._spot_type.value
        spot["rank"] = self._rank
        return spot


class TeamMatchSpot(MatchSpot):
    def __init__(
        self,
        seed: int,
    ):
        super().__init__(SpotType.TEAM)
        self._seed = seed

    def as_jsonable_dict(self) -> dict:
        spot = {}
        spot["spotType"] = self._spot_type.value
        spot["seed"] = self._seed
        return spot


class MatchParticipantMatchSpot(MatchSpot):
    def __init__(
        self,
        round_position: int,
        match_position: int,
        rank: int,
    ):
        super().__init__(SpotType.MATCH)
        self._round_position = round_position
        self._match_position = match_position
        self._rank = rank

    def as_jsonable_dict(self) -> dict:
        spot = {}
        spot["spotType"] = self._spot_type.value
        spot["roundPosition"] = self._round_position
        spot["matchPosition"] = self._match_position
        spot["rank"] = self._rank
        return spot

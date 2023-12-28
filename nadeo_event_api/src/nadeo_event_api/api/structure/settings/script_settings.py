from abc import ABC


# TODO add all these settings https://wiki.trackmania.io/en/dedicated-server/Usage/OfficialGameModesSettings
class ScriptSettings(ABC):
    def __init__(
        self,
    ):
        pass

    def as_jsonable_dict(self) -> dict:
        return {}


# TODO temporary class, will be split into rounds, cup, etc
class ClassicScriptSettings(ScriptSettings):
    def __init__(
        self,
        points_repartition: str = "",  # TODO take in as list of int
        points_limit: int = 100,
        finish_timeout: int = -1,
        rounds_per_map: int = 5,
        number_of_winners: int = 3,
        warmup_number: int = 1,
        warmup_duration: int = 120,
    ):
        super().__init__()

        self._points_repartition = points_repartition
        self._points_limit = points_limit
        self._finish_timeout = finish_timeout
        self._rounds_per_map = rounds_per_map
        self._number_of_winners = number_of_winners
        self._warmup_number = warmup_number
        self._warmup_duration = warmup_duration

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_PointsRepartition"] = self._points_repartition
        script_settings["S_PointsLimit"] = self._points_limit
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        script_settings["S_NbOfWinners"] = self._number_of_winners
        script_settings["S_WarmUpNb"] = self._warmup_number
        script_settings["S_WarmUpDuration"] = self._warmup_duration
        return script_settings


class TimeAttackScriptSettings(ScriptSettings):
    def __init__(
        self,
        time_limit: int = 300,
        warmup_number: int = 1,
        warmup_duration: int = 15,
        force_laps_number: int = 0,
    ):
        super().__init__()

        self._time_limit = time_limit
        self._warmup_number = warmup_number
        self._warmup_duration = warmup_duration
        self._force_laps_number = force_laps_number

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_TimeLimit"] = self._time_limit
        script_settings["S_WarmUpNb"] = self._warmup_number
        script_settings["S_WarmUpDuration"] = self._warmup_duration
        script_settings["S_ForceLapsNb"] = self._force_laps_number
        return script_settings


class CupSpecialScriptSettings(ClassicScriptSettings):
    def __init__(
        self,
        points_repartition: str = "",  # TODO take in as list of int
        points_limit: int = 100,
        finish_timeout: int = -1,
        rounds_per_map: int = 5,
        number_of_winners: int = 3,
        warmup_number: int = 1,
        warmup_duration: int = 120,
        match_points_limit: int = 2,
        cup_points_limit: int = 2,
        ko_checkpoint_number: int = 0,
    ):
        super().__init__(
            points_repartition=points_repartition,
            points_limit=points_limit,
            finish_timeout=finish_timeout,
            rounds_per_map=rounds_per_map,
            number_of_winners=number_of_winners,
            warmup_number=warmup_number,
            warmup_duration=warmup_duration,
        )

        # TODO separate out into Cup[Short/Long/Classic]ScriptSettings if appropriate
        self._match_points_limit = match_points_limit
        self._cup_points_limit = cup_points_limit
        self._ko_checkpoint_number = ko_checkpoint_number

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_MatchPointsLimit"] = self._match_points_limit
        script_settings["S_CupPointsLimit"] = self._cup_points_limit
        script_settings["S_KOCheckpointNb"] = self._ko_checkpoint_number
        return script_settings

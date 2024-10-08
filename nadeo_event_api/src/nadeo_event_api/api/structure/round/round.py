from datetime import datetime
from typing import List

from nadeo_event_api.utils import dt_standardize
from ....constants import NADEO_DATE_FMT
from .match import Match
from .qualifier import Qualifier
from ..enums import (
    LeaderboardType,
    PluginType,
    ScriptType,
)
from ..maps import Map
from ...structure.settings.plugin_settings import ClassicPluginSettings, PluginSettings
from ...structure.settings.script_settings import CupScriptSettings, ScriptSettings


class RoundConfig:
    def __init__(
        self,
        map_pool: List[Map],
        script: ScriptType,
        max_players: int,
        max_spectators: int = 32,
        plugin: PluginType = PluginType.EMPTY,
        script_settings: ScriptSettings = CupScriptSettings(),
        plugin_settings: PluginSettings = ClassicPluginSettings(),
    ):
        self._map_pool = map_pool
        self._script = script
        self._max_players = max_players
        self._max_spectators = max_spectators
        self._plugin = plugin
        self._script_settings = script_settings
        self._plugin_settings = plugin_settings

    def as_jsonable_dict(self) -> dict:
        """
        Returns the round config as a JSON-able dictionary.
        """
        config = {}
        config["maps"] = [map._uuid for map in self._map_pool]
        config["script"] = self._script.value
        config["maxPlayers"] = self._max_players
        config["maxSpectators"] = self._max_spectators
        config["plugin"] = self._plugin.value
        config["pluginSettings"] = self._plugin_settings.as_jsonable_dict()
        config["scriptSettings"] = self._script_settings.as_jsonable_dict()
        return config


class Round:
    def __init__(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        matches: List[Match],
        config: RoundConfig,
        qualifier: Qualifier = None,
    ):
        self._name = name
        self._start_date = dt_standardize(start_date)
        self._end_date = dt_standardize(end_date)
        self._matches = matches
        self._leaderboard_type = (
            LeaderboardType.BRACKET
        )  # It seems like rounds only support this type...
        self._config = config
        self._qualifier = qualifier
        self._team_leaderboard_type = "TEAM_SCORE"  # TODO figure out what this is

    def as_jsonable_dict(self) -> dict:
        """
        Returns the round as a JSON-able dictionary.
        """
        round = {}
        round["name"] = self._name
        round["startDate"] = self._start_date.strftime(NADEO_DATE_FMT)
        round["endDate"] = self._end_date.strftime(NADEO_DATE_FMT)
        round["nbMatches"] = len(self._matches)
        round["leaderboardType"] = self._leaderboard_type.value
        round["config"] = self._config.as_jsonable_dict()
        round["config"]["name"] = self._name
        round["qualifier"] = (
            self._qualifier.as_jsonable_dict() if self._qualifier else None
        )
        round["teamLeaderboardType"] = self._team_leaderboard_type
        return round

    def valid(self) -> bool:
        """
        Ensures that the round is valid.

        :returns: True if valid, False otherwise.
        """
        if self._qualifier is not None:
            if not self._qualifier.valid():
                print("Qualifier is invalid.")
                return False

        if self._end_date <= self._start_date:
            print("Round end date must be after start date.")
            return False

        return True

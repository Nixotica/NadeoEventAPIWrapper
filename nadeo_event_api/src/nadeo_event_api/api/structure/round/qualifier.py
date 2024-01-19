from datetime import datetime
from typing import List

from nadeo_event_api.utils import dt_standardize

from ...structure.settings.plugin_settings import PluginSettings, QualifierPluginSettings
from ...structure.settings.script_settings import (
    ScriptSettings,
    TimeAttackScriptSettings,
)
from ....constants import NADEO_DATE_FMT
from ...structure.maps import Map
from ...structure.enums import (
    LeaderboardType,
    PluginType,
    ScriptType,
)


class QualifierConfig:
    def __init__(
        self,
        map_pool: List[Map],
        script: ScriptType,
        max_players: int = 64,
        max_spectators: int = 64,
        plugin: PluginType = PluginType.EMPTY,
        script_settings: ScriptSettings = TimeAttackScriptSettings(),
        plugin_settings: PluginSettings = QualifierPluginSettings(),
    ):
        self._map_pool = map_pool
        self._script = script
        self._max_players = max_players
        self._max_spectators = max_spectators
        self._plugin = plugin
        self._script_settings = script_settings
        self._plugin_settings = plugin_settings

    def as_jsonable_dict(self) -> dict:
        config = {}
        config["maps"] = [map._uuid for map in self._map_pool]
        config["script"] = self._script.value
        config["plugin"] = self._plugin.value
        config["maxPlayers"] = self._max_players
        config["maxSpectators"] = self._max_spectators
        config["pluginSettings"] = self._plugin_settings.as_jsonable_dict()
        config["scriptSettings"] = self._script_settings.as_jsonable_dict()
        return config


# TODO this shares a lot with round, minus matches and qualifier
# so find some way to consolidate that
class Qualifier:
    def __init__(
        self,
        name: str,
        start_date: datetime,
        end_date: datetime,
        leaderboard_type: LeaderboardType,
        config: QualifierConfig,
    ):
        self._name = name
        self._start_date = dt_standardize(start_date)
        self._end_date = dt_standardize(end_date)
        self._leaderboard_type = leaderboard_type
        self._config = config

    def as_jsonable_dict(self) -> dict:
        """
        Returns the qualifier as a JSON-able dictionary.
        """
        qualifier = {}
        qualifier["name"] = self._name
        qualifier["startDate"] = self._start_date.strftime(NADEO_DATE_FMT)
        qualifier["endDate"] = self._end_date.strftime(NADEO_DATE_FMT)
        qualifier["leaderboardType"] = self._leaderboard_type.value
        qualifier["position"] = 0
        qualifier["id"] = None
        qualifier["config"] = self._config.as_jsonable_dict()
        qualifier["config"]["name"] = self._name
        qualifier["isQualification"] = True
        return qualifier

    def valid(self) -> bool:
        """
        Ensures that qualifier is valid.

        :returns: True if valid, False otherwise.
        """

        if self._end_date <= self._start_date:
            print("Qualifier end date must be after start date.")
            return False

        return True

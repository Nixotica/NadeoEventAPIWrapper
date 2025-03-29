from abc import ABC
from typing import Dict, Optional

from nadeo_event_api.objects.outbound.settings.pick_ban_style import PickBanStyle

from ...structure.enums import RespawnBehavior

# Nadeo api documentation: https://wiki.trackmania.io/en/dedicated-server/Usage/OfficialGameModesSettings


class BaseScriptSettings:
    def __init__(
        self,
        chat_time: int = 10,
        force_laps_number: int = -1,
        respawn_behavior: RespawnBehavior = RespawnBehavior.DEFAULT,
        warmup_duration: int = 0,
        warmup_number: int = 0,
        warmup_timeout: int = -1,
        pick_ban_enable: bool = False,
    ):
        """
        Base settings shared by all game modes. - Declares the list of script settings to use in a round.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.
        """
        self._chat_time = chat_time
        self._force_laps_number = force_laps_number
        self._respawn_behavior = respawn_behavior
        self._warmup_duration = warmup_duration
        self._warmup_number = warmup_number
        self._warmup_timeout = warmup_timeout
        self._pick_ban_enable = pick_ban_enable


class BaseTMWTScriptSettings:
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        teams_url: Optional[str] = None,
        match_points_limit: int = 2,
        match_info: Optional[str] = None,
    ) -> None:
        """Base settings shared by all TMWT game modes. - Declares the list of script settings to use in a round.

        Args:
            base_script_settings (BaseScriptSettings, optional): The base script settings to use. Defaults to BaseScriptSettings().
            teams_url (Optional[str], optional): URL to a raw json-compatible file (example: https://pastebin.com/raw/n6sDFhPu). Defaults to None.
            match_points_limit (int, optional): How many map wins are needed to win a match. Defaults to 2.
            match_info (Optional[str], optional): Match info to display at the top bar of the game. Defaults to None.
        """
        self._base_script_settings = base_script_settings
        self._teams_url = teams_url
        self._match_points_limit = match_points_limit
        self._match_info = match_info
        

class ScriptSettings(ABC):
    def __init__(self, base_script_settings: BaseScriptSettings = BaseScriptSettings()):
        """
        Declares the list of script settings to use in a round.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.
        """
        self.base_script_settings = base_script_settings

    def as_jsonable_dict(self) -> dict:
        script_settings = {}
        script_settings["S_ChatTime"] = self.base_script_settings._chat_time
        script_settings["S_ForceLapsNb"] = self.base_script_settings._force_laps_number
        script_settings[
            "S_RespawnBehaviour"
        ] = self.base_script_settings._respawn_behavior.value
        script_settings["S_WarmUpDuration"] = self.base_script_settings._warmup_duration
        script_settings["S_WarmUpNb"] = self.base_script_settings._warmup_number
        script_settings["S_WarmUpTimeout"] = self.base_script_settings._warmup_timeout
        script_settings[
            "S_PickAndBan_Enable"
        ] = self.base_script_settings._pick_ban_enable

        return script_settings

class TMWTScriptSettings(ScriptSettings):
    def __init__(self, tmwt_script_settings: BaseTMWTScriptSettings = BaseTMWTScriptSettings()) -> None:
        """Declares TMWT script settings shared by all TMWT game modes. 

        Args:
            tmwt_script_settings (BaseTMWTScriptSettings, optional): The base TMWT script settings to use. Defaults to BaseTMWTScriptSettings().
        """
        super().__init__(tmwt_script_settings._base_script_settings)
        self._tmwt_script_settings = tmwt_script_settings

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()

        # NOTE: THIS WILL BREAK AND REJECT POSTING THE EVENT IF YOU PUT "" FOR THIS VALUE
        if self._tmwt_script_settings._teams_url is not None:
            script_settings["S_TeamsUrl"] = self._tmwt_script_settings._teams_url
        
        script_settings["S_MatchPointsLimit"] = self._tmwt_script_settings._match_points_limit
        script_settings["S_MatchInfo"] = self._tmwt_script_settings._match_info

        return script_settings

class ChampionScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        best_lap_bonus_points: int = 2,
        disable_give_up: bool = False,
        finish_timeout: int = 5,
        force_winners_number: int = 0,
        pause_before_round_number: int = 0,
        pause_duration: int = 360,
        points_limit: int = 0,
        points_repartition: str = "20,14,12,10,8,7,6,5,5,4,4,3,3,2,2,1",
        rounds_limit: int = 6,
        rounds_per_map: int = 1,
        rounds_with_phase_change: str = "3,5",
        time_limit: int = -1,
        timeout_players_number: int = 0,
        use_tie_break: bool = False,
    ):
        """
        Declares the list of script settings to use for Champion mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param best_lap_bonus_points: Points bonus attributed to the player with the best lap. Default 2.
        :param disable_give_up: Disable give up, overrides respawn_behavior. Default False.
        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param force_winners_number: Force the number of players who can win points at the end of the round. Set 0 to use winners_ratio. Default 0.
        :param pause_before_round_number: Round with a pause before its start, used in TMGL with the value 4. Set to 0 to disable. Linked to pause_duration. Default 0.
        :param pause_duration: Pause time in seconds. Set to 0 to disable. Linked to pause_before_round_number. Default 360.
        :param points_limit: Limit number of points. 0 = unlimited. Default 0.
        :param points_repartition: Point repartition from first to last. Default 20,14,12,10,8,7,6,5,5,4,4,3,3,2,2,1.
        :param rounds_limit: Number of rounds to play before finding a winner. Default 6.
        :param rounds_per_map: Number of rounds to play on one map before going to the next. -1 or 0: unlimited. Default 1.
        :param rounds_with_phase_change: Rounds with a phase change (opening, semi-final, final like TMGL). It's possible to skip a phase by duplicating a number (e.g. 3,3). Default 3,5.
        :param time_limit: Time limit before going to the next map. 0 or -1 for unlimited time. Default -1.
        :param timeout_players_number: Players crossing finish line before starting finish timeout. Linked to finish_timeout. Default 0.
        :param use_tie_break: Continue to play the map until the tie is broken. Default False.
        """
        super().__init__(base_script_settings)

        self._best_lap_bonus_points = best_lap_bonus_points
        self._disable_give_up = disable_give_up
        self._finish_timeout = finish_timeout
        self._force_winners_number = force_winners_number
        self._pause_before_round_number = pause_before_round_number
        self._pause_duration = pause_duration
        self._points_limit = points_limit
        self._points_repartition = points_repartition
        self._rounds_limit = rounds_limit
        self._rounds_per_map = rounds_per_map
        self._rounds_with_phase_change = rounds_with_phase_change
        self._time_limit = time_limit
        self._timeout_players_number = timeout_players_number
        self._use_tie_break = use_tie_break

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_BestLapBonusPoints"] = self._best_lap_bonus_points
        script_settings["S_DisableGiveUp"] = self._disable_give_up
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_ForceWinnersNb"] = self._force_winners_number
        script_settings["S_PauseBeforeRoundNb"] = self._pause_before_round_number
        script_settings["S_PauseDuration"] = self._pause_duration
        script_settings["S_PointsLimit"] = self._points_limit
        script_settings["S_PointsRepartition"] = self._points_repartition
        script_settings["S_RoundsLimit"] = self._rounds_limit
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        script_settings["S_RoundsWithAPhaseChange"] = self._rounds_with_phase_change
        script_settings["S_TimeLimit"] = self._time_limit
        script_settings["S_TimeOutPlayersNumber"] = self._timeout_players_number
        script_settings["S_UseTieBreak"] = self._use_tie_break
        return script_settings


class CupScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        finish_timeout: int = 5,
        number_of_winners: int = 1,
        points_limit: int = 100,
        points_repartition: str = "10,6,4,3,2,1",
        rounds_per_map: int = 5,
    ):
        """
        Declares the list of script settings to use in Cup mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param number_of_winners: Number of winners in the match. Default 1.
        :param points_limit: Limit number of points to become finalist. Default 100.
        :param points_repartition: Point repartition from first to last. Default 10,6,4,3,2,1.
        :param rounds_per_map: Number of rounds to play on one map before going to the next. -1 or 0: unlimited. Default 5.
        """
        super().__init__(base_script_settings)

        self._finish_timeout = finish_timeout
        self._number_of_winners = number_of_winners
        self._points_limit = points_limit
        self._points_repartition = points_repartition
        self._rounds_per_map = rounds_per_map

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_NbOfWinners"] = self._number_of_winners
        script_settings["S_PointsLimit"] = self._points_limit
        script_settings["S_PointsRepartition"] = self._points_repartition
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        return script_settings


class KnockoutScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        eliminated_players_number_ranks: str = "4,16,16",
        finish_timeout: int = 5,
        match_position: int = -1,
        rounds_per_map: int = -1,
        rounds_without_elimination: int = 1,
    ):
        """
        Declares the list of script settings to use in Knockout mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param eliminated_players_number_ranks: Rank at which one more player is eliminated per round. COTD uses 8,16,16. Default 4,16,16.
        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param match_position: Server number to define global player rank. -1: Disable global ranking. N: Position of the player + N * 64. Default -1.
        :param rounds_per_map: Number of rounds to play on one map before going to the next. -1 or 0: unlimited. Default -1.
        :param rounds_without_elimination: Number of rounds without elimination (like warmup, but only on first map of match). Default 1.
        """
        super().__init__(base_script_settings)

        self._eliminated_players_number_ranks = eliminated_players_number_ranks
        self._finish_timeout = finish_timeout
        self._match_position = match_position
        self._rounds_per_map = rounds_per_map
        self._rounds_without_elimination = rounds_without_elimination

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings[
            "S_EliminatedPlayersNbRanks"
        ] = self._eliminated_players_number_ranks
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_MatchPosition"] = self._match_position
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        script_settings["S_RoundsWithoutElimination"] = self._rounds_without_elimination
        return script_settings


class LapsScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        disable_giveup: bool = False,
        finish_timeout: int = 5,
        time_limit: int = 0,
    ):
        """
        Declares the list of script settings to use in Laps mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param disable_give_up: Disable give up, overrides respawn_behavior. Default False.
        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param time_limit: Time limit before going to the next map. 0 or -1 for unlimited time. Default 0.
        """
        super().__init__(base_script_settings)

        self._disable_giveup = disable_giveup
        self._finish_timeout = finish_timeout
        self._time_limit = time_limit

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_DisableGiveUp"] = self._disable_giveup
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_TimeLimit"] = self._time_limit
        return script_settings


class TeamsScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        cumulate_points: bool = False,
        finish_timeout: int = 5,
        maps_per_match: int | None = None,
        max_points_per_round: int = 6,
        points_gap: int = 0,
        points_limit: int = 5,
        points_repartition: str | None = None,
        rounds_per_map: int = -1,
        use_alternate_rules: bool = True,
        use_tie_break: bool = True,
        winners_ratio: float = 0.5,
    ):
        """
        Declares the list of script settings to use in Teams mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param cumulate_points: Cumulate points earned by players to their team score. Default False.
        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param maps_per_match: Number of maps to play before finishing the match. Set 0 or -1 is equivalent to have only one map. Default None (will keep playing until other match ending condition is met).
        :param max_points_per_round: The maximum number of points attributed to the first player to cross the finish line. Only available when use_custom_points_repartition is set to False. Default 6.
        :param points_gap: The number of points lead a team must have to win the map. Default 0.
        :param points_limit: Limit number of points for team to win. Default 5.
        :param points_repartition: Point repartition from first to last. Default None (1,0).
        :param rounds_per_map: Number of rounds to play on one map before going to the next. -1 or 0: unlimited. Default -1.
        :param use_alternate_rules: False: Give 1 point to all first players of a team. True: Use the equation [min(max_points_per_round, num_players) - position - 1]. This setting is ignored if points_repartition is specified.
        :param use_tie_break: Continue to play the map until the tie is broken. Default True.
        :param winners_ratio: Ratio of players who will win points.
        """
        super().__init__(base_script_settings)

        self._cumulate_points = cumulate_points
        self._finish_timeout = finish_timeout
        self._maps_per_match = maps_per_match
        self._max_points_per_round = max_points_per_round
        self._points_gap = points_gap
        self._points_limit = points_limit
        self._points_repartition = points_repartition
        self._rounds_per_map = rounds_per_map
        self._use_alternate_rules = use_alternate_rules
        self._use_tie_break = use_tie_break
        self._winners_ratio = winners_ratio

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_CumulatePoints"] = self._cumulate_points
        script_settings["S_FinishTimeout"] = self._finish_timeout
        if self._maps_per_match is not None:
            script_settings["S_MapsPerMatch"] = self._maps_per_match
        script_settings["S_MaxPointsPerRound"] = self._max_points_per_round
        script_settings["S_PointsGap"] = self._points_gap
        script_settings["S_PointsLimit"] = self._points_limit
        if self._points_repartition is not None:
            script_settings["S_PointsRepartition"] = self._points_repartition
            script_settings["S_UseCustomPointsRepartition"] = True
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        script_settings["S_UseAlternateRules"] = self._use_alternate_rules
        script_settings["S_UseTieBreak"] = self._use_tie_break
        script_settings["S_WinnersRatio"] = self._winners_ratio
        return script_settings


class TimeAttackScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        time_limit: int = 300,
    ):
        """
        Declares the list of script settings to use in TimeAttack mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param time_limit: Time limit before going to the next map. 0 or -1 for unlimited time. Default 300.
        """
        super().__init__(base_script_settings)

        self._time_limit = time_limit

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_TimeLimit"] = self._time_limit
        return script_settings


class RoundsScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        finish_timeout: int = 5,
        maps_per_match: int | None = None,
        points_limit: int = 50,
        points_repartition: str = "10,6,4,3,2,1",
        rounds_per_map: int = -1,
        use_tie_break: bool = True,
    ):
        """
        Declares the list of script settings to use in Rounds mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param maps_per_match: Number of maps to play before finishing the match. Set 0 or -1 is equivalent to have only one map. Default None (will keep playing until other match ending condition is met).
        :param points_limit: Limit number of points to win. 0 = unlimited. Default 50.
        :param points_repartition: Point repartition from first to last. Default 10,6,4,3,2,1.
        :param rounds_per_map: Number of rounds to play on one map before going to the next. -1 or 0: unlimited. Default -1.
        :param use_tie_break: Continue to play the map until the tie is broken. Default True.
        """
        super().__init__(base_script_settings)

        self._finish_timeout = finish_timeout
        self._maps_per_match = maps_per_match
        self._points_limit = points_limit
        self._points_repartition = points_repartition
        self._rounds_per_map = rounds_per_map
        self._use_tie_break = use_tie_break

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_FinishTimeout"] = self._finish_timeout
        if self._maps_per_match is not None:
            script_settings["S_MapsPerMatch"] = self._maps_per_match
        script_settings["S_PointsLimit"] = self._points_limit
        script_settings["S_PointsRepartition"] = self._points_repartition
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        script_settings["S_UseTieBreak"] = self._use_tie_break
        return script_settings


class CupSpecialScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        finish_timeout: int = 5,
        number_of_winners: int = 1,
        points_limit: int = 100,
        points_repartition: str = "10,6,4,3,2,1",
        rounds_per_map: int = 5,
        match_points_limit: int | None = None,
        cup_points_limit: int | None = None,
        ko_checkpoint_number: int | None = None,
        enable_ambient_sound: bool = False,
        hide_scores_header: bool = False,
        # TODO S_OverridePlayerProfiles as raw text json file for team + player names
    ):
        """
        Declares the list of script settings to use in Cup mode.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param finish_timeout: Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default 5.
        :param number_of_winners: Number of winners in the match. Default 1.
        :param points_limit: Limit number of points to win. Only applies to CupClassic Default 100.
        :param points_repartition: Point repartition from first to last. Default 10,6,4,3,2,1.
        :param rounds_per_map: Number of rounds to play on one map before going to the next. -1 or 0: unlimited. Default 5.

        :param match_points_limit: How many map wins are needed to win a match. Default 2.
        :param cup_points_limit: Limit number of points to win a map. Players become finalist at n-1. Default 2.
        :param ko_checkpoint_number: Number of checkpoints before Win-by-KO is triggered. Set to 0 to disabled. Default 0.
        :param enable_ambient_sound: Enables crowd sounds in spectator. Default False.
        :param hide_scores_header: True: Move total points to left panel instead of top. False: Keep total points at top. Default False.
        """
        super().__init__(base_script_settings)

        self._finish_timeout = finish_timeout
        self._number_of_winners = number_of_winners
        self._points_limit = points_limit
        self._points_repartition = points_repartition
        self._rounds_per_map = rounds_per_map

        self._match_points_limit = match_points_limit
        self._cup_points_limit = cup_points_limit
        self._ko_checkpoint_number = ko_checkpoint_number
        self._enable_ambient_sound = enable_ambient_sound
        self._hide_scores_header = hide_scores_header

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_NbOfWinners"] = self._number_of_winners
        script_settings["S_PointsLimit"] = self._points_limit
        script_settings["S_PointsRepartition"] = self._points_repartition
        script_settings["S_RoundsPerMap"] = self._rounds_per_map
        if self._match_points_limit is not None:
            script_settings["S_MatchPointsLimit"] = self._match_points_limit
        if self._cup_points_limit is not None:
            script_settings["S_CupPointsLimit"] = self._cup_points_limit
        if self._ko_checkpoint_number is not None:
            script_settings["S_KOCheckpointNb"] = self._ko_checkpoint_number
        script_settings["S_EnableAmbientSound"] = self._enable_ambient_sound
        script_settings["S_HideScoresHeader"] = self._hide_scores_header
        return script_settings


class TMWC2023ScriptSettings(TMWTScriptSettings):
    def __init__(
        self,
        base_tmwt_script_settings: BaseTMWTScriptSettings = BaseTMWTScriptSettings(),
        crash_detection_threshold: int = 1000,
    ) -> None:
        """Creates TMWC 2023 script settings with default settings, allowing for overrides.

        Args:
            base_tmwt_script_settings (TMWTScriptSettings, optional): Shared TMWT mode script settings. Defaults to TMWTScriptSettings().
            crash_detection_threshold (int, optional): Time in milliseconds for a round to count as a crash for a player from first place. Default 1000.
        """

        super().__init__(base_tmwt_script_settings)

        self._crash_detection_threshold = crash_detection_threshold

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()

        script_settings["S_CrashDetectionThreshold"] = self._crash_detection_threshold

        return script_settings


class TMWT2025ScriptSettings(TMWTScriptSettings):
    def __init__(
        self,
        base_tmwt_script_settings: BaseTMWTScriptSettings = BaseTMWTScriptSettings(),
        map_points_limit: int = 10,
        finish_timeout: int = -1,
        loading_screen_image_url: str = "",
        sponsors_url: str = "",
        header_logo_url: str = "",
        intro_background_url: str = "",
        intro_logo_url: str = "",
        sign_2x3_default_url: str = "file://Media/Manialinks/Nadeo/Trackmania/Modes/TMWT/Sign2x3/Default.dds",
        sign_16x9_default_url: str = "",
        sign_64x10_default_url: str = "file://Media/Manialinks/Nadeo/Trackmania/Modes/TMWT/Sign64x10/Default.dds",
        disable_match_intro: bool = False,
        force_road_spectators_number: int = -1,
        enable_dossard_color: bool = True,
        is_matchmaking: bool = True,
        pick_ban_style: PickBanStyle = PickBanStyle(),
        api_url: str = "",
        api_competition_uid: str = "",
        api_authorization_header: str = "",
    ) -> None:
        """Creates TMWT 2025 script settings with default settings, allowing for overrides.

        Args:
            base_tmwt_script_settings (TMWTScriptSettings, optional): Shared TMWT mode script settings. Defaults to TMWTScriptSettings().
            map_points_limit (int, optional): Number of points to win a map. Default 10.
            finish_timeout (int, optional): Time to finish the round in seconds after the winner. Use -1 to base on AT (5 sec + AT / 6). Default -1.
            loading_screen_image_url (str, optional): URL to an image to display during the loading screen between tracks. Default "".
            sponsors_url (str, optional): A list of URLs, separated by spaces (` `), to images to display in the upper right corner of the viewer's screen. Default "".
            header_logo_url (str, optional): URL to an image that will be displayed as a logo in the header at the top of the screen during the match. Default "".
            intro_background_url (str, optional): URL to an image that will be displayed as a logo in the header at the top of the screen during the match. Default "".
            intro_logo_url (str, optional): URL to an image that will be displayed as a logo during the intro sequence at the start of the match. Default "".
            sign_2x3_default_url (str, optional): URL to an image that will be displayed in the 2x3 signs of the stadium if the targeted player team does not have a custom image. Default "file://Media/Manialinks/Nadeo/Trackmania/Modes/TMWT/Sign2x3/Default.dds".
            sign_16x9_default_url (str, optional): URL to an image that will be displayed in the 16x9 signs of the stadium if the targeted player team does not have a custom image. Default "".
            sign_64x10_default_url (str, optional): URL to an image that will be displayed in the checkpoint/start/finish signs if the targeted player team does not have a custom image. Default "file://Media/Manialinks/Nadeo/Trackmania/Modes/TMWT/Sign64x10/Default.dds".
            disable_match_intro: (bool, optional): Disable the intro sequence at the beginning of the match that displays team information. Default False.
            force_road_spectators_number (int, optional): Set the number of spectators displayed in the stand blocks. A negative value keeps the server default value. Default -1.
            enable_dossard_color (bool, optional): Use the team color on the trigram and rank displayed on the back of the car. Default True.
            is_matchmaking (bool, optional): Set to `True` if the server is managed by the official Trackmania competition tool. Set to `False` if you are using your own dedicated server. Default True.
            pick_ban_style: (PickBanStyle, optional): A JSON string containing the URL to the images dispalyed in the pick and ban screen. Default  { "Background": "", "TopLeftLogo": "", "TopRightLogo": "", "BottomLogo": "" }.
            api_url (str, optional): URL of the player statistics API (win rate, crash rate, etc). Default "".
            api_competition_uid (str, optional): Custom identifier used to separate statistics for different events. Default "".
            api_authorization_header (str, optional): Value of the authorization header added to the API requests. Default "".
        """

        super().__init__(base_tmwt_script_settings)

        self._map_points_limit = map_points_limit
        self._finish_timeout = finish_timeout
        self._loading_screen_image_url = loading_screen_image_url
        self._sponsors_url = sponsors_url
        self._header_logo_url = header_logo_url
        self._intro_background_url = intro_background_url
        self._intro_logo_url = intro_logo_url
        self._sign_2x3_default_url = sign_2x3_default_url
        self._sign_16x9_default_url = sign_16x9_default_url
        self._sign_64x10_default_url = sign_64x10_default_url
        self._disable_match_intro = disable_match_intro
        self._force_road_spectators_number = force_road_spectators_number
        self._enable_dossard_color = enable_dossard_color
        self._is_matchmaking = is_matchmaking
        self._pick_ban_style = pick_ban_style
        self._api_url = api_url
        self._api_competition_uid = api_competition_uid
        self._api_authorization_header = api_authorization_header

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()

        script_settings["S_MapPointsLimit"] = self._map_points_limit
        script_settings["S_FinishTimeout"] = self._finish_timeout
        script_settings["S_LoadingScreenImageUrl"] = self._loading_screen_image_url
        script_settings["S_SponsorsUrl"] = self._sponsors_url
        script_settings["S_HeaderLogoUrl"] = self._header_logo_url
        script_settings["S_IntroBackgroundUrl"] = self._intro_background_url
        script_settings["S_IntroLogoUrl"] = self._intro_logo_url
        script_settings["S_Sign2x3DefaultUrl"] = self._sign_2x3_default_url
        script_settings["S_Sign16x9DefaultUrl"] = self._sign_16x9_default_url
        script_settings["S_Sign64x10DefaultUrl"] = self._sign_64x10_default_url
        script_settings["S_DisableMatchIntro"] = self._disable_match_intro
        script_settings["S_ForceRoadSpectatorsNb"] = self._force_road_spectators_number
        script_settings["S_EnableDossardColor"] = self._enable_dossard_color
        script_settings["S_IsMatchmaking"] = self._is_matchmaking
        script_settings["S_PickAndBanStyle"] = self._pick_ban_style.as_jsonable_string()
        script_settings["S_ApiUrl"] = self._api_url
        script_settings["S_ApiCompetitionUid"] = self._api_competition_uid
        script_settings["S_ApiAuthorizationHeader"] = self._api_authorization_header

        return script_settings
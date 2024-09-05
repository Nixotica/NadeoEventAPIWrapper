from abc import ABC

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


class TMWTScriptSettings(ScriptSettings):
    def __init__(
        self,
        base_script_settings: BaseScriptSettings = BaseScriptSettings(),
        crash_detection_threshold: int = 1000,
        match_points_limit: int = 2,
    ):
        """
        Declares the list of script settings to use in a round.

        :param chat_time: Chat time at the end of a map or match. Default 10.
        :param force_laps_number: Number of laps per round. -1: Use laps from map settings. 0: Independent laps (TimeAttack). 1+: Number of laps. Default is from laps map settings.
        :param respawn_behavior: Respawn behavior. Default is standard respawn behavior for the chosen gamemode.
        :param warmup_duration: Time in seconds of the warmup. 0: Time based on the AT (5 sec + AT on 1 lap + (AT on 1 lap / 6)). -1: Only one round attempt (give up ends WU for player). Default 0.
        :param warmup_number: Number of warmup rounds. Default 0.
        :param warmup_timeout: Time to finish in seconds after the winners, equivalent of finish_timeout but for warmup, only if warmup_duration is -1. -1: Time based on AT (5 sec + AT / 6). Default -1.
        :param pick_ban_enable: Enable pick and ban. Defining a pick ban order in plugin settings without this enabled will not enable it.

        :param crash_detection_threshold: Time in milliseconds for a round to count as a crash for a player from first place. Default 1000.
        :param match_points_limit: How many map wins are needed to win a match. Default 2.
        """

        super().__init__(base_script_settings)

        self._crash_detection_threshold = crash_detection_threshold
        self._match_points_limit = match_points_limit

    def as_jsonable_dict(self) -> dict:
        script_settings = super().as_jsonable_dict()
        script_settings["S_CrashDetectionThreshold"] = self._crash_detection_threshold
        script_settings["S_MatchPointsLimit"] = self._match_points_limit
        return script_settings

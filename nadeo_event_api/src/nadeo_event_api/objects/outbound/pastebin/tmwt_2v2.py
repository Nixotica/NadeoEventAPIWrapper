import json
import os
from typing import List


class Tmwt2v2PastebinTeam:
    def __init__(
        self,
        team_name: str,
        p1_tm_account_id: str,
        p2_tm_account_id: str,
    ):
        self.team_name = team_name
        self.p1_tm_account_id = p1_tm_account_id
        self.p2_tm_account_id = p2_tm_account_id

    def members(self) -> List[str]:
        return [self.p1_tm_account_id, self.p2_tm_account_id]

class Tmwt2v2Pastebin:
    def __init__(
        self,
        team_a: Tmwt2v2PastebinTeam,
        team_b: Tmwt2v2PastebinTeam,
    ):
        self.team_a = team_a
        self.team_b = team_b

    def as_jsonable_dict(self) -> dict:
        curr_dir = os.path.dirname(__file__)
        file_path = os.path.join(curr_dir, "pastebin_2v2_template.json")

        with open(file_path, "r") as f:
            pastebin_json = json.load(f)

        pastebin_json[0]["Name"] = self.team_a.team_name
        pastebin_json[0]["Players"][0]["AccountId"] = self.team_a.p1_tm_account_id
        pastebin_json[0]["Players"][1]["AccountId"] = self.team_a.p2_tm_account_id
        pastebin_json[1]["Name"] = self.team_b.team_name
        pastebin_json[1]["Players"][0]["AccountId"] = self.team_b.p1_tm_account_id
        pastebin_json[1]["Players"][1]["AccountId"] = self.team_b.p2_tm_account_id

        return pastebin_json
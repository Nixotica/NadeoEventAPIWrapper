import json


class PickBanStyle:
    def __init__(
        self,
        background: str = "",
        top_left_logo: str = "",
        top_right_logo: str = "",
        bottom_logo: str = "",
    ) -> None:
        self.background = background
        self.top_left_logo = top_left_logo
        self.top_right_logo = top_right_logo
        self.bottom_logo = bottom_logo
        
    def as_jsonable_string(self) -> str:
        pick_ban_style = {
            "Background": self.background,
            "TopLeftLogo": self.top_left_logo,
            "TopRightLogo": self.top_right_logo,
            "BottomLogo": self.bottom_logo,
        }

        return json.dumps(pick_ban_style)
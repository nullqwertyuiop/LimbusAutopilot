from pathlib import Path

from PIL import Image

from model import BaseStage, CheckPair, Return, ClickIt
from util import register_stage, check_and_wait
from var import ASSETS


class BeforeFightStage(BaseStage):
    @property
    def id(self) -> str:
        return "stage.before_drive"

    @property
    def name(self) -> str:
        return "作战前"

    @property
    def determine_pairs(self) -> set[CheckPair]:
        return {
            CheckPair(
                name="作战前",
                image=Image.open(ASSETS / "fight" / "edit_team.png"),
                actions=[Return],
                returns=self,
            ),
        }

    def proceed(self):
        to_battle = Image.open(Path("assets") / "fight" / "to_battle.png")
        check_and_wait(CheckPair(name="开始作战", image=to_battle, actions=[ClickIt, Return]))

    def exit(self):
        pass


register_stage(BeforeFightStage())

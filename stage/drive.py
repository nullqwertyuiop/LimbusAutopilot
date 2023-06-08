from PIL import Image

from model import BaseStage, CheckPair, Return, ClickIt
from util import register_stage, check_and_wait, rightmost
from var import ASSETS


class DriveStage(BaseStage):
    finished_lux: bool = False

    @property
    def id(self) -> str:
        return "stage.drive"

    @property
    def name(self) -> str:
        return "Drive"

    @property
    def determine_pairs(self) -> set[CheckPair]:
        return {
            CheckPair(
                name="Drive",
                image=Image.open(ASSETS / "main" / "drive_selected.png"),
                actions=[Return],
                returns=self,
            ),
        }

    def proceed_lux(self):
        lux = Image.open(ASSETS / "drive" / "lux.png")
        check_and_wait(CheckPair(name="进入作战", image=lux, actions=[ClickIt, Return]))


    def proceed(self):
        if not self.finished_lux:
            self.proceed_lux()
        enter = Image.open(ASSETS / "drive" / "enter.png")
        check_and_wait(
            CheckPair(name="进入作战", image=enter, actions=[ClickIt, Return]),
            result_filter=rightmost,
        )

    def exit(self):
        pass


register_stage(DriveStage())

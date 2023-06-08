from pathlib import Path

from PIL import Image
from loguru import logger

from model import BaseStage, CheckPair, Return, ClickIt
from util import register_stage, check_and_wait
from var import ASSETS


class FightStage(BaseStage):
    turn: int = 1

    @property
    def id(self) -> str:
        return "stage.fight"

    @property
    def name(self) -> str:
        return "作战中"

    @property
    def determine_pairs(self) -> set[CheckPair]:
        return {
            CheckPair(
                name="作战",
                image=Image.open(ASSETS / "fight" / "label.png"),
                actions=[Return],
                returns=self,
            ),
        }

    def proceed(self):
        win_rate = Image.open(ASSETS / "fight" / "win_rate.png")
        start = Image.open(ASSETS / "fight" / "start.png")
        label = Image.open(ASSETS / "fight" / "label.png")
        reward = Image.open(ASSETS / "fight" / "reward.png")
        confirm = Image.open(ASSETS / "fight" / "confirm.png")
        while True:
            _, status = check_and_wait(
                CheckPair(name="作战标签", image=label, actions=[Return], returns=False),
                CheckPair(name="战利品", image=reward, actions=[Return], returns=True),
            )
            if status:
                logger.success(f"作战完毕，一共 {self.turn} 轮")
                break
            check_and_wait(CheckPair(name="胜率", image=win_rate, actions=[ClickIt, Return]))
            check_and_wait(
                CheckPair(name="开始", image=start, actions=[ClickIt, Return]),
                CheckPair(name="胜率", image=win_rate, actions=[ClickIt])
            )
        check_and_wait(CheckPair(name="确认", image=confirm, actions=[ClickIt, Return]))

    def exit(self):
        pass

register_stage(FightStage())

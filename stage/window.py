from PIL import Image

from model import BaseStage, CheckPair, Return, ClickIt
from util import register_stage, check_and_wait
from var import ASSETS


class WindowStage(BaseStage):
    assembled_enk_module: bool = False

    @property
    def id(self) -> str:
        return "stage.window"

    @property
    def name(self) -> str:
        return "Window"

    @property
    def determine_pairs(self) -> set[CheckPair]:
        return {
            CheckPair(
                name="Window",
                image=Image.open(ASSETS / "main" / "drive_unselected.png"),
                actions=[Return],
                returns=self,
            ),
            CheckPair(
                name="Window",
                image=Image.open(ASSETS / "main" / "drive_selected.png"),
                actions=[Return],
                returns=self,
            )
        }

    def proceed_assemble_enk_module(self):
        enk_module = Image.open(ASSETS / "main" / "enk_module.png")
        enk_cancel = Image.open(ASSETS / "main" / "enk_cancel.png")
        enk_max = Image.open(ASSETS / "main" / "enk_max.png")
        enk_confirm = Image.open(ASSETS / "main" / "enk_confirm.png")
        check_and_wait(CheckPair(name="更新确认按钮", image=enk_module, actions=[ClickIt, Return]))
        _, result = check_and_wait(
            CheckPair(name="拉满组装 Enk Module", image=enk_max, actions=[ClickIt, Return], returns=True),
            CheckPair(name="Enk Module 回落", image=enk_cancel, actions=[ClickIt, Return], returns=False)
        )
        if not result:
            return
        check_and_wait(CheckPair(name="组装 Enk Module", image=enk_confirm, actions=[ClickIt, Return]))
        check_and_wait(CheckPair(name="返回 Window", image=enk_cancel, actions=[ClickIt, Return]))
        self.assembled_enk_module = True

    def proceed(self):
        if not self.assembled_enk_module:
            self.proceed_assemble_enk_module()

    def exit(self):
        pass


register_stage(WindowStage())

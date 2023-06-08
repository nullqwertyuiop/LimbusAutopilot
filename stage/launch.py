from PIL import Image

from var import ASSETS
from model import CheckPair, ClickIt, Return, BaseStage
from util import check_and_wait, register_stage


class LaunchStage(BaseStage):
    @property
    def id(self) -> str:
        return "stage.launch"

    @property
    def name(self) -> str:
        return "启动屏幕"

    @property
    def determine_pairs(self) -> set[CheckPair]:
        return {
            CheckPair(
                name="启动页面",
                image=Image.open(ASSETS / "launch" / "cache.png"),
                actions=[Return],
                returns=self,
            )
        }

    def proceed(self):
        banner = Image.open(ASSETS / "launch" / "banner.png")
        confirm = Image.open(ASSETS / "launch" / "confirm.png")
        combat_tips = Image.open(ASSETS / "general" / "combat_tips.png")

        check_and_wait(CheckPair(name="启动横幅", image=banner, actions=[ClickIt, Return]))
        check_and_wait(
            CheckPair(
                name="更新确认按钮", image=confirm, actions=[ClickIt], log="存在未下载的更新，点击确认"
            ),
            CheckPair(name="登入完成", image=combat_tips, actions=[Return], log="已完成登入"),
        )

    def exit(self):
        pass


register_stage(LaunchStage())

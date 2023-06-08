import pyautogui
from loguru import logger

from stage import determine_stage
from var import LOGO


def main():
    logger.info(LOGO)
    stage = determine_stage()
    stage.proceed()


if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    # 设置成 False，不然移动到边缘的时候 pyautogui 会抛出错误
    main()

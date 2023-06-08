import pyautogui
from loguru import logger

from stage import determine_stage
from var import LOGO


def main():
    logger.info(LOGO)
    while True:
        stage = determine_stage()
        stage.proceed()
        logger.info(f"{stage.name} 已执行完毕，退出阶段")
        stage.exit()


if __name__ == "__main__":
    pyautogui.FAILSAFE = False
    # 设置成 False，不然移动到边缘的时候 pyautogui 会抛出错误
    main()

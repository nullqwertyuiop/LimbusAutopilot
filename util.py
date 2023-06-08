import importlib
import time
from pathlib import Path
from typing import overload, TypeVar

import aircv
import cv2
import numpy
import pyautogui
from PIL import Image, ImageGrab
from loguru import logger

from exception import ImageNotFound
from model import ImageFindResult, CheckPair, ClickIt, RemoveMe, Continue, Call, Return, BaseStage

_T = TypeVar("_T")

def image_to_cv2(image: Image) -> numpy.ndarray:
    """
    将 PIL.Image 转换为 cv2

    Args:
        image (Image): PIL.Image

    Returns:
        numpy.ndarray: cv2
    """
    return cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR)  # type: ignore


def cv2_to_image(image: numpy.ndarray) -> Image:
    """
    将 cv2 转换为 PIL.Image

    Args:
        image (numpy.ndarray): cv2

    Returns:
        Image: PIL.Image
    """
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))  # type: ignore


def find_all(
    target: Image, base: Image.Image | None, similarity: float = 0.85
) -> list[ImageFindResult]:
    """
    在图片中查找所有目标图片

    Args:
        target (Image): 目标图片
        base (Image.Image | None): 基础图片，如为 None 则使用当前屏幕截图
        similarity (float, optional): 相似度. Defaults to 0.85.

    Returns:
        list[ImageFindResult]: 查找结果
    """
    if base is None:
        base = ImageGrab.grab()
    return aircv.find_all_template(image_to_cv2(base), image_to_cv2(target), similarity)  # type: ignore


def has(
    target: Image, base: Image.Image | None = None, similarity: float = 0.85
) -> bool:
    """
    在图片中查找目标图片

    Args:
        target (Image): 目标图片
        base (Image.Image | None): 基础图片，如为 None 则使用当前屏幕截图
        similarity (float, optional): 相似度. Defaults to 0.85.

    Returns:
        bool: 是否找到
    """
    return len(find_all(target, base, similarity)) > 0


def move(target: tuple[float, float], duration: float = 0.5) -> None:
    """
    移动鼠标到指定位置

    Args:
        target (tuple[float, float]): 位置
        duration (float, optional): 移动持续时间. Defaults to 0.5.
    """
    logger.debug(f"移动鼠标到 {target}，持续时间 {duration} 秒")
    pyautogui.moveTo(target[0], target[1], duration)


def reset_cursor(duration: float = 0.5) -> None:
    move((0, 0), 0.5)


@overload
def move_click(
    target: tuple[float, float], /, duration: float = 0.5, pause: float = 1.0
) -> None:
    ...

@overload
def move_click(
    target: Image.Image | numpy.ndarray,
    base: Image.Image | None = None,
    similarity: float = 0.85,
    /,
    duration: float = 0.5,
    pause: float = 1.0,
) -> None:
    ...


def move_click(
    target: tuple[float, float] | Image.Image | numpy.ndarray,
    base: Image.Image | None = None,
    similarity: float = 0.85,
    /,
    duration: float = 0.5,
    pause: float = 1.0,
    reset: bool = True
) -> None:
    """
    移动鼠标到指定位置并点击

    Args:
        target (tuple[float, float]): 位置
        base (Image.Image | None): 基础图片，如为 None 则使用当前屏幕截图
        similarity (float, optional): 相似度. Defaults to 0.85.
        duration (float, optional): 移动持续时间. Defaults to 0.5.
        pause (float, optional): 点击后暂停时间. Defaults to 1.0.
        reset (bool, optional): 点击后重置鼠标位置. Defaults to True.

    Raises:
        ImageNotFound: 未找到图片
    """
    if isinstance(target, numpy.ndarray):
        target = cv2_to_image(target)
    if isinstance(target, Image.Image):
        results = find_all(target, base, similarity)
        if len(results) == 0:
            raise ImageNotFound(f"无法找到图片 {target}")
        elif len(results) > 1:
            logger.warning("找到多个图片，使用第一个")
        target = results[0]["result"]
    target: tuple[float, float]
    move((target[0], target[1]), duration)
    if pause > 0:
        logger.debug(f"暂停 {pause} 秒")
        time.sleep(pause)
    logger.debug(f"点击 {target}")
    pyautogui.click()
    if reset:
        reset_cursor()


def check_and_wait(
    *checks: CheckPair,
    similarity: float = 0.85,
    interval: float = 0.1,
    delay: float = 1.0
) -> tuple[list[ImageFindResult], _T | None]:
    """
    检查图片是否出现，出现则执行对应操作，否则继续检查

    Args:
        checks (CheckPair): 检查数据
        similarity (float, optional): 相似度. Defaults to 0.85.
        interval (float, optional): 检查间隔. Defaults to 0.1.
        delay (float, optional): 检查前延迟. Defaults to 1.0.

    Returns:
        list[ImageFindResult]: 图片识别结果
    """
    start = time.time()
    logger.debug(f"开始检查，相似度 {similarity}，间隔 {interval} 秒，{len(checks)} 个检查，延迟 {delay} 秒")
    time.sleep(delay)
    checks = list(checks)
    while True:
        base = ImageGrab.grab()
        if not checks:
            return [], None
        for check in checks:
            image = check.image
            if not (results := find_all(image, base, similarity)):
                continue
            if check.log is not None:
                logger.info(check.log)
            if not check.actions:
                logger.debug(f"已找到 {check.name}，等候耗时 {time.time() - start} 秒")
                return results, check.returns
            for action in check.actions:
                if action is ClickIt:
                    logger.debug(f"已找到 {check.name}，执行点击，等候耗时 {time.time() - start} 秒")
                    move_click(results[0]["result"])
                elif action is RemoveMe:
                    logger.debug(f"已找到 {check.name}，移除检查，等候耗时 {time.time() - start} 秒")
                    checks.remove(check)
                elif action is Continue:
                    # Continue 不需要记入日志
                    continue
                elif isinstance(action, Call):
                    logger.debug(f"已找到 {check.name}，执行函数，等候耗时 {time.time() - start} 秒")
                    action.partial()
                elif action is Return:
                    logger.debug(f"已找到 {check.name}，执行返回，等候耗时 {time.time() - start} 秒")
                    return results, check.returns
                else:
                    logger.warning(f"非预期的操作 {action}")
        time.sleep(interval)


stages: list[BaseStage] = []


def register_stage(stage: BaseStage):
    if stage.id not in [_.id for _ in stages]:
        stages.append(stage)



def load_stages():
    for stage_file in Path("stage").glob("*.py"):
        importlib.import_module(f"stage.{stage_file.stem}")

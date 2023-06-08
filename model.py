import functools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypedDict, TypeVar

from PIL import Image

_T = TypeVar("_T")


class CheckAction:
    """检查行为"""


class Continue(CheckAction):
    """继续循环"""


class ClickIt(CheckAction):
    """点击"""


class RemoveMe(CheckAction):
    """移除自己"""


class Return(CheckAction):
    """返回"""


class Call(CheckAction):
    """调用"""
    partial: functools.partial

    def __init__(self, func, *args, **kwargs):
        self.partial = functools.partial(func, *args, **kwargs)


@dataclass
class CheckPair:
    """检查对"""

    name: str
    image: Image.Image
    actions: list[type[CheckAction] | Call] | None
    log: str = None
    returns: _T | None = None

    def __hash__(self):
        return id(self)


class ImageFindResult(TypedDict):
    """aircv 图像识别结果"""

    result: tuple[float, float]
    rectangle: tuple[float, float, float, float]
    confidence: float


class BaseStage(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        """阶段 ID"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """阶段名称"""
        pass

    @property
    @abstractmethod
    def determine_pairs(self) -> set[CheckPair]:
        """检查对集合"""
        pass

    @abstractmethod
    def proceed(self):
        pass

    @abstractmethod
    def exit(self):
        pass

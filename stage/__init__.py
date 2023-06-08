from loguru import logger

from model import CheckPair, BaseStage
from util import check_and_wait, load_stages, stages


def determine_stage() -> BaseStage:
    load_stages()
    logger.success(f"已注册 {len(stages)} 个阶段")

    pairs: set[CheckPair] = set()
    for stage in stages:
        pairs.update(stage.determine_pairs)

    _, stage = check_and_wait(*pairs)
    stage: BaseStage
    logger.success(f"已检测到当前阶段：{stage.name}")

    return stage

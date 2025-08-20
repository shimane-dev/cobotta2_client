#!/usr/bin/env python
"""
Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_set_work():
    import logging
    import asyncio
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, CobottaVarManager
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta1.yaml")
    # Config.load_yaml("config_cobotta1.yaml")

    logger = XLogger(log_level="debug", logger_name=Config.CLIENT_LOGGER_NAME)
    # cobotta = CobottaCtrl(cobotta_ip=Config.COBOTTA_IP, arm_name="Arm", logger=logger)
    cobotta = AsyncCobottaClient(config=Config, logger=logger)

    ret = await cobotta.reset_error()
    assert ret is not None, "接続失敗"

    var = CobottaVarManager()

    # speed の入手などには take_arm が必要(アームごとのパラメータなので)
    await cobotta.take_arm()
    await cobotta.turn_on_motor()

    # ########################
    # Current_position
    current_pos = await cobotta.get_current_position()
    logger.info(f"current_pos = {current_pos}")

    pos = [
        # 20.259341327288382,
        0.0,
        # 276.59469818653,
        280,
        # 38.52868750215305,
        50.0,
        # 178.72745234477128,
        180.0,
        # 4.521890180915519,
        0.0,
        # -89.24661909122011,
        -90.0,
        261.0,
    ]
    data = await cobotta.get_work(0)
    logger.info(f"get_work {data}")

    logger.info(f"change_work(0)")
    await cobotta.change_work(0)

    logger.info("******")
    logger.info("")
    logger.info(f"set_work {pos}")
    await cobotta.set_work(1, pos)
    logger.info(f"change_work(1)")
    await cobotta.change_work(1)

    data = await cobotta.get_current_position()
    logger.info(f"current_pos = {data}")
    logger.info("")
    logger.info("******")

    logger.info("")
    logger.info(f"change_work(0)")
    await cobotta.change_work(0)
    current_pos = await cobotta.get_current_position()
    logger.info(f"current_pos = {current_pos}")

    # data = cobotta.get_current_work_no()
    # logger.info(f"current_work_no = {data}")

    # current_pos = cobotta.get_current_position()
    # logger.info(f"current_pos = {current_pos}")
    # # cobotta.move(pos, path_blend="@E", motion_mode=MotionMode.LINE, speed=50)
    # # cobotta.wait_for_complete()

    # logger.info(f"pos: {pos}")

    # # ########################
    # # move Target
    # cobotta.cored_type = "P"
    # cobotta.path_blend = "@P"
    # cobotta.motion_mode = MotionMode.PTP
    # # cobotta.bstr_opt = "Speed=100,Next"
    # cobotta.move(pos)
    # cobotta.wait_for_complete()

    # current_pos = cobotta.get_current_position()
    # logger.info(f"current_position: {current_pos}")

    assert "result" == "result"

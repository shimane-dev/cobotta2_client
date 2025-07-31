#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_Async_test_1_2():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    logger.info("== take arm()")
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    logger.info("== turn on motor()")
    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    logger.info("== run test()")
    ret = await client.get_extspeed()
    assert ret is not None, "接続失敗"
    logger.info(ret)

    time.sleep(0.1)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

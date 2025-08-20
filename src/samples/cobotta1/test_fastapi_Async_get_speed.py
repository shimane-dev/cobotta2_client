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
    import asyncio
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta1.yaml")
    # Config.load_yaml("config_cobotta1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    logger.info("== take arm()")
    ret = await client.take_arm()
    assert ret is not None, "接続失敗"

    logger.info("== turn on motor()")
    ret = await client.turn_on_motor()
    assert ret is not None, "接続失敗"

    logger.info("== get_speed()")
    ###############################
    ret = await client.get_speed()
    ###############################
    assert ret is not None, "接続失敗"
    logger.info(ret)

    await asyncio.sleep(0.1)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

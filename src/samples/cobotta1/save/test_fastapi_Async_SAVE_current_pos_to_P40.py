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
    import re
    import json
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "../config_cobotta1.yaml")
    # Config.load_yaml("../config_cobotta1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    await client.take_arm()
    await client.turn_on_motor()

    num = 40

    ret = await client.current_position()
    logger.info(f"current_pos: {ret[:6]}")
    await client.set_P(num, ret[:6])

    name_pos = await client.get_P(num)
    logger.info(f"get_P({num}): {name_pos}")

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

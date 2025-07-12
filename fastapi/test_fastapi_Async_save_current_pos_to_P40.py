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
    import re
    import json
    import logging
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server1.yaml")

    _logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=_logger)

    await client.take_arm()
    await client.turn_on_motor()

    num = 40

    ret = await client.current_position()
    _logger.info(f"current_pos: {ret[:6]}")
    await client.set_P(num, ret[:6])

    name_pos = await client.get_P(num)
    _logger.info(f"get_P({num}): {name_pos}")

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

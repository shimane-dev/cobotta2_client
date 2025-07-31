#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest

from cobotta2.server_fastapi.clients.async_cobotta_state_client import (
    AsyncCobottaStateClient,
)


@pytest.mark.asyncio
async def test_fastapi_state():
    import sys
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    config2 = Config("config_server2.yaml")
    config2_state = Config("config_server2_state.yaml")

    logger = XLogger(log_level="info", logger_name=config2.CLIENT_LOGGER_NAME)
    client2 = AsyncCobottaClient(config=config2, logger=logger)

    # state2 は client に関係なく nonblocking で問い合わせが可能
    state2 = AsyncCobottaStateClient(config=config2_state, logger=logger)
    if state2.busy_status():
        logger.info("state2 is busy")
        sys.exit(-1)

    try:
        # busy_status などの問い合わせは take arm しないほうがいい。
        result = await client2.current_angle()
        logger.info(type(result))
        logger.info(result)
        time.sleep(0.5)
    except Exception as e:
        print(e)
    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

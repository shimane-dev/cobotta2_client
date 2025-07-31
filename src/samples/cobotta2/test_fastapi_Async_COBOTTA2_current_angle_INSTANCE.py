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
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    # instance
    config2 = Config("config_server2.yaml")

    print(f"SERVER IP:{config2.SERVER_IP}")
    print(f"SERVER PORT:{config2.SERVER_PORT}")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=config2, logger=logger)
    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"

    # busy_status などの問い合わせは take arm しないほうがいい。
    result = await client.current_angle()
    logger.info(type(result))
    logger.info(result)
    time.sleep(0.5)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

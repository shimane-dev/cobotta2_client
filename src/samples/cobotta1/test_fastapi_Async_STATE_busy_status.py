#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


@pytest.mark.asyncio
async def test_fastapi_state():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaStateClient
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server1_state.yaml")

    logger= XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    state = AsyncCobottaStateClient(config=Config, logger=logger)

    # while True:
    # busy_status などの問い合わせは take arm しないほうがいい。
    result = await state.busy_status()
    logger.info(f"[state] busy_status = {result}")
    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

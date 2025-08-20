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

    from cobotta2 import Config
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta2.yaml")
    # Config.load_yaml("config_cobotta2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"

    name = "Pro1"

    # 拡張子は必要ない
    logger.info(f"== take script({name})")

    # take_arm の代わりにやる
    await client.take_script(name)

    logger.info(f"== run_script: {name}")
    await client.run_script()
    await client.wait_for_complete()

    await asyncio.sleep(0.1)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

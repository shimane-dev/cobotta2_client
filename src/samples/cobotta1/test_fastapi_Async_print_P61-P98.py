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
    import re
    import asyncio
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "config_cobotta1.yaml")
    # Config.load_yaml("config_cobotta1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    await client.take_arm()
    await client.turn_on_motor()

    start = "P61"
    end = "P98"

    # Pの後ろの数字を抽出して整数に変換
    start_num = int(re.findall(r"\d+", start)[0])
    end_num = int(re.findall(r"\d+", end)[0])

    for i in range(start_num, end_num + 1):
        name_pos = await client.get_P(i)
        logger.info(f"P({i}): {name_pos}")

    await asyncio.sleep(0.1)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

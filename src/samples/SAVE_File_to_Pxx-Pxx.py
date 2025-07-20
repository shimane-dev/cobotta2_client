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

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    await client.take_arm()
    await client.turn_on_motor()

    start = "P60"
    end = "P105"
    filepath = f"COBOTTA1_{start}_{end}_pos.json"

    # Pの後ろの数字を抽出して整数に変換
    start_num = int(re.findall(r"\d+", start)[0])
    end_num = int(re.findall(r"\d+", end)[0])

    # ファイルから読み込み
    with open(filepath, "r", encoding="utf-8") as f:
        memory_loaded = json.load(f)

    for i in range(start_num, end_num + 1):
        key = f"P{i}"
        value = memory_loaded.get(key)
        if value is not None:
            await client.set_P(i, value)
            logger.info(f"set_P({i}, {value})")
        else:
            print(f"{key} は存在しません")

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

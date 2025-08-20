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

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
    Config.load_yaml(HERE / "config_cobotta2.yaml")
    # Config.load_yaml("config_cobotta2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"

    await client.take_arm()
    ret = await client.turn_on_motor()

    start = "P60"
    end = "P105"

    # Pの後ろの数字を抽出して整数に変換
    start_num = int(re.findall(r"\d+", start)[0])
    end_num = int(re.findall(r"\d+", end)[0])

    memory = {}
    for i in range(start_num, end_num + 1):
        name_pos = await client.get_P(i)
        logger.info(f"P{i}: {name_pos}")
        target = list(name_pos)
        memory[f"P{i}"] = target

        # print(json.dumps(memory, indent=4))

    # ファイルに書き込む
    filepath = f"COBOTTA2_{start}_{end}_pos.json"
    with open(f"{filepath}", "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=True, indent=4)

    await asyncio.sleep(0.1)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

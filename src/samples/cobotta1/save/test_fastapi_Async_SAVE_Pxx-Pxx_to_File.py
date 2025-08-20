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
    import json
    from datetime import datetime
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "../config_cobotta1.yaml")
    # Config.load_yaml("../config_cobotta1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)

    await client.take_arm()
    await client.turn_on_motor()

    # start = "P60"
    # end = "P105"
    start = "P120"
    end = "P140"

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

    now = datetime.now()
    dt_str = now.strftime("%Y-%m-%d_%H%M")  # 例: '2025-07-17_1632'

    # ファイルに書き込む
    filepath = f"COBOTTA1_{start}_{end}_pos_{dt_str}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=True, indent=4)

    filepath = f"COBOTTA1_{start}_{end}_pos.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=True, indent=4)

    await asyncio.sleep(0.1)

    assert "result" == "result"
    # send_command("unknown")  # これはエラーになる

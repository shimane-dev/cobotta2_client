#!/usr/bin/env python
"""

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
# import pytest
import asyncio


# @pytest.mark.asyncio
async def main():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from x_logger.x_logger import XLogger

    Config.load_yaml("../config_server1.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    await client.reset_error()

    name = "P_P62"

    # 拡張子は必要ない
    logger.info(f"== take script({name})")
    await client.take_script(name)

    logger.info(f"== run_script: {name}")
    await client.run_script()
    await client.wait_for_complete()

    time.sleep(0.1)


if __name__ == "__main__":
    asyncio.run(main())

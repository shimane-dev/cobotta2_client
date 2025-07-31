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
    from cobotta2.server_fastapi.models.motion import MotionMode
    from x_logger.x_logger import XLogger

    Config.load_yaml("../config_server1.yaml")

    _logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=_logger)
    # busy_status などの問い合わせは take arm しないほうがいい。

    try:
        # ret = await client.get_cobotta_file_names()
        # _logger.info(ret)
        await client.download_all_files_from_cobotta()
    except Exception as e:
        print(e)
    # assert "result" == "result"
    # send_command("unknown")  # これはエラーになる


if __name__ == "__main__":
    asyncio.run(main())

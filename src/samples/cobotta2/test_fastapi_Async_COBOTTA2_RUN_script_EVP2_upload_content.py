#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest


def make_file_content(evp_script_name: str) -> str:
    file_content = f"""
    #Include "Variant.h"
    Dim ctrl As Object 

    Sub Main
        ctrl = Cao.AddController("Runner", "CaoProv.DENSO.EVP2", "", "@IfnotMember")
        ctrl.LoadFile "{evp_script_name}"
        ctrl.Run
    End Sub
    """
    return file_content


@pytest.mark.asyncio
async def test_fastapi_Async_test_1_2():
    import logging

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    import time
    from cobotta2.config import Config
    from cobotta2.server_fastapi.clients import AsyncCobottaClient
    from x_logger.x_logger import XLogger

    Config.load_yaml("config_server2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.COBOTTA_CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"
    await client.release_arm()

    await client.turn_on_motor()

    pac_script_name = "EVP2_p3.pcs"
    evp_script_name = "try_camera"
    file_content = make_file_content(evp_script_name)
    await client.upload_content_to_cobotta(file_content, pac_script_name)

    await client.take_script(pac_script_name)
    await client.run_script()

    await client.wait_for_complete()
    print(client.P10)

    assert "result" == "result"


# def test_local_reset_error():
#     p = multiprocessing.Process(target=worker)
#     p.start()
#     # p.terminate()
#     p.join()  # join()なしでもkillはされる

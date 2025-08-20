#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest
import asyncio


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
    import asyncio
    from pathlib import Path

    # httpx のログを WARNING レベル以上にする（INFO を抑制）
    logging.getLogger("httpx").setLevel(logging.WARNING)

    from cobotta2 import Config, MotionMode
    from cobotta2.server import AsyncCobottaClient
    from x_logger import XLogger

    HERE = Path(__file__).parent
    Config.load_yaml(HERE / "../config_cobotta2.yaml")
    # Config.load_yaml("../config_cobotta2.yaml")

    logger = XLogger(log_level="info", logger_name=Config.CLIENT_LOGGER_NAME)
    client = AsyncCobottaClient(config=Config, logger=logger)
    ret = await client.reset_error()
    if ret is None or ret is False:
        assert False, "Connect Error"
    await client.release_arm()

    await client.turn_on_motor()

    logger.info("--------- カメラポジションへ -----------------")
    await client.take_arm()
    await client.open_hand()
    await client.move("P110", path_blend="@E", motion_mode=MotionMode.LINE, speed=100)
    await client.release_arm()

    # 画像認識の結果記録を初期化
    client.I2 = 0
    client.P10 = await client.get_current_position()

    # この挙動は画像モデルによって異なる(参照する変数とか)ので注意
    while True:
        logger.info("---------- カメラで画像認識 -------------------")
        pac_script_name = "EVP2_p3.pcs"
        evp_script_name = "try_camera"
        file_content = make_file_content(evp_script_name)
        await client.upload_content_to_cobotta(file_content, pac_script_name)

        await client.take_script(pac_script_name)
        await client.run_script()

        await client.wait_for_complete()
        logger.info(f"Result: {client.P10}")
        if client.I2 == 1:
            break
        logger.error(f"*** ターゲットが見つけられません ***")
        logger.error(f"*** 3sec 後に retry します ***")
        await asyncio.sleep(3)

    logger.error(f"***")
    logger.info(f"Result(work): {client.P10}")
    logger.error(f"***")

    logger.info("----------- 画像認識のセンターへmove  --------------")
    await client.take_arm()
    # client.move("P10+(0,0,-5)", speed=30)
    # client.move("@E P10", offset=(0, 0, -5), speed=30)
    await client.move_L("@E P10", speed=30)
    await client.wait_for_complete()

    logger.info("----------- 指先を９０度回転  --------------")
    # client.drive_EX((6, -90))  # 相対
    await client.rotate_H(-90.0)  # 相対
    await client.wait_for_complete()

    logger.info("----------- 近づく(offset-move)  --------------")
    pos = await client.get_current_position()

    ############### 基本動作テスト
    # client.cored_type = "P"
    # client.path_blend = "@P"
    # client.motion_mode = MotionMode.PTP
    # # client.bstr_opt = "Speed=100,Next"
    # client.move(pos)
    ##########################

    ## ### offset 付きの基本動作
    ## client.move(pos, offset=(0, 0, -13), speed=30)

    ### # cobotta.hand_move_A(30, speed=100)  # full-open
    ### client.wait_for_complete()

    # ここで、P10 を入れると J6 の値が元に戻るので 直前の回転が意味がなくなる
    # client.move("P10", offset=(0, 0, -15), speed=30)


# def test_local_reset_error():
#     p = multiprocessing.Process(target=worker)
#     p.start()
#     # p.terminate()
#     p.join()  # join()なしでもkillはされる

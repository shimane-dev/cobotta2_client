#!/usr/bin/env python
"""
内部変数値を読んで、それを配列に入れなおして、そこに移動する

Kengo NAKADA:
https://github.com/shimane-dev, https://github.com/kengo-nakada
kengo.nakada@mat.shimane-u.ac.jp, kengo.nakada@gmail.com
"""
import pytest
import asyncio
import sys


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

    ##############################################
    await client.turn_on_motor()

    logger.info("--------- カメラポジションへ -----------------")
    await client.take_arm()
    await client.open_hand()

    # based on P110
    # P110_camera = (
    #     197.74189325511722,  # X
    #     -102.87065719423421,  # y
    #     # 45.40395449388056,  # z
    #     180.0,  # z
    #     -176.46837944742447,  # rx
    #     # 10.232977777915506,  # ry
    #     0.0,
    #     176.76296478619867,  # rz
    #     261.0,
    # )
    # ret = await client.move(P110_camera, speed=50)
    pos_P110 = await client.get_current_position()
    await client.move("P110", path_blend="@E", motion_mode=MotionMode.LINE, speed=100)
    if not ret or ret is None:
        sys.exit(-1)

    logger.info("---------- Hand 初期位置移動 -------------------")
    await client.init_hand()
    await asyncio.sleep(1)
    await client.release_arm()

    # 画像認識の結果記録を初期化
    client.I2 = 0
    client.P10 = await client.get_current_position()

    # この挙動は画像モデルによって異なる(参照する変数とか)ので注意
    while True:
        logger.info("---------- カメラで画像認識 -------------------")
        # pac_script_name = "EVP2_03.pcs"
        # evp_script_name = "try_camera"
        # file_content = client.make_file_content(evp_script_name)
        await client.take_camera("try_camera", "EVP2_03.pcs")
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

    #   sys.exit(-1)
    # Result = (
    #     248.1692352294922,
    #     -109.76080322265625,
    #     8.715171813964844,
    #     176.98410034179688,
    #     -1.8386553525924683,
    #     -34.57173538208008,
    #     261.0,
    # )

    logger.info("----------- 画像認識のセンターへmove  --------------")
    await client.take_arm()
    # await client.move("P10+(0,0,-5)", speed=30)
    # await client.move("@E P10", offset=(0, 0, -5), speed=30)
    await client.move("P10", path_blend="@E", speed=30)
    await client.wait_for_complete()

    logger.info("----------- 指先を９０度回転  --------------")
    logger.info("rotate_H: -90.0")
    ret = await client.drive_EX((6, -90))  # 相対
    # await client.rotate_H(-90.0)  # 相対
    if not ret or ret is None:
        # 開始状態によっては指の回転状態が異なるので -90 でエラーとなることがあるのでそのときは +90 でチャレンジ
        logger.info("Retry: rotate_H: 90.0")
        await client.reset_error()
        await client.release_arm()
        await client.take_arm()
        ret2 = await client.drive_EX((6, 90))  # 相対
        if not ret2 or ret2 is None:
            sys.exit(-1)

    await client.wait_for_complete()

    # ret = await client.get_current_position()
    # logger.info(ret)
    # ret = [
    #     248.1541738999505,
    #     -109.81285328165427,
    #     8.648594204999199,
    #     -178.16926548965247,
    #     -3.0251761097850935,
    #     -124.44920678674276,
    #     261.0,
    # ]
    # sys.exit(-1)

    logger.info("----------- 近づく(offset-move)  --------------")
    pos = await client.get_current_position()
    # offset 付きの基本動作
    # ret = client.move(pos, path_blend="@0", offset=(0, 0, -25), speed=30)
    ret = await client.move(pos, path_blend="@E", offset=(0, 0, -25), speed=30)
    if not ret:
        sys.exit(-1)  ## ここでぶつかる恐れがある

    # ret = await client.get_current_position()
    # logger.info(ret)
    # sys.exit(-1)

    logger.info("----------- つかむ  --------------")
    # ret = await client.hand_move_H(8, True)
    ret = await client.hand(force=8)
    if not ret:
        sys.exit(-1)
    await client.wait_for_complete()
    await asyncio.sleep(2)

    # ここで、P10 を入れると J6 の値が元に戻るので 直前の回転が意味がなくなる
    # client.move("P10", offset=(0, 0, -15), speed=30)

    logger.info("----------- 移動 --------------")
    await client.move("P111", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P112", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P113", motion_mode=MotionMode.LINE, speed=50)
    ##  client.move("P114", motion_mode=MotionMode.LINE, speed=50)
    ##  client.move("P117", motion_mode=MotionMode.LINE, speed=50)
    ##  client.move("P118", motion_mode=MotionMode.LINE, speed=50) # だめ
    await client.move("P119", motion_mode=MotionMode.LINE, speed=50)
    # await client.move("P120", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P121", motion_mode=MotionMode.LINE, speed=50)
    await client.wait_for_complete()

    # 離して測る
    await client.open_hand()
    await asyncio.sleep(0.5)

    logger.info("----------- つかむ  --------------")
    # ret = await client.hand_move_H(8, True)
    ret = await client.hand(force=8)
    if not ret:
        sys.exit(-1)
    await client.wait_for_complete()
    await asyncio.sleep(2)

    logger.info("----------- 帰宅 --------------")
    # await client.move("P120", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P119", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P113", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P112", motion_mode=MotionMode.LINE, speed=50)
    await client.move("P111", motion_mode=MotionMode.LINE, speed=50)

    # Place
    await client.move("P122", motion_mode=MotionMode.LINE, speed=50)
    await client.open_hand()
    await asyncio.sleep(0.5)

    # move to home
    await client.move("P110", motion_mode=MotionMode.LINE, speed=50)

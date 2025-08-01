#!/usr/bin/env python

from cobotta2 import Config, CobottaVarManager
from cobotta2.server import AsyncCobottaClient
from x_logger import XLogger

import logging

# httpx のログを WARNING レベル以上にする（INFO を抑制）
logging.getLogger("httpx").setLevel(logging.WARNING)

import os

config2 = Config("config_cobotta2.yaml")

logger = XLogger(log_level="info", logger_name=config2.CLIENT_LOGGER_NAME)
client = AsyncCobottaClient(config=config2, logger=logger)

v = CobottaVarManager(client)
v.get_cobotta("P110")
# v.read_vars_from_cobotta("P", 110, 199)
# v.read_vars_from_cobotta("P", 0, 300)
# v.read_vars_from_cobotta("P", 110)
print(v.P110)
#
# var.read_vars_from_cobotta("P", 111)
# print(var.P111)
#
# var.read_vars_from_cobotta("P", 112)
# print(var.P111)

# print(var.P111)
# var.save("a.json")


# print("カレントディレクトリ:", os.getcwd())
#
# config = Config("../../examples/config_cobotta1.yaml")
# # config_state = Config("config_cobotta1_state.yaml")
#
#
# print(config.SERVER_IP)
# print(config.SERVER_PORT)

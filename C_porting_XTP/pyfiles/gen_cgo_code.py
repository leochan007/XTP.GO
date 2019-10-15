#!/usr/bin/python
#! -*- encoding=utf-8 -*-

import os
import re
import shutil
import time

from modules import *

if __name__ == '__main__':
    gen_common_h()
    enum_map = gen_convert_utils()
    gen_define_h(enum_map)
    info1 = gen_xtp_api('xtp_quote_api')
    info2 = gen_xtp_api('xtp_trader_api')

    start_message = 3000
    gen_message_h(info1, info2, start_message)
    gen_def_go_file(info1, info2, start_message)
    cp_cmakelist()

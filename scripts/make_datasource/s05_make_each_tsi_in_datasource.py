#!/usr/bin/env python
# -*- coding: utf-8 -*-
# s05_make_each_tsi_in_datasource.py
# made by Daniel Minseok Kwon
# 2020-06-17 04:03:54
#########################
import sys
import os
SVRNAME = os.uname()[1]
if "MBI" in SVRNAME.upper():
    sys_path = "/Users/pcaso/bin/python_lib"
elif SVRNAME == "T7":
    sys_path = "/ms1/bin/python_lib"
else:
    sys_path = "/home/mk446/bin/python_lib"
sys.path.append(sys_path)


def make_each_tsi_in_datasource():
    

if __name__ == "__main__":
    import proc_util
    import file_util
    import seq_util
    make_each_tsi_in_datasource()

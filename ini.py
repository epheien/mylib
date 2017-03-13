#!/usr/bin/env python
# -*- coding: utf-8 -*-

import portalocker # pip install portalocker
import ConfigParser
import traceback
import os

def read(fname, section, key, default=None, errmsg=None):
    '''
    发生错误时，返回 default
    '''
    errmsg = [] if errmsg is None else errmsg
    config = ConfigParser.RawConfigParser()
    try:
        with open(fname) as fp:
            portalocker.lock(fp, portalocker.LOCK_SH)
            config.readfp(fp)
            if config.has_option(section, key):
                return config.get(section, key)
            else:
                return default
    except:
        errmsg.append(traceback.format_exc())
        return default

def write(fname, section, key, val, errmsg=None):
    errmsg = [] if errmsg is None else errmsg
    config = ConfigParser.RawConfigParser()

    # FIXME: 有问题，两个锁之间有窗口期，但是Windows下不知道如何处理
    try:
        with open(fname) as fp:
            portalocker.lock(fp, portalocker.LOCK_SH)
            config.readfp(fp)
            if not config.has_section(section):
                config.add_section(section)
            config.set(section, key, val)

        # 写一个备份，以防不测。需要读取的时候判断是否使用这个文件
        #with open(fname + '.bak', 'w') as fp:
            #config.write(fp)

        with open(fname, 'w') as fp:
            portalocker.lock(fp, portalocker.LOCK_EX)
            config.write(fp)
    except:
        errmsg.append(traceback.format_exc())


if __name__ == '__main__':
    errmsg = []
    #write('a.ini', 'all', 'key', 'val', errmsg=errmsg)
    #write('a.ini', 'all', 'key2', 'val2', errmsg=errmsg)
    #if errmsg:
    #    print errmsg.pop()
    #print read('a.ini', 'all', 'key', errmsg=errmsg)
    #if errmsg:
    #    print errmsg.pop()

#!/usr/bin/env python
# coding:utf-8

import sys
import CallbackServer

def callback_method(query):
    return ['Hello', 'World!', 'with', query]

if __name__ == '__main__':
    port = sys.argv[1]
    CallbackServer.start(port, callback_method)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/19 17:26
# @Author  : wAiXi
# @Site    : 
# @File    : Common.py
# @Software: PyCharm Community Edition
from urllib.parse import quote
import urllib.request

import eventlet
from bs4 import BeautifulSoup
import time


def get_url(base_path, page_index, keywords):
    query_dynasty = keywords.encode('UTF-8')
    url = base_path + '?p=' + str(page_index) + '&c=' + quote(query_dynasty)
    return url


def get_elapsed_time(fn):
    def _wrapper(*args, **kwargs):
        start = time.clock()
        fn(*args, **kwargs)
        print("%s cost %s second" % (fn.__name__, time.clock() - start))

    return _wrapper


# 获取soup
def get_soup(_link):
    html = urllib.request.urlopen(_link)
    soup = BeautifulSoup(html, 'lxml')
    return soup


# 使用eventlet获取soups
def get_soups(_all_links):
    pool = eventlet.GreenPool()
    soups = pool.imap(get_soup, _all_links)
    return soups

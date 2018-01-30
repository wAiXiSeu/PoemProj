#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/14 15:48
# @Author  : wAiXi
# @Site    : 
# @File    : Dynasty.py
# @Software: PyCharm Community Edition

import urllib.request
from bs4 import BeautifulSoup


def get_dynasty_list(base_path, link):
    html = urllib.request.urlopen(base_path + link)
    soup = BeautifulSoup(html, 'lxml')
    dynasty_info = soup.find_all('a', style=' width:auto; margin-left:16px;')
    dynast_list = []
    for d in dynasty_info:
        dynast_list.append({
            'dynasty_link': d.attrs['href'],
            'dynasty': d.string
        })
    return dynast_list


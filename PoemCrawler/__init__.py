#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/10 15:59
# @Author  : wAiXi
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm Community Edition

import urllib.request

from bs4 import BeautifulSoup


def get_dynasty_list(link):
    html = urllib.request.urlopen(link)
    soup = BeautifulSoup(html, 'lxml')
    dynasty_info = soup.find_all('a', style=' width:auto; margin-left:16px;')
    dynast_list = []
    for d in dynasty_info:
        dynast_list.append({
            'dynasty_link': 'http://so.gushiwen.org' + d.attrs['href'],
            'dynasty': d.string
        })
    return dynast_list

def get_author_list(link):

    pass

if __name__ == '__main__':
    poemSrcPath = 'http://so.gushiwen.org/authors/'
    dynastyList = get_dynasty_list(poemSrcPath)
    print(dynastyList)

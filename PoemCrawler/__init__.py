#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/10 15:59
# @Author  : wAiXi
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm Community Edition
import time

from PoemCrawler.Author import get_author_list
from PoemCrawler.Dynasty import get_dynasty_list
from PoemCrawler.Poem import get_poem

base_url = 'http://so.gushiwen.org'
author_default_link = '/authors/Default.aspx'
dynasty_list = []
author_list = []

if __name__ == '__main__':
    print("get author list task start...")
    start_time = time.time()
    author_list = get_author_list(base_url, author_default_link, '唐代')
    print("get author list task end...")
    print("cost %s seconds" % (time.clock() - start_time))
    print(author_list)
    author_links = [base_url + link['author_link'] for link in author_list]
    print('start work...')
    start_time = time.time()
    contents = get_poem(base_url, author_links[0:10])
    print('end work...')
    end_time = time.time()
    print('cost %s seconds' % (end_time - start_time))
    for c in contents:
        print('----------------------')
        print(c.get())
        print(len(c.get()))
        print('----------------------')
        print()

    pass




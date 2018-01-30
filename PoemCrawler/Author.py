#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/14 15:50
# @Author  : wAiXi
# @Site    : 
# @File    : Author.py
# @Software: PyCharm Community Edition
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import multiprocessing
import re
import time
import urllib.request
from multiprocessing.pool import ThreadPool

from bs4 import BeautifulSoup

from PoemCrawler.Common import get_url


def _get_author_total_count(soup):
    _count_info = soup.find('span',
                            style='color:#65645F; background-color:#E1E0C7; border:0px; width:auto;').string
    if re.search('\d+', _count_info) is not None:
        num = re.search('\d+', _count_info).group()
    return num


def _get_author_list(_author_url):
    _html = urllib.request.urlopen(_author_url)
    _soup = BeautifulSoup(_html, 'lxml')
    _author_info = _soup.find_all('a', target='_blank', style='font-size:18px; line-height:22px; height:22px;')
    _a_list = []
    for a in _author_info:
        _a_list.append({
            'author': a.string,
            'author_link': a.attrs['href']
        })
    return _a_list


def get_author_list(base_path, relative_path, dynasty):
    url = get_url(base_path + relative_path, 1, dynasty)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    total_count = _get_author_total_count(soup)
    count_per_page = 10
    page_count = int(int(total_count) / count_per_page)
    pool = ThreadPool(multiprocessing.cpu_count())
    index = range(1, page_count + 1)
    _author_list = []
    for i in index:
        p = pool.apply_async(_get_author_list, (get_url(base_path + relative_path, i, dynasty),))
        _author_list.append(p)
    pool.close()
    pool.join()
    author_list = []
    for a in _author_list:
        author_list.extend(a.get())
    return author_list


def _get_author_info_list(_base_path, _author_link):
    author_id = re.search(r'\d+', _author_link).group()
    html = urllib.request.urlopen(_base_path + _author_link)
    soup = BeautifulSoup(html, 'lxml')
    author_description = re.sub(r'' + str(_author_link) + '', '',
                                soup.find('textarea', id='txtareAuthor' + str(author_id)).contents[0])
    author_info = re.search(r'(.*?)（(.*?)）.*', author_description)
    if author_info is not None:
        author_name = author_info.group(1)
        author_time = author_info.group(2)
    else:
        author_name = ""
        author_time = ""
    author_zi = re.search(r'(字.*?)[，|。]', author_description)
    if author_zi is not None:
        author_zi = author_zi.group(1)
    else:
        author_zi = ""
    author_hao = re.search(r'(号.*?)[，|。]', author_description)
    if author_hao is not None:
        author_hao = author_hao.group(1)
    else:
        author_hao = ""
    author_ming = re.search(r'(名.*?)[，|。]', author_description)
    if author_ming is not None:
        author_ming = author_ming.group(1)
    else:
        author_ming = ""
    poem_link = soup.p.a['href']
    poem_account = re.sub(r'\D', '', soup.p.a.string)
    author_info_list = {
        "author_id": author_id,
        "author_name": author_name,
        "author_time": author_time,
        "author_ming": author_ming,
        "author_zi": author_zi,
        "author_hao": author_hao,
        "poem_account": poem_account,
        "author_description": author_description,
        "poem_link": poem_link
    }
    return author_info_list


def get_author_info_list(_base_url, _author_links):
    author_info_list = []
    with ThreadPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        future_author_list = {executor.submit(_get_author_info_list, _base_url, link): link for link in _author_links}
        for future in concurrent.futures.as_completed(future_author_list):
            author_info_list.append(future.result())
        return author_info_list


if __name__ == '__main__':
    base_url = 'http://so.gushiwen.org'
    author_default_link = '/authors/Default.aspx'
    start_time = time.clock()
    print("get author list task start...")
    author_list = get_author_list(base_url, author_default_link, '唐代')
    print("get author list task end...")
    print("cost %s seconds" % (time.clock() - start_time))
    print(author_list)

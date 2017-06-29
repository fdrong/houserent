#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'rongfudi636'
__mtime__ = '22/06/2017'
"""


from scrapy import cmdline
cmdline.execute('scrapy crawl my58 -a key=金硕河畔,瑞和新苑 -a days=30'.split())
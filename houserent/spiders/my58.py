# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime


class My58Spider(scrapy.Spider):
    name = 'my58'
    # allowed_domains = ['58.com']
    base_url = u'http://sh.58.com/zufang/0/?key={key}&PGTID=0d3090a7-0000-23a4-e2ae-3fdd979b4ae6&ClickID=4'
    # start_urls = [u'http://sh.58.com/zufang/0/?key=浦江丽都&PGTID=0d3090a7-0000-23a4-e2ae-3fdd979b4ae6&ClickID=4']

    def __init__(self, *args, **kwargs):
        super(My58Spider, self).__init__(args, **kwargs)
        keys = kwargs.get('key').decode('utf-8')
        for key in keys.split(','):
            self.start_urls.append(self.base_url.format(key=key))

    def parse(self, response):
        for li in response.css('ul.listUl li'):
            href = li.css('div.img_list a::attr("href")').extract_first()
            send_time = li.css('div.sendTime::text').extract_first()
            if not send_time:
                continue
            send_time = send_time.strip()
            try:
                send_time = datetime.strptime(u'2017-{}'.format(send_time), '%Y-%m-%d')
            except Exception, e:
                self.log(u"parse send time:{} error, reason: {}".format(send_time, str(e)))
                yield response.follow(href, self.parse_detail)
                continue
            interval = (datetime.now()-send_time).days
            try:
                days = getattr(self, 'days')
            except Exception as e:
                days = 30
            # 大于30天估计房子都没了
            if interval < days:
                yield response.follow(href, self.parse_detail)

    def parse_detail(self, response):
        href = response.css('a.c_000::attr("href")').extract_first()
        yield response.follow(href, self.parse_person)

    def parse_person(self, response):
        href = response.css('div.sc-post-iframe iframe::attr("src")').extract_first()
        yield response.follow(href, self.parse_public)

    def parse_public(self, response):
        public_count = int(response.css('li.cur a::text').re_first(r'\d+'))
        urls = response.xpath('//div[@class="sc-post-con"]//a[not(@class="color313")]/@href').extract()
        titles = response.xpath('//div[@class="sc-post-con"]//a[not(@class="color313")]/text()').extract()
        excludes = set([title.strip() for title in titles])
        # 识别出中介
        if public_count <= 1 or len(excludes) <= 1:
            yield {
                'public_count': public_count,
                "urls": urls
            }
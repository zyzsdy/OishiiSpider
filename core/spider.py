# coding: utf-8
import requests
import queue
import re
from urllib.parse import urljoin
from lxml import etree
from pybloom import BloomFilter


class Rule:
    def __init__(self, regex, callback=None, follow=None):
        self.re_str = regex
        self.regex = re.compile(regex)
        if follow is None:
            if callback is None:
                self.follow = True
            else:
                self.follow = False
        else:
            self.follow = follow
        self.callback = callback

    def test(self, url):
        res = re.search(self.regex, url)
        return True if res else False


class Spider:
    rules = ()

    def __init__(self, domain, first_url=None, first_url_callback=None, first_url_follow=True, url_amount=100000,
                 requests_session=None, tls=False, max_depth=100):
        self.domain = domain
        self.max_depth = max_depth
        self.bf = BloomFilter(capacity=url_amount, error_rate=1 / url_amount)
        self.url_queue = queue.Queue()

        if first_url is None:
            if tls:
                first_url = 'https://' + domain
            else:
                first_url = 'http://' + domain

        self.url_queue.put((first_url, first_url_callback, first_url_follow, 0))

        if requests_session is None:
            self.session = requests.Session()
        else:
            self.session = requests_session

    def start_crawl(self):
        try:
            while True:
                url, cb, follow, depth = self.url_queue.get_nowait()
                if depth > self.max_depth:
                    continue
                elif url not in self.bf:
                    self.process_url(url, cb, follow, depth)
                    self.bf.add(url)
        except queue.Empty as e:
            print("//////////INFO: Crawl Finished.")

    def process_url(self, url, callback, follow, depth):
        print("//////%s GET: %s" % (depth, url))
        res = self.session.get(url)
        if follow:
            html = etree.HTML(res.content)
            hrefs = html.xpath("//a/@href")
            for href in hrefs:
                next_url = urljoin(url, href)
                if next_url not in self.bf:
                    for rule in self.rules:
                        if rule.test(next_url):
                            next_follow = rule.follow
                            next_callback = rule.callback
                            self.url_queue.put((next_url, next_callback, next_follow, depth+1))
        if callback:
            cb = getattr(self, callback)
            if callable(cb):
                cb(res.content, url)
            else:
                raise AttributeError("%s is not a callback function." % callback)




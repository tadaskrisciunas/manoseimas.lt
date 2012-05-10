# coding: utf-8

import unittest

from scrapy.http import HtmlResponse

from ..spiders.sittings import SittingsSpider

from .utils import fixture


def parse_question():
    spider = SittingsSpider()
    url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.klaus_stadija?'
           'p_svarst_kl_stad_id=-9211')
    response = HtmlResponse(url, body=fixture('question_-9211.html'))
    return list(spider.parse_question(response))


def parse_voting():
    spider = SittingsSpider()
    url = ('http://www3.lrs.lt/pls/inter/w5_sale_new.bals?'
           'p_bals_id=-10765')
    response = HtmlResponse(url, body=fixture('sitting_-10765.html'))
    return list(spider.parse_person_votes(response))


class TestSittingsSpider(unittest.TestCase):
    def test_question(self):
        items = parse_question()

        # question
        item = items[0]
        self.assertEqual(item['_id'], '-9211q')

        # voting
        item = items[1]
        self.assertEqual(item['_id'], '-10765v')


    def test_nedzinskas(self):
        items = parse_voting()

        item = items[0]
        self.assertEqual(item['_id'], '-10765v')
        self.assertEqual(item['documents'], [u'XIP-2992', u'XIP-2993'])
        self.assertEqual(item['votes'][0], {
            'fraction': u'TTF',
            'name': u'Ačas Remigijus',
            'person': u'47852p',
            'vote': u'aye'
        })
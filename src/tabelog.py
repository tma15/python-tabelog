#!/usr/bin/python
#-*- coding:utf8 -*-
#
# API manual:
# http://tabelog.com/help/api_manual/
#
import sys
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup


def convert2prefecture_parameter(prefecture):
    prefecture_map = {'北海道': 'hokkaido', '青森': 'aomori', '岩手': 'iwate', '宮城': 'miyagi',
                      '秋田': 'akita', '山形': 'yamagata', '福島': 'fukushima', '茨城': 'ibaraki',
                      '栃木': 'tochigi', '群馬': 'gunma', '埼玉': 'saitama', '千葉': 'chiba', '東京': 'tokyo',
                      '神奈川': 'kanagawa', '新潟': 'niigata', '富山': 'toyama', '石川': 'ishikawa',
                      '福井': 'fukui', '山梨': 'yamanashi', '長野': 'nagano', '岐阜': 'gifu',
                      '静岡': 'shizuoka', '愛知': 'aichi', '三重': 'mie', '滋賀': 'shiga', '京都': 'kyoto',
                      '大阪': 'osaka', '兵庫': 'hyogo', '奈良': 'nara', '和歌山': 'wakayama',
                      '鳥取': 'tottori', '島根': 'shimane', '岡山': 'okayama', '広島': 'hiroshima',
                      '山口': 'yamaguchi', '徳島': 'tokushima', '香川': 'kagawa', '愛媛': 'ehime',
                      '高知': 'kochi', '福岡': 'fukuoka', '佐賀': 'saga', '長崎': 'nagasaki',
                      '熊本': 'kumamoto', '大分': 'oita', '宮崎': 'miyazaki', '鹿児島': 'kagoshima',
                      '沖縄': 'okinawa', '全国': 'japan'}
    return prefecture_map[prefecture]


class TabeLog:
    def __init__(self, access_key):
        self._access_key = access_key
        self._request_url = 'http://api.tabelog.com/Ver2.1/RestaurantSearch/?Key=%s' % self._access_key
        self._search_results = None

    @property
    def request_url(self):
        return self._request_url

    def search_restaurant(self,
                        lattitude=None,
                        longitude=None,
                        datum=None,
                        search_range=None,
                        prefecture=None,
                        station=None,
                        result_set=None,
                        sort_order=None,
                        page_num=None,
                        result_datum=None,
                        ):
        if lattitude:
            self._request_url = "%sLatitude=%f" % (self._request_url, float(lattitude))
        if longitude:
            self._request_url = "%sLongitude=%f" % (self._request_url, float(longitude))
        if datum and lattitude and longitude: ### valid if both lattitude and longitude are specified
            self._request_url = "%sDatum=%s" % (self._request_url, str(datum))
        if search_range:
            self._request_url = "%sSearchRange=%s" % (self._request_url, str(search_range))
        if prefecture:
            self._request_url = "%s&Prefecture=%s" % (self._request_url, str(convert2prefecture_parameter(prefecture)))
        if station:
            query = [('Station', station)]
            self._request_url = "%s&%s" % (self._request_url, urllib.urlencode(query))
        if result_set:
            self._request_url = "%s&ResultSet=%s" % (self._request_url, str(result_set))
        if sort_order:
            self._request_url = "%s&SortOrder=%s" % (self._request_url, str(sort_order))
        if page_num:
            self._request_url = "%s&PageNum=%d" % (self._request_url, str(page_num))
        if result_datum:
            self._request_url = "%s&ResultDatum=%d" % (self._request_url, str(result_datum))

        f = urllib2.urlopen(self._request_url)
        soup = BeautifulSoup(f.read())
        self._search_results = soup.findAll('item')
        return self._search_results


def demo():
    key = 'Your access key here.'
    prefecture = '東京'
    station = '渋谷'
    tabelog = TabeLog(key)
    restaurants = tabelog.search_restaurant(prefecture=prefecture, station=station)
    for restaurant in restaurants:
        print restaurant


if __name__ == '__main__':
    demo()

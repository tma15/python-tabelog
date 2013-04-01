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
    try:
        return prefecture_map[prefecture]
    except KeyError:
        sys.exit('invalid prefecture name: %s' % prefecture)


class Tabelog:
    def __init__(self, access_key):
        self._access_key = access_key

    def _extract_items(self, request_url):
        try:
            fd = urllib2.urlopen(request_url)
        except urllib2.HTTPError, err:
            sys.exit(err.read())
        soup = BeautifulSoup(fd.read())
        _search_results = soup.findAll('item')
        return _search_results

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
        _request_url = 'http://api.tabelog.com/Ver2.1/RestaurantSearch/?Key=%s' % self._access_key
        if lattitude:
            _request_url = "%sLatitude=%f" % (_request_url, float(lattitude))
        if longitude:
            _request_url = "%sLongitude=%f" % (_request_url, float(longitude))
        if datum and lattitude and longitude: ### valid if both lattitude and longitude are specified
            _request_url = "%sDatum=%s" % (self._request_url, str(datum))
        if search_range:
            _request_url = "%sSearchRange=%s" % (_request_url, str(search_range))
        if prefecture:
            _request_url = "%s&Prefecture=%s" % (_request_url, str(convert2prefecture_parameter(prefecture)))
        if station:
            query = [('Station', station)]
            _request_url = "%s&%s" % (_request_url, urllib.urlencode(query))
        if result_set:
            _request_url = "%s&ResultSet=%s" % (_request_url, str(result_set))
        if sort_order:
            _request_url = "%s&SortOrder=%s" % (_request_url, str(sort_order))
        if page_num:
            _request_url = "%s&PageNum=%d" % (_request_url, str(page_num))
        if result_datum:
            _request_url = "%s&ResultDatum=%d" % (_request_url, str(result_datum))
        _search_results = self._extract_items(_request_url)
        _restaurants = [Restaurant(item) for item in _search_results]
        return _restaurants

    def search_review(self, restaurant_cord, sort_order=None, page_num=None):
        _request_url = 'http://api.tabelog.com/Ver1/ReviewSearch/?Key=%s&Rcd=%d' % (self._access_key, int(restaurant_cord))
        if sort_order:
            _request_url = "%s&SortOrder=%s" % (_request_url, sort_order)
        if page_num:
            _request_url = "%s&PageNum=%d" % (_request_url, int(page_num))
        _search_results = self._extract_items(_request_url)
        _reviews = [Review(item) for item in _search_results]
        return _reviews

    def search_restaurant_image(self, restaurant_cord):
        _request_url = 'http://api.tabelog.com/Ver1/ReviewImageSearch/?Key=%s&Rcd=%d' % (self._access_key, int(restaurant_cord))
        _search_results = self._extract_items(_request_url)
        images = [Image(item) for item in _search_results]
        return images


class Restaurant(object):
    def __init__(self, soup_item):
        self._soup_item = soup_item
        self._rcd = None
        self._name = None
        self._tabelogurl = None
        self._tabelogmobileurl = None
        self._totalscore = None
        self._tastescore = None
        self._servicescore = None
        self._moodscore = None
        self._situation = None
        self._dinnerprice = None
        self._lunchprice = None
        self._category = None
        self._station = None

    @property
    def rcd(self):
        if self._rcd == None:
            self._rcd = int(self._soup_item.find('rcd').renderContents())
        return self._rcd

    @property
    def name(self):
        if self._name == None:
            self._name = self._soup_item.find('restaurantname').renderContents()
        return self._name

    @property
    def tabelogurl(self):
        if self._tabelogurl == None:
            self._tabelogurl = self._soup_item.find('tabelogurl').renderContents()
        return self._tabelogurl

    @property
    def tabelogmobileurl(self):
        if self._tabelogmobileurl == None:
            self._tabelogmobileurl = self._soup_item.find('tabelogmobileurl').renderContents()
        return self._tabelogmobileurl

    @property
    def totalscore(self):
        if self._totalscore == None:
            self._totalscore = self._soup_item.find('totalscore').renderContents()
            if self._totalscore:
                self._totalscore = float(self._totalscore)
        return self._totalscore

    @property
    def tastescore(self):
        if self._tastescore == None:
            self._tastescore = self._soup_item.find('tastescore').renderContents()
            if self._tastescore:
                self._tastescore = float(self._tastescore)
        return self._tastescore

    @property
    def servicescore(self):
        if self._servicescore == None:
            self._servicescore = self._soup_item.find('servicescore').renderContents()
            if self._servicescore:
                self._servicescore = float(self._servicescore)
        return self._servicescore

    @property
    def moodscore(self):
        if self._moodscore == None:
            self._moodscore = self._soup_item.find('moodscore').renderContents()
            if self._moodscore:
                self._moodscore = float(self._moodscore)
        return self._moodscore

    @property
    def situation(self):
        if self._situation == None:
            self._situation = self._soup_item.find('situation').renderContents()
        return self._situation

    @property
    def dinnerprice(self):
        if self._dinnerprice == None:
            self._dinnerprice = self._soup_item.find('dinnerprice').renderContents()
        return self._dinnerprice

    @property
    def lunchprice(self):
        if self._lunchprice == None:
            self._lunchprice = self._soup_item.find('lunchprice').renderContents()
        return self._lunchprice

    @property
    def category(self):
        if self._category == None:
            self._category = self._soup_item.find('category').renderContents()
        return self._category

    @property
    def station(self):
        if self._station == None:
            self._station = self._soup_item.find('station').renderContents()
        return self._station


class Review(object):
    def __init__(self, soup_item):
        self._soup_item = soup_item
        self._nickname = None
        self._visitdate = None
        self._reviewdate = None
        self._usetype = None
        self._situation = None
        self._totalscore = None
        self._tastescore = None
        self._servicescore = None
        self._moodscore = None
        self._dinnerprice = None
        self._lunchprice = None
        self._title = None
        self._pcsiteurl = None
        self._mobilesiteurl = None

    @property
    def nickname(self):
        if self._nickname == None:
            self._nickname = self._soup_item.find('nickname').renderContents()
        return self._situation

    @property
    def visitdate(self):
        if self._visitdate == None:
            self._visitdate = self._soup_item.find('visitdate').renderContents()
        return self._situation

    @property
    def reviewdate(self):
        if self._reviewdate == None:
            self._reviewdate = self._soup_item.find('reviewdate').renderContents()
        return self._situation

    @property
    def usetype(self):
        if self._usetype == None:
            self._usetype = self._soup_item.find('usetype').renderContents()
        return self._situation

    @property
    def situation(self):
        if self._situation == None:
            self._situation = self._soup_item.find('situation').renderContents()
        return self._situation

    @property
    def totalscore(self):
        if self._totalscore == None:
            self._totalscore = self._soup_item.find('totalscore').renderContents()
            if self._totalscore:
                self._totalscore = float(self._totalscore)
        return self._totalscore

    @property
    def tastescore(self):
        if self._tastescore == None:
            self._tastescore = self._soup_item.find('tastescore').renderContents()
            if self._tastescore:
                self._tastescore = float(self._tastescore)
        return self._tastescore

    @property
    def servicescore(self):
        if self._servicescore == None:
            self._servicescore = self._soup_item.find('servicescore').renderContents()
            if self._servicescore:
                self._servicescore = float(self._servicescore)
        return self._servicescore

    @property
    def moodscore(self):
        if self._moodscore == None:
            self._moodscore = self._soup_item.find('moodscore').renderContents()
            if self._moodscore:
                self._moodscore = float(self._moodscore)
        return self._moodscore

    @property
    def situation(self):
        if self._situation == None:
            self._situation = self._soup_item.find('situation').renderContents()
        return self._situation

    @property
    def dinnerprice(self):
        if self._dinnerprice == None:
            self._dinnerprice = self._soup_item.find('pricedinner').renderContents()
        return self._dinnerprice

    @property
    def lunchprice(self):
        if self._lunchprice == None:
            self._lunchprice = self._soup_item.find('pricelunch').renderContents()
        return self._lunchprice

    @property
    def title(self):
        if self._title == None:
            self._title = self._soup_item.find('title').renderContents()
        return self._title

    @property
    def pcsiteurl(self):
        if self._pcsiteurl == None:
            self._pcsiteurl = self._soup_item.find('pcsiteurl').renderContents()
        return self._title

    @property
    def mobilesiteurl(self):
        if self._mobilesiteurl == None:
            self._mobilesiteurl = self._soup_item.find('mobilesiteurl').renderContents()
        return self._title


class Image(object):
    def __init__(self, soup_item):
        self._soup_item = soup_item
        self._urls = None
        self._urlm = None
        self._urll = None
        self._comment = None
        self._pcsiteurl = None
        self._mobilesiteurl = None

    @property
    def urls(self):
        if self._urls == None:
            self._urls = self._soup_item.find('imageurls').renderContents()
        return self._urls

    @property
    def urlm(self):
        if self._urlm == None:
            self._urlm = self._soup_item.find('imageurlm').renderContents()
        return self._urlm

    @property
    def urll(self):
        if self._urll == None:
            self._urll = self._soup_item.find('imageurll').renderContents()
        return self._urll

    @property
    def comment(self):
        if self._comment == None:
            self._comment = self._soup_item.find('imagecomment').renderContents()
        return self._comment

    @property
    def pcsiteurl(self):
        if self._pcsiteurl == None:
            self._pcsiteurl = self._soup_item.find('pcsiteurl').renderContents()
        return self._pcsiteurl

    @property
    def mobilesiteurl(self):
        if self._mobilesiteurl == None:
            self._mobilesiteurl = self._soup_item.find('mobilesiteurl').renderContents()
        return self._mobilesiteurl



def demo():
    key = 'Your access key here.'
    prefecture = '東京'
    station = '渋谷'
    tabelog = Tabelog(key)
    restaurants = tabelog.search_restaurant(prefecture=prefecture, station=station)
    for restaurant in restaurants:
        print 'rcd:', restaurant.rcd
        print 'name:', restaurant.name
        print 'url:', restaurant.tabelogurl
        print 'mobile url:', restaurant.tabelogmobileurl
        print 'dinner price:', restaurant.dinnerprice
        print 'lunch price:', restaurant.lunchprice
        print 'total score:', restaurant.totalscore
        print 'taste score:', restaurant.tastescore
        print 'service score:', restaurant.servicescore
        print 'mood score:', restaurant.moodscore
        print 'category:', restaurant.category
        print 'station:', restaurant.station
        print 'situation:', restaurant.situation
#    reviews = tabelog.search_review(13004626)
#    for review in reviews:
#        print 'nickname:', review.nickname
#        print 'title:', review.title
#        print 'dinner price:', review.dinnerprice
#        print 'lunch price:', review.lunchprice
#        print 'total score:', review.totalscore
#        print 'service score:', review.servicescore
#        print 'taste score:', review.tastescore
#        print 'mood score:', review.moodscore
#    images = tabelog.search_restaurant_image(13004626)
#    for img in images:
#        print 'url small:', img.urls
#        print 'url medium:', img.urlm
#        print 'url large:', img.urll
#        print 'comment:', img.comment
#        print 'pc site url:', img.pcsiteurl
#        print 'mobile site url:', img.mobilesiteurl


if __name__ == '__main__':
    demo()

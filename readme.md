python-tabelog
====================

Install
--------------------

    git clone https://github.com/tma15/python-tabelog.git
    cd python-tabelog
    python setup.py install

Example
--------------------

    key = 'Your access key here.'
    tabelog = Tabelog(key)
    prefecture = '東京'
    station = '渋谷'
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


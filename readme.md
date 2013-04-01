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
    tabelog = TabeLog(key)
    prefecture = '東京'
    station = '渋谷'
    restaurants = tabelog.search_restaurant(prefecture=prefecture, station=station)
    for restaurant in restaurants:
        print restaurant

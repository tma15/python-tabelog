python-tabelog
====================

Example
--------------------

    key = 'Your access key here.'
    tabelog = TabeLog(key)
    prefecture = '東京'
    station = '渋谷'
    restaurants = tabelog.search_restaurant(prefecture=prefecture, station=station)
    for restaurant in restaurants:
        print restaurant

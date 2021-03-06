# encoding: utf-8
# author:   Jan Hybs
import time
import datetime


def pretty_date (time=False, now_=None):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    now = datetime.now () if now_ is None else now_
    if type (time) is int or type (time) is float:
        diff = now - datetime.fromtimestamp (time)
    elif isinstance (time, datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str (second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str (second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str (second_diff / 3600) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str (day_diff) + " days ago"
    if day_diff < 31:
        return str (day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str (day_diff / 30) + " months ago"
    return str (day_diff / 365) + " years ago"


start_time = time.time ()


def millis (since_start=False):
    """
    function which returns current or relative timestamp based on given param
    :param since_start:
    :return:
    """
    dt = time.time () - start_time if since_start else time.time ()
    return int (dt * 1000)

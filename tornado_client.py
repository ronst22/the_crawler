#!/usr/bin/python

import httplib, urllib2, urllib, cookielib

class Client():
    def __init__(self):
        pass

    def is_offensive(self, text):
        """Ask the service if the text is offensive"""
        params = urllib.urlencode({'text': text})
        headers = {"Content-type": "application/form-data", "Accept": "text/plain"}
        opener = urllib2.build_opener()
        req = urllib2.Request("http://104.214.70.4", params, headers)
        res = opener.open(req)
        return res.read() == "True"
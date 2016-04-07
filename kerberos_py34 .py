#!/bin/python

import platform
import sys
import os
import argparse
import json
from pprint import pprint


import urllib2

import kerberos 
import urllib2_kerberos


import cookielib

import httplib
import urllib
import requests
from requests_kerberos import HTTPKerberosAuth, OPTIONAL, DISABLED
'''
import logging
try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
http_client.HTTPConnection.debuglevel = 1


# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig() 
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
'''

def main():
    
    url = '<url>'
    # Disable proxy
    proxy_support = urllib2.ProxyHandler({})
    handler = urllib2.HTTPSHandler(debuglevel=1)
    opener = urllib2.build_opener(handler, proxy_support)
    cj = cookielib.CookieJar()
    opener.add_handler(urllib2.HTTPCookieProcessor(cj))
    opener.add_handler(urllib2_kerberos.HTTPKerberosAuthHandler(mutual=False))
   
    value = {"name1":"val1", "attrs":{"ip":"1.2.3.4"}}
    # data = urllib.urlencode(value) # urlencode will introduce 'server error 500' because of the server side config

    try:
        headers = {
            "Content-Type": "application/json"
            }
        
        #req = urllib2.Request(url, data, headers)
        req = urllib2.Request(url, '{"name1":"val1", "attrs":{"ip":"1.2.3.4"}}', headers)
        resp = opener.open(req) 

        '''
        resp = requests.post(url, 
                            auth=HTTPKerberosAuth(),#mutual_authentication=DISABLED,
                            data,
                            verify=False, headers=headers)
        '''
        contents = resp.read()
        data = json.loads(contents)
        pprint(data)
        #pprint(contents)
    except urllib2.HTTPError as error:
        contents = error.read()
        print ("--------------------- exception captured --------------------")
        pprint(contents)
    

if __name__ == "__main__":
    main()
#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import requests
from lxml import etree
from test import ShellParse
from zabbix_api import Zabbix

def zabbix_server(token, ip, area):
    session = requests.Session()
    session.keep_alive = False
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
        'cookie': 'zbx_sessionid=' + token,
        "ctsso-secret": "sebk2rgn2xqfycme4pvscml62fkeoh5b"
    }
    response = session.get(url='http://' + ip + '/system/' + area + '/zabbix.php?action=report.status&ddreset=1', headers=headers)
    html_str = response.content.decode()
    print html_str

zabbix = Zabbix('http://10.129.133.205/system/5fcb35fe60044b96935bb79e276c78c2/index.php', 'Admin', 'zabbix')
token = zabbix.user_login('Admin', 'zabbix')
zabbix_server(token, '10.129.133.205', '5fcb35fe60044b96935bb79e276c78c2')
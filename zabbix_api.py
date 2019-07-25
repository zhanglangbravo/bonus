#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import time
import urllib2


class Zabbix(object):
    def __init__(self, zbx_url, username, password):
        self.url = zbx_url
        self.header = {"Content-Type": "application/json","ctsso-secret":"sebk2rgn2xqfycme4pvscml62fkeoh5b"}
        self.authID = self.user_login(username, password)

    def user_login(self, username, password):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                    "user": username,
                    "password": password
                },
                "id": 0
            })
        request = urllib2.Request(self.url, data=data.encode(encoding='UTF8'))
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except urllib2.URLError as e:
            # print "Auth Failed, Please Check Net and Name And Password:", e.message
            pass
        else:

            response = json.loads(result.read())
            result.close()
            authID = response['result']
            return authID

    def get_params(self):
        return self.__dict__

    def get_data(self, data):
        headers = {'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0'}
        request = urllib2.Request(self.url, data.encode(encoding='UTF8'),headers)
        for key in self.header:
            request.add_header(key, self.header[key])

        retry = 0
        while(True):
            try:
                result = urllib2.urlopen(request)
            except urllib2.URLError as e:
                if hasattr(e, 'reason'):
                    print 'We failed to reach a server.'
                    print 'Reason: ', e.reason
                    if retry < 5:
                        print "retry"+str(retry)
                        retry+=1
                        time.sleep(1)
                        continue
                elif hasattr(e, 'code'):
                    print 'The server could not fulfill the request.'
                    print 'Error code: ', e.code
                return 0
            else:
                response = json.loads(result.read())
                result.close()
                return response

    def item_get(self, hostid, name="", key=""):
        data = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "item.get",
                "params": {
                    "output": ["itemid", "key_", "name", "lastvalue"],
                    "hostids": hostid,
                    "search": {"name": name, "key_": key}
                },
                "auth": self.authID,
                "id": 1
            })
        result = self.get_data(data)['result']
        return result

    def massadd(self, key, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": key + ".massadd",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        result_data = self.get_data(data)
        result = result_data['result']
        return result

    def host_get_ids(self, hostname):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.get",
            "params": {
                "output": ["name"],
                "filter": {"name": hostname}
            },
            "auth": self.authID,
            "id": 1
        })
        result = self.get_data(data)['result']
        return result

    def hostGroup_get_ids(self, hostGroupNames):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "hostgroup.get",
            "params": {
                "output": "groupid",
                "filter": {
                    "name": hostGroupNames
                }
            },
            "auth": self.authID,
            "id": 1
        })
        result = self.get_data(data)['result']
        return result

    def host_createSNMP(self, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "host.create",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        data= self.get_data(data)
        print data
        result = data['result']
        return result

    def templates_get_ids(self, templateNames):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "template.get",
            "params": {
                "output": "templateid",
                "filter": {
                    "host": templateNames
                }
            },
            "auth": self.authID,
            "id": 1
        })
        result = self.get_data(data)['result']
        return result

    def graph_getByItemid(self, itemid):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "graph.get",
            "params": {
                "output": "extend",
                "itemids": itemid,
                "sortfield": "name"
            },
            "auth": self.authID,
            "id": 1
        })
        result = self.get_data(data)['result']
        return result

    def tigger_create(self, description, expression, priority=3):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": {
                "description": description,
                "expression": expression,
                "priority": priority
            },
            "auth": self.authID,
            "id": 1
        })
        result = self.get_data(data)['result']
        return result

    def screen_create(self, name, hsize, vsize, screenitems):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "screen.create",
            "params": {
                "name": name,
                "hsize": hsize,
                "vsize": vsize,
                "screenitems": screenitems
            },
            "auth": self.authID,
            "id": 1
        })
        # 注意此处报错，多是由于 宽、高设置超过了100
        result_data = self.get_data(data)
        result = result_data['result']
        return result

    def key_create(self, key, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": key + ".create",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        result = self.get_data(data)['result']
        return result

    def key_get(self, key, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": key + ".get",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        result_data = self.get_data(data)
        result = result_data['result']
        return result

    def execute(self, key, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": key + ".execute",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        result_data = self.get_data(data)
        return result_data

    def key_update(self, key, params):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": key + ".update",
            "params": params,
            "auth": self.authID,
            "id": 1
        })
        result_data = self.get_data(data)
        print result_data
        result = result_data['result']
        return result
   # def key_delete(self, key, params):
   #     data = json.dumps({
   #         "jsonrpc": "2.0",
   #         "method": key + ".delete",
   #         "params": params,
   #         "auth": self.authID,
   #         "id": 1
   #     })
   #     result_data = self.get_data(data)
   #     print result_data
   #     result = result_data['result']
   #     return result

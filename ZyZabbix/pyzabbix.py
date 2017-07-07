#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json


class ZabbixAPIException:
    """ generic zabbix api exception
    code list:
         -32602 - Invalid params (eg already exists)
         -32500 - no permissions
    """

    def __init__(self, exception):
        self.exception = exception
        print(self.exception)


class ZabbixAPI:
    def __init__(self,
                 server='http://localhost/zabbix',
                 session=None,
                 timeout=None):
        '''
        :param server: Base URI for zabbix web interface (omitting /api_jsonrpc.php)
        :param session:optional pre-configured requests.Session instance
        :param timeout:optional connect and read timeout in seconds, default: None
        '''
        if session:
            self.session = session
        else:
            self.session = requests.Session()
        # Default headers for all requests
        self.session.headers.update({
            'Content-Type': 'application/json-rpc',
            'User-Agent': 'python/pyzabbix',
            'Cache-Control': 'no-cache'
        })
        self.auth = ''
        self.id = 0
        self.timeout = timeout
        self.url = server + '/api_jsonrpc.php'

    def login(self, user='', password=''):
        """
           :param password: Password used to login into Zabbix
           :param user: Username used to login into Zabbix
        """
        # If we have an invalid auth token, we are not allowed to send a login
        # request. Clear it before trying.
        try:
            self.auth = self.user.login(user=user, password=password)
            print(self.auth)
        except Exception:
            ZabbixAPIException('连接异常')

    def confimport(self, confformat='', source='', rules=''):
        """Alias for configuration.import because it clashes with
           Python's import reserved keyword
           :param rules:
           :param source:
           :param confformat:
        """
        return self.do_request(
            method="configuration.import",
            params={"format": confformat, "source": source, "rules": rules}
        )['result']

    def do_request(self, method, params=None):
        request_json = {
            'jsonrpc': '2.0',
            'method': method,
            'params': params or {},
            'id': self.id,
        }

        # 调用api需要加入认证信息，但是登录api和查看api版本（apiinfo.version）不需要加入。
        if self.auth and method != 'apiinfo.version':
            request_json['auth'] = self.auth

        response = self.session.post(
            self.url,
            data=json.dumps(request_json),
            timeout=self.timeout
        )

        # NOTE: Getting a 412 response code means the headers are not in the
        # list of allowed headers.
        response.raise_for_status()

        if not len(response.text):
            raise ZabbixAPIException("Received empty response")

        try:
            response_json = json.loads(response.text)
        except ValueError:
            raise ZabbixAPIException(
                "Unable to parse json: %s" % response.text
            )

        self.id += 1

        if 'error' in response_json:  # some exception
            if 'data' not in response_json['error']:  # some errors don't contain 'data': workaround for ZBX-9340
                response_json['error']['data'] = "No data"
            msg = "Error {code}: {message}, {data}".format(
                code=response_json['error']['code'],
                message=response_json['error']['message'],
                data=response_json['error']['data']
            )
            raise ZabbixAPIException(msg, response_json['error']['code'])

        return response_json

    def __getattr__(self, attr):
        """Dynamically create an object class (ie: host)"""
        return ZabbixAPIObjectClass(attr, self)   # user.login ==> attr=user
        # zapi.user：返回ZabbixAPIObjectClass类对象，并传入参数user和ZabbixAPI对象；
        # zapi.user.login：去ZabbixAPIObjectClass类找login方法


class ZabbixAPIObjectClass:
    def __init__(self, name, parent):
        self.name = name   # name = user
        self.parent = parent # parent = ZabbixAPI对象

    def __getattr__(self, attr):  # attr = login
        """Dynamically create a method (ie: get)"""
        def fn(*args, **kwargs):
            if args and kwargs:
                raise TypeError("Found both args and kwargs")

            return self.parent.do_request(
                '{0}.{1}'.format(self.name, attr),
                args or kwargs
            )['result']

        return fn


# zapi = ZabbixAPI("http://10.0.0.61/zabbix/")
# zapi.login('Admin', 'zabbix')

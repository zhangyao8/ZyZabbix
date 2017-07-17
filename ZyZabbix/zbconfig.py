#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os
from ZyZabbix import pyzabbix

zabbixInfoFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zabbix_info.conf')
zabbixInfoConfig = configparser.ConfigParser()


def readInfo():
    zabbixInfoConfig.read(zabbixInfoFile, encoding='utf-8')


def getInfo(key):
    return zabbixInfoConfig.get('zabbix_info', key)


def setInfo(key, value):
    zabbixInfoConfig.set('zabbix_info', key, value)


def writeInfo():
    zabbixInfoConfig.write(open(zabbixInfoFile, 'w'))


def login_zabbix():
    readInfo()
    zabbixurl = getInfo('zabbix_web')
    zabbixsess = getInfo('zabbix_sess')
    zabbixuser = getInfo('zabbix_user')
    zabbixpass = getInfo('zabbix_pass')
    zabbixip = getInfo('zabbix_server')
    zabbixstatus = 1
    zapi = pyzabbix.ZabbixAPI(zabbixurl, timeout=1)
    zapi.auth = zabbixsess
    result = zapi.user.get(countOutput=1)
    if "error1" in result:
        zabbixsess = zapi.login(zabbixuser, zabbixpass)
        if "error1" in zabbixsess:
            zabbixstatus = 0
        else:
            setInfo('zabbix_sess', zabbixsess)
            writeInfo()
    elif "error2" in result:
        zabbixsess = result
        zabbixstatus = 0

    result = {
        'zabbixurl': zabbixurl,
        'zabbixuser': zabbixuser,
        'zabbixpass': zabbixpass,
        'zabbixip': zabbixip,
        'zabbixsess': zabbixsess,
        'zabbixstatus': zabbixstatus,
        'zapi': zapi
    }
    return result

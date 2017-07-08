#!/usr/bin/env python
# -*- coding: utf-8 -*-
import configparser
import os

zabbix_info_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zabbix_info.conf')
zabbix_info_config = configparser.ConfigParser()


def read_info():
    zabbix_info_config.read(zabbix_info_file, encoding='utf-8')

def get_info(key):
    return zabbix_info_config.get('zabbix_info', key)


def set_info(key, value):
    zabbix_info_config.set('zabbix_info', key, value)


def write_info():
    zabbix_info_config.write(open(zabbix_info_file, 'w'))

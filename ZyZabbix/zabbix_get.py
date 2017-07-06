#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket

def gethostname(ip,port,timeout=3):
    client_socket = None
    try:
        client_socket = socket.create_connection((ip, port), timeout)
        client_socket.sendall(bytes("system.hostname", encoding='utf8'))
        ret_bytes1 = client_socket.recv(5)
        if ret_bytes1 != b'ZBXD\x01':
            return '检查是否有访问权限'
        ret_bytes2 = client_socket.recv(8)
        ret_bytes3 = client_socket.recv(65535)
        ret_str3 = str(ret_bytes3, encoding='utf8')
        return ret_str3
    except Exception as e:
        return "Unable to receive data from agent: {0}".format(e)
    finally:
        if client_socket is not None:
            client_socket.close()

# a = check('10.0.0.61', 10050)
# print(a)
# # check('10.0.0.62', 10050)

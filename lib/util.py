#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lcy
# @Date:   2016-09-20 13:46:52
# @Last Modified by:   Lcy
# @Last Modified time: 2016-09-26 16:34:41
import os
from socket import gethostbyname
from urlparse import urlsplit
import math
def getWebsiteExp():
    path = os.path.split(os.path.realpath(__file__))[0].replace('lib','')
    exps = os.listdir(path + '/exploits/website/')
    fil = lambda str:(True, False)[str[-3:] == 'pyc' or str.find('__init__.py') != -1]
    return filter(fil, exps)

def getServerExp():
    path = os.path.split(os.path.realpath(__file__))[0].replace('lib','')
    exps = os.listdir(path+ '/exploits/server/')
    fil = lambda str:(True, False)[str[-3:] == 'pyc' or str.find('__init__.py') != -1]
    return filter(fil, exps)
#生成扫描结果
def saveHead(filename):
    head = '''
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <meta charset="utf-8">
                    <title>LcyScan</title>
                    <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css"> 
                    <link rel="stylesheet" href="http://cdn.bootcss.com/font-awesome/4.2.0/css/font-awesome.min.css"> 
                    <script src="http://cdn.bootcss.com/jquery/2.1.3/jquery.min.js"></script>
                </head>
                <style>
                   
                    table { 
                    table-layout: fixed;
                    word-wrap:break-word;
                    }
                </style>
                <body>
                    <table class="table table-hover" style="width:100%;hegiht:100%;">
                        <thead>
                            <tr>
                              <th>url</th>
                              <th>存在漏洞的插件</th>
                              <th>插件名称</th>
                              <th>漏洞来源</th>
                              <th>执行结果</th>
                              <th>类型</th>
                            </tr>
                        </thead>
                        <tbody>
    '''
    f = open(filename,"a")
    f.write(head)
    f.close
def saveFoot(filename):
    head = '''
                        </tbody>
            </table>
        </body>
    </html>
    '''
    f = open(filename,"a")
    f.write(head)
    f.close
def saveResult(filename,result):
    html = "<tr>"
    html += '<td>' + result['target'] + '</td>'
    html += '<td>' + result['filename'] + '</td>'
    html += '<td>' + result['name'] + '</td>'
    html += '<td>' + result['ref'] + '</td>'
    html += '<td>' + result['info'] + '</td>'
    html += '<td>' + result['type'] + '</td>'
    html += '</tr>'
    f = open(filename,"a")
    f.write(html)
    f.close()
def url2ip(url):
    """
    works like turning 'http://baidu.com' => '180.149.132.47'
    """
    iport = urlsplit(url)[1].split(':')
    if len(iport) > 1:
        return gethostbyname(iport[0])
    return gethostbyname(iport[0])
def url_seg(url_list, process_num):
    # [1,2,3,4,5,6,7,8,9] to [[1, 2, 3, 4], [5, 6, 7, 8], [9]]
    n = int(math.ceil(len(url_list) / float(process_num)))
    return [url_list[i:i + n] for i in range(0, len(url_list), n)]
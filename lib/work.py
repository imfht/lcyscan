#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lcy
# @Date:   2016-09-20 14:52:30
# @Last Modified by:   Lcy
# @Last Modified time: 2016-09-27 16:32:55
import threading
import Queue
import sys
from util import saveResult
from Color import *
from consle_width import getTerminalSize
from requests import RequestException
from urllib2 import URLError
import socket
class Work():  
    def __init__(self,types,tnum,que=None,targets=None,filename=None):  
        if types =='website':
            sys.path.append('exploits/website')
        else:
            sys.path.append('exploits/server')
        self.type=type
        self.tnum = int(tnum)
        self.que = que 
        self.targets = targets
        self.filename = filename
        self.lock = threading.Lock()
        self.console_width = getTerminalSize()[0] - 2
        self.maxpross = que.qsize() * len(targets)
        self.pross = 0
        self.tq = Queue.Queue()
        socket.setdefaulttimeout(5)
    def start(self): 
        ts = []
        for i in range(self.tnum):
                t = threading.Thread(target=self.works)
                t.setDaemon(True)
                ts.append(t)
                t.start()
        for t in ts:
            t.join()
    def works(self):
        while self.que.qsize() > 0:
            exp = self.que.get_nowait() 
            m = __import__(exp[:-3])
            myplugin = getattr(m, "Exploit")
            #只剩一个插件,启动线程
            if self.que.qsize() == 0:
                for target in self.targets:
                    self.tq.put(target)
                ts = []
                for i in range(self.tnum):
                        t = threading.Thread(target=self.task,args=(myplugin,exp))
                        ts.append(t)
                        t.start()
                for t in ts:
                    t.join()
            else:
                for target in self.targets:
                    self.pross = self.pross + 1
                    self.lock.acquire()
                    msg = '[*] %s|%s|%s' % (target,str(self.pross) + "/"+ str(self.maxpross),exp)
                    wi = self.console_width -len(msg)
                    if wi < 0:
                        msg = msg[0:self.console_width]
                    sys.stdout.write(msg + ' ' * (self.console_width -len(msg)) + '\r')
                    self.lock.release()
                    try:
                        p = myplugin(target,exp)
                        p.verify()
                        result = p.result
                        if result['status']:
                            self.lock.acquire()
                            msg = "[+] {target} | {file}".format(target=result['target'],file=exp)
                            color.cprint(msg + ' ' * (self.console_width -len(msg)),CYAN)
                            self.lock.release()
                            saveResult(self.filename,result)
                    except RequestException,e:
                        pass
                    except IOError,e:
                        pass
                    except Exception,e:
                        if e.message <> "":
                            # print dir(e)
                            print "error:%s|%s|%s" % (e.message,exp,target)
                            pass
    def task(self,myplugin,exp):
        while self.tq.qsize() > 0:
            target = self.tq.get_nowait() 
            self.pross = self.pross + 1
            self.lock.acquire()
            msg = '[*] %s|%s|%s' % (target,str(self.pross) + "/"+ str(self.maxpross),exp)
            wi = self.console_width -len(msg)
            if wi < 0:
                msg = msg[0:self.console_width]
            sys.stdout.write(msg + ' ' * (self.console_width -len(msg)) + '\r')
            self.lock.release()
            try:
                p = myplugin(target,exp)
                p.verify()
                result = p.result
                if result['status']:
                    self.lock.acquire()
                    msg = "[+] {target} | {file}".format(target=result['target'],file=exp)
                    color.cprint(msg + ' ' * (self.console_width -len(msg)),CYAN)
                    self.lock.release()
                    saveResult(self.filename,result)
            except RequestException,e:
                pass
            except IOError,e:
                pass
            except Exception,e:
                print "error:%s|%s|%s" % (e,exp,target)
                pass
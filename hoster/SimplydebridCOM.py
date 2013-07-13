#!/usr/bin/env python
# -*- coding: utf-8 -*-

from module.plugins.Hoster import Hoster
from module.utils import html_unescape
from urllib import quote, unquote
from time import sleep
import re

class SimplydebridCOM(Hoster):
    __name__ = "SimplydebridCOM"
    __version__ = "0.1"
    __type__ = "hoster"
    __pattern__ = r"http://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}/sd.php/*"
    __description__ = """simply-debrid.com hoster plugin"""
    __author_name__ = ("Kagenoshin")
    __author_mail__ = ("kagenoshin@gmx.ch")

    def setup(self):
        self.resumeDownload = self.multiDL = True
        self.chunkLimit = 1

    def process(self, pyfile):
        if not self.account:
            self.logError(_("Please enter your simply-debrid.com account or deactivate this plugin"))
            self.fail("No simply-debrid.com account provided")
        
        self.logDebug("simply-debrid.com: Old URL: %s" % pyfile.url)
        
        #fix the links for simply-debrid.com!
        new_url = pyfile.url
        new_url = new_url.replace("clz.to", "cloudzer.net/file")
        new_url = new_url.replace("http://share-online", "http://www.share-online")
        new_url = new_url.replace("ul.to", "uploaded.net/file")
        new_url = new_url.replace("uploaded.com", "uploaded.net")
        new_url = new_url.replace("filerio.com", "filerio.in")
        new_url = new_url.replace("lumfile.com", "lumfile.se")
        if('fileparadox' in new_url):
            new_url = new_url.replace("http://", "https://")
        
        if re.match(self.__pattern__, new_url):
            new_url = new_url
        else:
            page = self.req.load('http://simply-debrid.com/api.php?dl='+new_url)#+'&u='+self.user+'&p='+self.account.getAccountData(self.user)['password'])
            if('tiger Link' in page or 'Invalid Link' in page or ('API' in page and 'ERROR' in page)):
                self.fail('Unable to unrestrict link')
            new_url = page
        
        self.setWait(5)
        self.wait()
        self.logDebug("Unrestricted URL: " + new_url)
        
        self.download(new_url, disposition=True)
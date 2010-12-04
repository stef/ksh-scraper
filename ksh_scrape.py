#!/usr/bin/env python2.6

# Copyright (c) 2010 asciimoo - asciimoo@gmail.com
# Licensed under the GNU Affero General Public License v3

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from sys import argv, exit
import re, htmlentitydefs

SOUP = None

def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)

def getContent(url):
    global SOUP
    r = urlopen(url)
    SOUP = BeautifulSoup(unicode(r.read(), 'iso-8859-2'))
    r.close()

if len(argv) != 2:
    print '[!] Usage: %s [portal.ksh.hu _url] - e.g. http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_zoi011.html' % argv[0]
    exit(1)

URL = argv[1]
getContent(URL)
TITLE = unescape(SOUP.find(attrs={'id': 'title'}).first().find(text=True))
urlFolder = URL[:URL.rfind('/')]

TABLES = {}
morePages = SOUP.find(attrs={'id': 'pages'})
p = '1'
if morePages:
    p = morePages.find('span').attrs[0][1]
    for page in morePages.findAll('a'):
        getContent('/'.join((urlFolder, page.attrs[0][1])))
        TABLES[page.attrs[1][1]] = SOUP.find(attrs={'id': 'table'})


TABLES[p] = SOUP.find(attrs={'id': 'table'})

print TABLES.keys()
print URL
print TITLE
print len(TABLES)

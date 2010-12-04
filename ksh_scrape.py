#!/usr/bin/env python2.6

# Copyright (c) 2010 asciimoo - asciimoo@gmail.com
# Licensed under the GNU Affero General Public License v3

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
from sys import argv, exit, stdout
import re, htmlentitydefs
import csv

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

def mergeCaptions(soup):
    # get column headers
    headers=[]
    for row in soup.find(id="thead").findAll('tr'):
        i=0
        for col in row.findAll('th'):
            # skip final headers.
            while i<len(headers) and headers[i][1]:
                i+=1
            final=False
            rowspan=int(col.get('rowspan','1'))
            if rowspan==2:
                final=True
            if rowspan>2:
                raise ValueError, rowspan
            colspan=int(col.get('colspan','1'))
            if i>=len(headers):
                headers.extend([(col.string,final)]*colspan)
            else:
                for j in xrange(colspan):
                    headers[i+j]=("%s %s" % (headers[i+j][0],col.string),headers[i+j][1])
            i+=colspan
    return [x[0] for x in headers]

def getRows(data,all=True):
    return [[''.join(x.findAll(text=True)) for x in row.findAll('td')] if all else
            [''.join(x.string.split(' ')) if re.match('[0-9]+',''.join(x.string.split(' '))) else x.string for x in row.findAll('td') if x.string]
            for row in data.findAll('tr')]


if __name__ == "__main__":
    #if len(argv) != 2:
    #    print '[!] Usage: %s [portal.ksh.hu _url] - e.g. http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_zoi011.html' % argv[0]
    #    exit(1)
    #URL = argv[1]

    URL = 'http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_qli049.html'
    getContent(URL)
    TITLE = unescape(SOUP.find(attrs={'id': 'title'}).first().find(text=True))
    urlFolder = URL[:URL.rfind('/')]

    TABLES = []
    morePages = SOUP.find(attrs={'id': 'pages'})
    if morePages:
        for page in morePages.findAll('a'):
            TABLES.append('/'.join((urlFolder, page.attrs[0][1])))

    TABLES.append(SOUP.find(attrs={'id': 'table'}))

    print URL
    print TITLE.encode('utf8')
    #print len(TABLES)

    writer = csv.writer(stdout,dialect='excel')
    for soup in TABLES:
        captions=mergeCaptions(soup)
        writer.writerow([unicode(x).encode("utf8") for x in captions])
        writer.writerows([[unicode(item).encode("utf8") for item in row] for row in getRows(soup.find(id='tbody'),False) if row])

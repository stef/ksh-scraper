#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-

# Copyright (c) 2010 asciimoo - asciimoo@gmail.com, stefan.marsiske@gmail.com
# Licensed under the GNU Affero General Public License v3

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib import urlopen
from sys import argv, exit, stdout
import re, htmlentitydefs, csv, tidy

SEQ=False   # list multiple pages vertically (True) or append horizontally(False)?
ALL=False   # keep intermediate summaries?

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
    r = urlopen(url)
    xml = unicode(str(tidy.parseString(unicode(r.read(), 'iso-8859-2'), **{'output_xhtml' : 1,
                                             'add_xml_decl' : 0,
                                             'indent' : 0,
                                             'drop-proprietary-attributes': 1,
                                             'tidy_mark' : 0,
                                             'doctype' : "strict",
                                             'wrap' : 0})),'utf8')
    res = BeautifulSoup(xml)
    r.close()
    return res

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
    return [[''.join(''.join(x.findAll(text=True)).split(' '))
             if re.match('[0-9]+',''.join(''.join(x.findAll(text=True)).split(' ')))
             else ''.join(x.findAll(text=True)) for x in row.findAll('td')]
            if all else
            [''.join(x.contents[0].split(' '))
             if re.match('[0-9]+',''.join(x.contents[0].split(' ')))
             else x.contents[0]
             for x in row.findAll('td') if x and x.contents and isinstance(x.contents[0],NavigableString)]
            for row in data.findAll('tr')]

if __name__ == "__main__":
    if len(argv) != 2:
        print '[!] Usage: %s [portal.ksh.hu _url] - e.g. http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_zoi011.html' % argv[0]
        exit(1)
    URL = argv[1]
    if not re.match(r'http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/[a-z_]+/[a-z0-9.]', URL):
        print '[!] only http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/ urls allowed'
        exit(1)

    soup=getContent(URL)
    TITLE = unescape(soup.find(attrs={'id': 'title'}).first().find(text=True))
    urlFolder = URL[:URL.rfind('/')]

    TABLES = {}
    p=0
    morePages = soup.find(attrs={'id': 'pages'})
    if morePages:
        # handle multi-page data-sets
        p = morePages.find('span').attrs[0][1]
        for page in morePages.findAll('a'):
            other=getContent('/'.join((urlFolder, page.attrs[0][1])))
            TABLES[page.attrs[1][1]] = other.find(attrs={'id': 'table'})
    TABLES[p] = soup.find(attrs={'id': 'table'})

    # write out header
    writer = csv.writer(stdout,dialect='excel')
    writer.writerow([u'Cím'.encode('utf8'),unicode(TITLE).encode('utf8')])
    writer.writerow([u'Forrás'.encode('utf8'),URL])
    if(SEQ):
        # append every page to the bottom.
        for idx in sorted(TABLES.keys()):
            soup=TABLES[idx]
            captions=mergeCaptions(soup)
            writer.writerow([unicode(x).encode("utf8") for x in captions])
            writer.writerows([[unicode(item).encode("utf8") for item in row] for row in getRows(soup.find(id='tbody'),ALL) if row])
    else:
        # append every page to the right - horizontally.
        captions=[]
        rows=[]
        for idx in sorted(TABLES.keys()):
            soup=TABLES[idx]
            captions.extend(mergeCaptions(soup))
            for i,row in enumerate([x for x in getRows(soup.find(id='tbody'),False) if x]):
                if i>=len(rows)-1: rows.append([])
                rows[i].extend(row)
        writer.writerow([unicode(x).encode("utf8") for x in captions])
        writer.writerows([[unicode(item).encode("utf8") for item in row] for row in rows])

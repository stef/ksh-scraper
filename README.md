# KSH 2 CSV

is [H.A.C.K.](http://hspbp.org/) contribution to the [2010 Open Data Hackday](http://www.opendataday.org/). KSH is the [Hungarian Central Statistical Office](http://portal.ksh.hu/portal/page?_pageid=38,119919&_dad=portal&_schema=PORTAL) and it publishes it's data in some unprocessable html forms (btw those guys should look into sql injections to they precious Oracle DB).

## Usage

### console
    ksh_scrape.py http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_onp004b.html
### web
Use http://mx.ctrlc.hu/ksh-scrape?, simply append the URL from portal.ksh.hu to the ksh-scrape webservice, like this: [http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_zoi011.html](http://mx.ctrlc.hu/ksh-scrape?http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/xstadat_eves/i_zoi011.html)
### web + automagic
Using Greasemonkey [Firefox)[https://addons.mozilla.org/en-US/firefox/addon/748/), [Chrome](http://blog.chromium.org/2010/02/40000-more-extensions.html), [IE](http://www.gm4ie.com/), you can install also the [userscript](https://github.com/stef/ksh-scraper/raw/master/ksh2csv.user.js) which will automatically insert "download as CSV" links on the pages with html-encumbered data.

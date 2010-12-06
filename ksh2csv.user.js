// ==UserScript==
// @name               ksh2csv
// @description	     provides links to CSV versions of data found on the hungarian statistics office
// @include		        http://portal.ksh.hu/pls/ksh/docs/hun/xstadat/*
// ==/UserScript==

//    This file is part of ksh-scrape

//    ksh-scrape is free software: you can redistribute it and/or modify
//    it under the terms of the GNU Affero General Public License as published by
//    the Free Software Foundation, either version 3 of the License, or
//    (at your option) any later version.

//    ksh-scrape is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU Affero General Public License for more details.

//    You should have received a copy of the GNU Affero General Public License
//    along with ksh-scrape.  If not, see <http://www.gnu.org/licenses/>.

// (C) 2010 by Stefan Marsiske, <stefan.marsiske@gmail.com>

var scrapeserver="http://sbxo.ctrlc.hu/ksh-scrape?";

div = document.getElementById('title');
newlink = document.createElement('a');
newlink.setAttribute('href', scrapeserver+document.URL);
newlink.appendChild(document.createTextNode("CSV formátum"));
div.appendChild(newlink);

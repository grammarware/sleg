#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3
# -*- coding: utf-8 -*-

import os
import WikiPage

names = {}

for root, dirs, filenames in os.walk('wiki/'):
	for f in filter(lambda x:x.endswith('.md'),filenames):
		if f in ('Home.md'):
			continue
		print('--------------%s-------------' % f)
		p = WikiPage.WikiPage('wiki/%s' % f)
		p.validate()
		# q = open('newiki/%s' % f, 'w')
		# q.write(str(p))
		# q.close()
		# 
		for lang in p.getLanguages():
			if lang not in names.keys():
				names[lang] = []
			for name in p.getNames(lang):
				if name not in names[lang]:
					names[lang].append(name)
				try:
					f = open('up/sleg/%s.html' % name,'w')
					f.write(p.getHtml(name))
					f.close()
				except IOError:
					print(' !!! "%s" cannot be accessed' % name)

#
f = open('up/sleg/index.html','w')
f.write('''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary"/>
	<title>SL(E)BOK — SLEG</title>
	<link href="../www/sleg.css" rel="stylesheet" type="text/css"/>
</head>
<body>
<div class="left">
	<a href="index.html"><img src="../www/sleg.200.png" alt="Software Language Engineering Glossary (SLEG)" class="pad"/></a><br/>
	<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="CC-BY-SA"><img src="../www/cc-by-sa.png" alt="CC-BY-SA"/></a><br/>
	<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Open Knowledge"><img src="../www/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="../www/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="../www/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
</div>
<div class="main">
	<h1>SLEG is a work is progress!</h1>
	<h2>Unordered list of all possible pages</h2>• ''')
for l in WikiPage.languages:
	if l in names:
		f.write('<a href="#%s">%s<a> • ' % (l,l))
for i in range(0,len(WikiPage.languages)):
	if WikiPage.languages[i] not in names:
		continue
	s = '<hr/><h3>'
	if WikiPage.flags[i]:
		s += '<img src="../www/%s.png" alt="%s"/>' % (WikiPage.flags[i], WikiPage.languages[i])
	s += '<a name="%s"/>%s</h3>\n<div class="mult">\n' % (WikiPage.languages[i], WikiPage.languages[i])
	for name in names[WikiPage.languages[i]]:
		s += '<a href="%s.html">%s</a><br/>\n' % (name,name)
	f.write(s+'</div>')
f.write('''</div><div style="clear:both"/><hr />
	<div class="last">
		<em>
			<a href="http://github.com/grammarware/sleg">Software Language Engineering Glossary</a> (SLEG) is
			created and maintained by <a href="http://grammarware.net">Dr. Vadim Zaytsev</a>.
		</em>
	</div></body></html>''')
f.close()
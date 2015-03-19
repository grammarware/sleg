#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os
import WikiPage
from Formatting import TEMPLATES

names = {}

for root, dirs, filenames in os.walk('../slegwiki/'):
	for f in [x for x in filenames if x.endswith('.md') and x != 'Home.md']:
		print('--------------%s-------------' % f)
		p = WikiPage.WikiPage('../slegwiki/%s' % f)
		p.validate()
		# q = open('newiki/%s' % f, 'w')
		# q.write(str(p))
		# q.close()
		for lang in p.getLanguages():
			if lang not in names.keys():
				names[lang] = []
			for name in p.getNames(lang):
				if name not in names[lang]:
					names[lang].append(name)
				try:
					f = open('../slebok/sleg/%s.html' % name, 'w', encoding="utf-8")
					f.write(p.getHtml(name).replace('../slegwiki/', 'wiki/'))
					f.close()
				except IOError:
					print(' !!! "%s" cannot be accessed' % name)

#
f = open('../slebok/sleg/index.html', 'w', encoding="utf-8")
f.write(TEMPLATES['indexhead']+'''
	<h1>SLEG is a work in progress!</h1>
	<h2>Unordered list of all possible pages</h2>• ''')
for l in WikiPage.languages:
	if l in names:
		f.write('<a href="#%s">%s</a> • ' % (l, l))
for i in range(len(WikiPage.languages)):
	if WikiPage.languages[i] not in names:
		continue
	s = '<hr/><h3>'
	if WikiPage.flags[i]:
		s += '<img src="../www/%s.png" alt="%s"/>' % (WikiPage.flags[i], WikiPage.languages[i])
	s += '<a name="{0}"/>{0}</h3>\n<div class="mult">\n'.format(WikiPage.languages[i])
	for name in sorted(names[WikiPage.languages[i]]):
		s += '<a href="{0}.html">{0}</a><br/>\n'.format(name)
	f.write(s+'</div>')
f.write(TEMPLATES['footer'])
f.close()

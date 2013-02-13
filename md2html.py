#!/usr/local/bin/python
# -*- coding: utf-8 -*-
# not /Library/Frameworks/Python.framework/Versions/3.1/bin/python3

import os
import markdown
from urllib import unquote

languages = ('English', 'Russian', 'German', 'Dutch', 'French', 'Abbreviated as')

'''
* English: _waterfall model_ ([Wikipedia](http://en.wikipedia.org/wiki/Waterfall model))
* Russian: _каскадная модель_ ([Wikipedia](http://ru.wikipedia.org/wiki/Каскадная модель))
* Dutch: _watervalmethode_ ([Wikipedia](http://nl.wikipedia.org/wiki/Watervalmethode))
* German: _Wasserfallmodell_ ([Wikipedia](http://de.wikipedia.org/wiki/Wasserfallmodell))
'''
def readmd(fn):
	names = []
	html = ''
	f = open('wiki/%s' % fn, 'r')
	for line in f.readlines():
		if not line.strip():
			continue
		wrds = line.split(': ')
		if len(wrds) == 2:
			lhs = wrds[0].split('* ')[1]
			rhs = wrds[1].strip()
			if lhs in languages:
				term = line.split('_')[1]
				# print 'A language:',{lhs:term}
				if term.find('/') < 0:
					names.append(term)
				else:
					names.extend(term.split('/'))
			# else:
			#	 print 'Not a language:',{lhs:rhs}
		# lang = line.split('* ')[1].split(': _')[0]
		# term = line.split('_')[1]
		# links = 
		try:
			# print markdown.markdown(unicode(line.strip()))
			html += markdown.markdown(line.strip().decode('unicode-escape'))
			# print markdown.markdown(line.strip().decode('unicode-escape'))
		except UnicodeDecodeError:
			print('"%s" cannot be decoded' % line)
		# print '???'
	f.close()
	for name in names:
		try:
			f = open('up/%s.html' % name,'w')
			f.write('<html><head><title>%s</title></head><body>%s</body></html>' % (name, html.encode('unicode-escape')))
			f.close()
		except IOError:
			print('"%s" cannot be accessed' % name)

for root, dirs, filenames in os.walk('wiki/'):
	for f in filter(lambda x:x.endswith('.md'),filenames):
		# home.write('* [[%s]]\n' % f[:-3])
		print(f)
		readmd(f)
# home.close()
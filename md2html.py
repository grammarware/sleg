#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3
# -*- coding: utf-8 -*-

import os
# import markdown
# from urllib import unquote
import WikiPage

for root, dirs, filenames in os.walk('wiki/'):
	for f in filter(lambda x:x.endswith('.md'),filenames):
		# home.write('* [[%s]]\n' % f[:-3])
		if f in ('Home.md'):
			continue
		print(f)
		p = WikiPage.WikiPage('wiki/%s' % f)
		p.validate()
		for name in p.getNames():
			try:
				f = open('up/%s.html' % name,'w')
				# f.write('<html><head><title>%s</title></head><body>%s</body></html>' % (name, html.encode('unicode-escape')))
				f.write(p.getHtml(name))
				f.close()
			except IOError:
				print('"%s" cannot be accessed' % name)

#
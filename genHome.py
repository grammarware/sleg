#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os

home = open('../slegwiki/Home.md', 'w')
for root, dirs, filenames in os.walk('../slegwiki/'):
	for f in [x for x in filenames if x.endswith('.md')]:
		home.write('* [[%s]]\n' % f[:-3])
		print f
home.close()

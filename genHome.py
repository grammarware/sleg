#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os

home = open('wiki/Home.md','w')
for root, dirs, filenames in os.walk('wiki/'):
	for f in filter(lambda x:x.endswith('.md'),filenames):
		home.write('* [[%s]]\n' % f[:-3])
		print f
home.close()
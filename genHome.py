#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

home = open('../slegwiki/Home.md','w')
for root, dirs, filenames in os.walk('../slegwiki/'):
	for f in filter(lambda x:x.endswith('.md'),filenames):
		home.write('* [[%s]]\n' % f[:-3])
		print f
home.close()
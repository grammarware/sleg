#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import urllib, urllib2, httplib, socket

languages = ('en','ru','nl','de')

def safelyLoadURL(url):
	errors = 0
	while errors<3:
		try:
			return urllib.urlopen(url).read()
		except IOError,e:
	 		print 'Warning: failed to load URL, retrying...'
	 		errors += 1
		except socket.error,e:
			print 'Warning: connection reset by peer, retrying...'
			errors += 1
	print 'Error fetching URL:',url
	return ''

for root, dirs, filenames in os.walk('../slegwiki/'):
	for f in filter(lambda x:x.endswith('.md'),filenames):
		if f == 'Home.md':
			continue
		print f
		md = open('../slegwiki/%s' % f, 'r')
		topic = ''
		links = []
		for line in md.readlines():
			if not line:
				continue
			for chunk in line.split('[')[1:]:
				name = chunk.split(']')[0]
				if chunk.find('](')<0 or chunk.find('))')<0:
					print 'Skip line',chunk.strip()
					continue
				link = chunk.split('](')[1].split('))')[0]
				if name == 'Wikipedia':
					links.append(link)
		print 'Checking up',topic
		for link in links:
			print '----->',link
			rawlink = link.replace('.wikipedia.org/wiki/', '.wikipedia.org/w/index.php?title=')+'&action=raw'
			for iw in filter(lambda x:x.startswith('[[') and x.strip().endswith(']]') and x[2:4] in languages and x[4]==':', safelyLoadURL(rawlink).split('\n')):
				newlink = 'http://%s.wikipedia.org/wiki/%s' % (iw[2:4],iw.split(':')[1].split(']]')[0])
				newlink = newlink.replace('(','%28').replace(')','%29')
				if newlink not in links:
					print '  ?-->',newlink
		md.close()

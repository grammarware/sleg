#!/usr/local/bin/python

f = open('allfiles.md','r')
for line in f.readlines():
	if line.startswith('File:'):
		fname = line.split('File: ')[1].strip().capitalize()
		print fname
		g = open('wiki/%s.md' % fname, 'w')
	else:
		g.write(line)
f.close()
g.close()

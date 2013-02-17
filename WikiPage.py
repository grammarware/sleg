#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3
import os
import sys

languages = ('Short', 'English', 'German', 'French', 'Dutch', 'Russian')
flags =     (''     ,  'EN'    , 'DE'    , 'FR'    , 'NL'   , 'RU')
code = ('**','[[','`')

class WikiPage:
	def __init__(self, fname):
		self.main = fname
		self.items = {}
		self.pubs = []
		self.defin = None
		self.fig = ''
		f = open(fname,'r')
		self.text = f.readlines()
		f.close()
		for line in self.text:
			wrds = line.split(': ')
			if len(wrds) == 2:
				lhs = wrds[0].split('* ')[1]
				rhs = wrds[1].strip()
				if lhs in languages:
					self.items[lhs] = Entry(rhs)
				elif lhs == 'Publication':
					self.pubs.append(Publication(rhs))
				elif lhs == 'Definition':
					self.defin = MDText(rhs)
				elif lhs == 'Figure':
					self.fig = rhs
				else:
					print('Unknown line:',line)
			elif line.strip():
				print('Strange line:',line)
	def who(self):
		return self.__class__.__name__
	def validate(self):
		lines = list(filter(lambda x:x,map(lambda x:x.strip(),self.text)))
		for line in str(self).split('\n'):
			if not line:
				continue
			if line in lines:
				lines.remove(line)
			else:
				print(' * The original is expected to have line "%s"' % line)
		for line in lines:
			print(' * The original has unmatched line "%s"' % line)
	def getLanguages(self):
		return sorted(self.items.keys())
	def getNames(self,lang):
		return self.items[lang]
	def getKeywords(self):
		kws = []
		for lang in self.items.keys():
			kws.append(lang)
			# print(self.items[lang].getTitles())
			kws.extend(self.items[lang].getTitles())
		return kws
	def getHtml(self, main):
		s = '''<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
			<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, %s"/>
			<title>SL(E)BOK — SLEG — %s</title>
			<link href="www/sleg.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
		<div class="left">
			<a href="index.html"><img src="www/sleg.200.png" alt="Software Language Engineering Glossary (SLEG)" class="pad"/></a><br/>
			<div class="pad">[<a href="http://github.com/grammarware/sleg/%s/_edit">Edit!</a>]</div><br/>
			<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="CC-BY-SA"><img src="www/cc-by-sa.png" alt="CC-BY-SA"/></a><br/>
			<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Open Knowledge"><img src="www/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
			<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="www/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
			<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="www/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
			<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
		</div>
		<div class="main">
		''' % (', '.join(self.getKeywords()), main, self.main.split('.md')[0].replace(' ','-'))
		if self.fig:
			s += '<div class="fig"><a href="http://github.com/grammarware/sleg/blob/master/figures/%s"><img src="http://github.com/grammarware/slef/raw/master/figures/%s" alt="%s" title="%s"/></a><br/>(<a href="http://github.com/grammarware/sleg/blob/master/figures/%s.info.txt">info</a>)</div>' % (self.fig, self.fig, main, main, self.fig)
		if self.defin:
			s += '<div class="def">%s</div>\n' % self.defin.getHtml()
		z = ''
		for k in languages:
			if k in self.items.keys():
				# print('"%s" vs "%s"' % (self.items[k].getTitle() , main))
				if self.items[k].getTitle() == main:
					z += '<li>%s<strong>%s</strong>: %s</li>\n' % (self.getFlag(k), k, self.items[k].getHtml())
				else:
					z += '<li>%s<strong>%s</strong>: %s</li>\n' % (self.getFlag(k), k, self.items[k].getHtmlLinked())
		if z:
			s += '<h2>Translations</h2><ul>%s</ul>' % z
		z = ''
		for p in self.pubs:
			z += '<li>%s</li>\n' % p.getHtml()
		if z:
			s += '<h2>Publications</h2><ul>%s</ul>' % z
		# Last updated: %s.<br/>
		return s+'''</div><div style="clear:both"/><hr />
		<div class="last">
			<em>
				<a href="http://github.com/grammarware/sleg">Software Language Engineering Glossary</a> (SLEG) is
				created and maintained by <a href="http://grammarware.net">Dr. Vadim Zaytsev</a>.
			</em>
		</div></body></html>'''
	def getFlag(self, key):
		f = flags[languages.index(key)]
		if f:
			return '<img src="www/%s.png" alt="%s"/>' % (f, key)
		else:
			return ''
	def __str__(self):
		s = ''
		if self.fig:
			s += '* Figure: %s\n' % self.fig
		if self.defin:
			s += '* Definition: %s\n' % self.defin
		for k in languages:
			if k in self.items.keys():
				s += '* %s: %s\n' % (k, self.items[k])
		for p in self.pubs:
			s += '* Publication: %s\n' % p
		return s

# Publication: [*Generalized multitext grammars*](http://dx.doi.org/10.3115/1218955.1219039)
class Publication:
	def __init__(self, s):
		self.title = s.split('[')[1].split(']')[0]
		if self.title.startswith('*') and self.title.endswith('*'):
			self.title = self.title[1:-1]
		if self.title.startswith('_') and self.title.endswith('_'):
			self.title = self.title[1:-1]
		self.link = s.split('](')[1][:-1]
	def who(self):
		return self.__class__.__name__
	def getHtml(self):
		return '<em><a href="%s">%s</a></em>' % (self.link, self.title)
	def __str__(self):
		return '[*%s*](%s)' % (self.title, self.link)

# English: _algebraic data type_ ([Wikipedia](http://en.wikipedia.org/wiki/Algebraic data type))
class Entry:
	def __init__(self, s):
		self.titles = []
		for t in s.split(' or '):
			self.titles.append(t.split('_')[1])
		self.links = []
		# Lng: _title_ ([W1](http://link)) ([W2](http://link))
		for link in s.split(' ([')[1:]:
			# W1](http://link))
			a,b = link.split('](')
			b = b[:-2]
			self.links.append((a,b))
	def who(self):
		return self.__class__.__name__
	def getTitle(self):
		# ???
		return '/'.join(self.titles)
	def getTitles(self):
		return self.titles
	def getHtml(self):
		return self.getHtmlLinks(' or '.join(['<em>%s</em>' % t for t in self.titles]))
	def getHtmlLinked(self):
		return self.getHtmlLinks(' or '.join(['<em><a href="%s.html">%s</a></em>' % (t,t) for t in self.titles])) # .capitalize()?
	def getHtmlLinks(self, s):
		for link in self.links:
			s += ' (<a href="%s">%s</a>)' % (link[1], link[0])
		return s
	def __str__(self):
		s = ' or '.join(['_%s_' % t for t in self.titles])
		for link in self.links:
			s += ' ([%s](%s))' % link
		return s

class MDText:
	def __init__(self, s):
		self.chunks = []
		while s:
			if s.startswith('**'):
				j = s[2:].find('**')+2
				self.chunks.append(MDBold(s[2:j]))
				s = s[j+2:]
			elif s.startswith('[['):
				j = s.find(']]')
				self.chunks.append(MDLink(s[2:j]))
				s = s[j+2:]
			elif s.startswith('`'):
				j = s[1:].find('`')+1
				self.chunks.append(MDCode(s[1:j]))
				s = s[j+1:]
			else:
				seq = list(filter(lambda x:x!=-1,map(lambda x:s.find(x),code)))
				if len(seq) < 1:
					j = len(s)
				else:
					j = min(seq)
				self.chunks.append(MDBare(s[:j]))
				s = s[j:]
	def getHtml(self):
		# present as HTML
		return ''.join(map(lambda x:x.getHtml(),self.chunks))
	def __str__(self):
		# present as Markdown
		return ''.join(map(str,self.chunks))

# not good with nesting
class MDBold:
	def __init__(self, s):
		self.text = s
	def getHtml(self):
		return '<strong>%s</strong>' % self.text
	def __str__(self):
		return '**%s**' % self.text

# bar not yet implemented
class MDLink:
	def __init__(self, s):
		if s.find('|') < 0:
			self.goal = self.text = s
		else:
			self.text,self.goal = s.split('|')
	def getHtml(self):
		return '<a href="%s.html">%s</a>' % (self.goal, self.text) # .capitalize()?
	def __str__(self):
		if self.goal == self.text:
			return '[[%s]]' % self.text
		else:
			return '[[%s|%s]]' % (self.text,self.goal)

class MDCode:
	def __init__(self, s):
		self.text = s
	def getHtml(self):
		return '<code>%s</code>' % self.text
	def __str__(self):
		return '`%s`' % self.text

class MDBare:
	def __init__(self, s):
		self.text = s
	def getHtml(self):
		return self.text
	def __str__(self):
		return self.text

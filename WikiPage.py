#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3
import os
import sys

languages = ('Abbreviated as', 'English', 'German', 'French', 'Dutch', 'Russian')
flags =     (''              ,  'UK'    , 'DE'    , 'FR'    , 'NL'   , 'RU')
code = ('**','[[')

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
	def getNames(self):
		names = []
		for k in self.items.keys():
			names.extend(self.items[k].getTitles())
		return names
	def getHtml(self, main):
		s = '''<!DOCTYPE html PUBLIC "-//W3C//Dth XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/Dth/xhtml1-strict.dth">
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
			<meta name="keywords" content="software language engineering,glossary,%s"/>
			<title>S(L)EBOK — SLEG — %s</title>
			<link href="sleg.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
		<div class="left">
			<a href="/"><img src="http://grammarware.github.com/logos/sleg.200.png" alt="Software Language Engineering Glossary (SLEG)"/></a><br/>
			[<a href="http://github.com/grammarware/sleg/wiki/%s">Edit!</a>]<br/>
			<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="CC-BY-SA"><img src="cc-by-sa.png" alt="CC-BY-SA" class="pad"/></a><br/>
			<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
			<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="css21.png" alt="CSS 2.1 W3C CanRec" /></a><br/>
			<div class="pad">[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
		</div>
		<div class="main">
		''' % (','.join(self.getNames()), main.capitalize(), self.main)
		if self.fig:
			s += '<div class="fig"><a href="http://github.com/grammarware/sleg/blob/master/figures/%s"><img src="http://github.com/grammarware/slef/raw/master/figures/%s" alt="%s" title="%s"/></a><br/>(<a href="http://github.com/grammarware/sleg/blob/master/figures/%s.info.txt">info</a>)</div>' % (self.fig, self.fig, main, main, self.fig)
		if self.defin:
			s += '<div class="def">%s</div>\n' % self.defin.getHtml()
		z = ''
		for k in languages:
			if k in self.items.keys():
				# print('"%s" vs "%s"' % (str(self.items[k]) , main))
				if self.items[k].title == main:
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
		return s+'''</div><br clear="both"/><hr />
		<div class="last">
			<em>
				<a href="http://github.com/grammarware/sleg">Software Language Engineering Glossary</a> (SLEG) is
				created and maintained by <a href="http://grammarware.net">Dr. Vadim Zaytsev</a>.
			</em>
		</div></body></html>'''
	def getFlag(self, key):
		f = flags[languages.index(key)]
		if f:
			return '<img src="%s.png" alt="%s"/>' % (f, key)
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
		self.title = s.split('_')[1]
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
		return self.title
	def getTitles(self):
		if self.title.find('/') < 0:
			return [self.title]
		else:
			return self.title.split('/')
	def getHtml(self):
		return self.getHtmlLinks('<em>%s</em>' % self.title)
	def getHtmlLinks(self, s):
		for link in self.links:
			s += ' (<a href="%s">%s</a>)' % (link[1], link[0])
		return s
	def getHtmlLinked(self):
		return self.getHtmlLinks('<em><a href="%s.html">%s</a></em>' % (self.title, self.title)) # .capitalize()?
	def __str__(self):
		s = '_%s_' % self.title
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
		self.text = s
	def getHtml(self):
		return '<a href="%s.html">%s</a>' % (self.text, self.text) # .capitalize()?
	def __str__(self):
		return '[[%s]]' % self.text

class MDBare:
	def __init__(self, s):
		self.text = s
	def getHtml(self):
		return self.text
	def __str__(self):
		return self.text

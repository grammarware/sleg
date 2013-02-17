#!/Library/Frameworks/Python.framework/Versions/3.1/bin/python3
import os
import sys

languages = ('English', 'German', 'French', 'Dutch', 'Russian')
flags =     ('EN'     , 'DE'    , 'FR'    , 'NL'   , 'RU'     )
code = ('**','[[','`')

class Bunch:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)

class WikiPage:
	def __init__(self, fname):
		self.main = fname
		self.sections = {}
		# self.pubs = []
		# self.defin = None
		# self.fig = ''
		f = open(fname,'r')
		self.text = f.readlines()
		f.close()
		cur = ''
		for line in self.text:
			if line.startswith('## '):
				cur = line[3:].strip()
				# self.sections[cur] = Bunch(terms=[],fig='',defin='',links=[])
				self.sections[cur] = Bunch(terms=[],pairs={})
				continue
			if not cur or not line.strip():
				# skip lines before the first section
				continue
			if line[2]=='_':
				# dangerous: assumes that all terms are surrounded by underscores!
				# is s[1:-1] better?
				self.sections[cur].terms = [s.split('_')[1] for s in line[2:].split('; ')]
				continue
			wrds = line.split(': ')
			if len(wrds) == 2:
				lhs = wrds[0].split('* ')[1]
				rhs = wrds[1].strip()
				if rhs.startswith('_') and rhs.endswith('_'):
					rhs = rhs[1:-1]
				# if lhs in languages:
				# 	self.items[lhs] = Entry(rhs)
				if lhs == 'Publication':
					e = Publication(rhs)
				elif lhs == 'Definition':
					e = MDText(rhs)
				# elif lhs == 'Figure':
				# 	self.fig = rhs
				else:
					# print('Unknown line:',line)
					e = Entry(rhs)
				if lhs in self.sections[cur].pairs.keys():
					self.sections[cur].pairs[lhs].append(e)
				else:
					self.sections[cur].pairs[lhs] = [e]
			elif line.strip():
				print('Strange line:',line)
	def who(self):
		return self.__class__.__name__
	def validate(self):
		lines = list(filter(lambda x:x,map(lambda x:x.strip(),self.text)))
		for line in lines:
			print(line)
		print('---vs---')
		print(str(self))
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
		return sorted(self.sections.keys())
	def getNames(self,lang):
		if 'Short' in self.sections[lang].pairs.keys(): # and not str(self.sections[lang].pairs['Short']).startswith('`'):
			return self.sections[lang].terms + list(filter(lambda x:str(x).isalnum(),self.sections[lang].pairs['Short']))
		else:
			return self.sections[lang].terms
	def getKeywords(self):
		kws = []
		for lang in self.sections.keys():
			kws.append(lang)
			# print(self.items[lang].getTitles())
			kws.extend(self.sections[lang].terms)
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
		''' % ('; '.join(self.getKeywords()), main, self.main.split('.md')[0].replace(' ','-'))
		for lang in languages:
			if lang not in self.sections.keys():
				continue
			# main loop
			# TODO: do not hyperlink self-references
			s += '<h2>%s</h2>\n<ul><li>' % Flagged(lang)
			# s += '<ul><li>%s</li>\n' % '; '.join(['<strong>%s</strong>' % s for s in self.sections[lang].terms])
			ts = []
			for t in self.sections[lang].terms:
				if t == main:
					ts.append('<strong>%s</strong>' % t)
				else:
					ts.append('<a href="%s.html"><strong>%s</strong></a>' % (t,t))
			s += '; '.join(ts)
			if 'Short' in self.sections[lang].pairs.keys():
				z = []
				for short in self.sections[lang].pairs['Short']:
					if short == main or not short.text.isalnum():
						z.append('%s' % short.getHtml())
					else:
						z.append('<a href="%s.html">%s</a>' % (short,short.getHtml()))
				s += ' (%s)' % '; '.join(z)
			s += '</li>\n'
			for k in self.sections[lang].pairs.keys():
				for rhs in self.sections[lang].pairs[k]:
					if k == 'Short':
						continue
					elif k == 'Figure':
						s += '<div class="fig"><a href="http://github.com/grammarware/sleg/blob/master/figures/%s"><img src="http://github.com/grammarware/sleg/raw/master/figures/%s" alt="%s" title="%s"/></a><br/>(<a href="http://github.com/grammarware/sleg/blob/master/figures/%s.info.txt">info</a>)</div>' % (rhs, rhs, main, main, rhs)
					elif k == 'Definition':
						s += '<li class="def">%s</li>\n' % rhs.getHtml()
					else:
						s += '<li>%s: %s</li>' % (k,rhs.getHtml())
			s += '</ul>'
		# z = ''
		# for k in languages:
		# 	if k in self.items.keys():
		# 		# print('"%s" vs "%s"' % (self.items[k].getTitle() , main))
		# 		if self.items[k].getTitle() == main:
		# 			z += '<li>%s<strong>%s</strong>: %s</li>\n' % (self.getFlag(k), k, self.items[k].getHtml())
		# 		else:
		# 			z += '<li>%s<strong>%s</strong>: %s</li>\n' % (self.getFlag(k), k, self.items[k].getHtmlLinked())
		# if z:
		# 	s += '<h2>Translations</h2><ul>%s</ul>' % z
		# z = ''
		# for p in self.pubs:
		# 	z += '<li>%s</li>\n' % p.getHtml()
		# if z:
		# 	s += '<h2>Publications</h2><ul>%s</ul>' % z
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
		for lang in languages:
			if lang not in self.sections.keys():
				continue
			s += '\n## %s\n* %s\n' % (lang,'; '.join(['_%s_' % s for s in self.sections[lang].terms]))
			for k in self.sections[lang].pairs:
				s += '* %s: %s\n' % (k, self.sections[lang].pairs[k])
		return s.strip()+'\n'
		if self.fig:
			s += '* Figure: %s\n' % self.fig
		if self.defin:
			s += '* Definition: %s\n' % self.defin
		for k in languages:
			if k in self.items.keys():
				s += '* %s: %s\n' % (k, self.items[k])
		for p in self.pubs:
			s += '* Publication: %s\n' % p
		return s.strip()

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

# English: Wikipedia: http://en.wikipedia.org/wiki/Algebraic_data_type
class Entry:
	def __init__(self, s):
		self.text = s
	def who(self):
		return self.__class__.__name__
	def getHtml(self):
		if self.text.startswith('http://'):
			return '<a class="src" href="%s">%s</a>' % (self.text,self.text)
		elif self.text.startswith('`'):
			return '<code>%s</code>' % self.text.split('`')[1]
		else:
			return '%s' % self.text
	def __str__(self):
		return self.text

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

class Flagged:
	def __init__(self, lang):
		self.lang = lang
		self.flag = flags[languages.index(self.lang)]
	def __str__(self):
		return '<img src="www/%s.png" alt="%s"/> %s' % (self.flag, self.lang, self.lang)

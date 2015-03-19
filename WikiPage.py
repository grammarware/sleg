#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from Formatting import TEMPLATES

languages = ('English', 'German', 'French', 'Dutch', 'Russian')
flags     = ('EN'     , 'DE'    , 'FR'    , 'NL'   , 'RU'     )
code = ('**', '[[', '`')

class Bunch:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)

class WikiPage:
	def __init__(self, fname):
		self.main = fname
		self.order = []
		self.sections = {}
		self.orders = {}
		f = open(fname, 'r', encoding="utf-8")
		self.text = f.readlines()
		f.close()
		cur = ''
		for line in self.text:
			if line.startswith('## '):
				cur = line[3:].strip()
				self.orders[cur] = []
				continue
			if not cur or not line.strip():
				# skip lines before the first section
				continue
			# TODO: shitty condition!
			if line[2] == '_':
				for s in line[2:].split('; '):
					z = s.strip()
					if z.startswith('_') and z.endswith('_'):
						z = z[1:-1]
					self.addValue(cur, 'Terms', z)
				continue
			wrds = line.split(': ')
			if len(wrds) > 1:
				lhs = wrds[0].split('* ')[1]
				rhs = ': '.join(wrds[1:]).strip()
				# TODO: decide whether this is a temporary fix or a robustness invariant
				if rhs.startswith('_') and rhs.endswith('_'):
					rhs = rhs[1:-1]
				if lhs == 'Publication':
					e = Publication(rhs)
				elif lhs == 'Definition':
					e = MDText(rhs)
				else:
					e = Entry(rhs)
				self.addValue(cur, lhs, e)
			elif line.strip():
				print('Strange line:', line)
	def getValues(self, key1, key2):
		if key1 not in self.sections.keys() or key2 not in self.sections[key1].keys():
			return []
		return self.sections[key1][key2]
	def getKeys(self, key):
		if key not in self.sections.keys():
			return []
		return self.orders[key]
	def addValue(self, key1, key2, v):
		if key1 not in self.sections.keys():
			self.sections[key1] = {}
			self.order.append(key1)
		if key2 not in self.sections[key1].keys():
			self.sections[key1][key2] = [v]
			self.orders[key1].append(key2)
		else:
			self.sections[key1][key2].append(v)
	def who(self):
		return self.__class__.__name__
	def validate(self):
		lines = [x.strip() for x in self.text if x.strip()]
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
	def getNames(self, lang):
		return self.getValues(lang, 'Terms') + self.getValues(lang, 'Short')
	def getKeywords(self):
		kws = []
		for lang in sorted(self.orders.keys()):
			kws.append(lang)
			kws.extend(self.getValues(lang, 'Terms'))
		return kws
	def getHtml(self, main):
		s = TEMPLATES['pagehead'].format('; '.join(self.getKeywords()), main, self.main.split('.md')[0].replace(' ', '-'))
		for lang in languages:
			if lang not in self.sections.keys():
				continue
			# main loop
			# TODO: do not hyperlink self-references
			s += '<h2>{0}</h2>\n<ul><li>'.format(Flagged(lang))
			# s += '<ul><li>%s</li>\n' % '; '.join(['<strong>%s</strong>' % s for s in self.sections[lang].terms])
			ts = []
			# for t in self.sections[lang].terms:
			for t in self.getValues(lang, 'Terms'):
				if t == main:
					ts.append('<strong>%s</strong>' % t)
				else:
					ts.append('<a href="%s.html"><strong>%s</strong></a>' % (t, t))
			s += '; '.join(ts)
			if 'Short' in self.getKeys(lang):
				z = []
				for short in self.getValues(lang, 'Short'):
					if short == main or not short.text.isalnum():
						z.append(short.getHtml())
					else:
						z.append('<a href="%s.html">%s</a>' % (short, short.getHtml()))
				s += ' (%s)' % '; '.join(z)
			s += '</li>\n'
			for k in self.getKeys(lang):
				for rhs in self.getValues(lang, k):
					if k in ('Short', 'Terms'):
						continue
					elif k == 'Figure':
						s += TEMPLATES['figure'].format(rhs, main)
					elif k == 'Definition':
						s += '<li class="def">{}</li>\n'.format(rhs.getHtml())
					else:
						s += '<li>{0}: {1}</li>'.format(k, rhs.getHtml())
			s += '</ul>'
		# Last updated: %s.<br/>
		return s+TEMPLATES['footer']
	def __str__(self):
		s = ''
		for lang in self.order:
			s += '\n## %s\n* %s\n' % (lang, '; '.join(['_%s_' % s for s in self.getValues(lang, 'Terms')]))
			for k in self.getKeys(lang):
				if k == 'Terms':
					continue
				for v in self.getValues(lang, k):
					s += '* %s: %s\n' % (k, v)
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
			return '<a class="src" href="%s">%s</a>' % (self.text, self.text)
		elif self.text.startswith('`'):
			return '<code>%s</code>' % self.text.split('`')[1]
		else:
			return '%s' % self.text
	def __str__(self):
		return self.text
	def __lt__(self, other):
		return str(self) < str(other)
	def __gt__(self, other):
		return str(self) > str(other)

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
				seq = [x for x in [s.find(x) for x in code] if x != -1]
				if len(seq) < 1:
					j = len(s)
				else:
					j = min(seq)
				self.chunks.append(MDBare(s[:j]))
				s = s[j:]
	def getHtml(self):
		# present as HTML
		return ''.join([x.getHtml() for x in self.chunks])
	def __str__(self):
		# present as Markdown
		return ''.join(map(str, self.chunks))

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
			self.text, self.goal = s.split('|')
	def getHtml(self):
		return '<a href="%s.html">%s</a>' % (self.goal, self.text) # .capitalize()?
	def __str__(self):
		if self.goal == self.text:
			return '[[%s]]' % self.text
		else:
			return '[[%s|%s]]' % (self.text, self.goal)

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
		return '<img src="../www/%s.png" alt="%s"/> %s' % (self.flag, self.lang, self.lang)

#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

TEMPLATES = {
	'figure':
		'<div class="fig">'+
		'<a href="http://github.com/slebok/sleg/blob/master/figures/{0}">'+
		'<img src="http://github.com/slebok/sleg/raw/master/figures/{0}" alt="{1}" title="{1}"/>'+
		'</a><br/>(<a href="http://github.com/slebok/sleg/blob/master/figures/{0}.info.txt">info</a>)</div>',
	'header':
		'''<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
			<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary%s"/>
			<title>SLEBOK — SLEG%s</title>
			<link href="../www/sleg.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
		<div class="left">
			<a href="index.html"><img src="../www/sleg.200.png" alt="Software Language Engineering Glossary (SLEG)" class="pad"/></a><br/>
			%s<a href="http://creativecommons.org/licenses/by-sa/4.0/" title="CC-BY-SA"><img src="../www/cc-by-sa.png" alt="CC-BY-SA"/></a><br/>
			<a href="http://creativecommons.org/licenses/by-sa/4.0/" title="Open Knowledge"><img src="../www/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
			<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="../www/xhtml.88.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
			<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="../www/css.88.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
			<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
		</div>
		<div class="main">\n\t\t''',
	'footer':
		'''</div><div style="clear:both"/><hr />
		<div class="last">
			<em>
				<a href="http://github.com/slebok/sleg">Software Language Engineering Glossary</a> (SLEG) is
				created and maintained by <a href="http://grammarware.net">Dr. Vadim Zaytsev</a>.<br/>
				Hosted as a part of <a href="http://slebok.github.io/">SLEBOK</a> on <a href="http://www.github.com/">GitHub</a>.
			</em>
		</div></body></html>'''
}

TEMPLATES['indexhead'] = (TEMPLATES['header'] % ('','','')).replace('\t\t','').strip()
TEMPLATES['pagehead'] = TEMPLATES['header'] % (', {}',' — {}','<div class="pad">[<a href="http://github.com/slebok/sleg/{}/_edit">Edit!</a>]</div><br/>\n\t\t\t')

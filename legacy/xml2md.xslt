<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:dict="http://grammarware.net/dict" version="1.0">
	<xsl:output method="text" encoding="UTF-8"/>
	<xsl:param name="date"/>
	<xsl:param name="setup"/>
	<xsl:variable name="cols" select="document($setup)/setup/*"/>
	<xsl:template match="/dict:glossary">
		<xsl:for-each select="term">
			<xsl:text>File: </xsl:text>
			<xsl:value-of select="en/w"/>
			<xsl:for-each select="*">
				<xsl:text>
* </xsl:text>
				<xsl:choose>
					<xsl:when test="local-name()='ab'">Abbreviated as</xsl:when>
					<xsl:when test="local-name()='en'">English</xsl:when>
					<xsl:when test="local-name()='ru'">Russian</xsl:when>
					<xsl:when test="local-name()='nl'">Dutch</xsl:when>
					<xsl:when test="local-name()='de'">German</xsl:when>
					<xsl:otherwise>???</xsl:otherwise>
				</xsl:choose>
				<xsl:text>: _</xsl:text>
				<xsl:value-of select="w"/>
				<xsl:text>_</xsl:text>
				<xsl:for-each select="*">
					<!-- ([Wikipedia](http://ru.wikipedia.org/wiki/%D0%9A%D0%BE%D0%BD%D1%82%D0%B5%D0%BA%D1%81%D1%82%D0%BD%D0%BE-%D1%81%D0%B2%D0%BE%D0%B1%D0%BE%D0%B4%D0%BD%D0%B0%D1%8F_%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0)) -->
					<xsl:choose>
						<xsl:when test="local-name()='wiki'">
							<xsl:text> ([Wikipedia](http://</xsl:text>
							<xsl:value-of select="local-name(..)"/>
							<xsl:text>.wikipedia.org/wiki/</xsl:text>
							<xsl:choose>
								<xsl:when test="./text()!=''">
									<xsl:value-of select="translate(./text(),' ','_')"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="../w/text()"/>
								</xsl:otherwise>
							</xsl:choose>
							<xsl:text>)</xsl:text>
						</xsl:when>
						<xsl:when test="local-name()='wbooks'">
							<xsl:text> ([WikiBooks](http://</xsl:text>
							<xsl:value-of select="local-name(..)"/>
							<xsl:text>.wikibooks.org/wiki/</xsl:text>
							<xsl:choose>
								<xsl:when test="./text()!=''">
									<xsl:value-of select="./text()"/>
								</xsl:when>
								<xsl:otherwise>
									<xsl:value-of select="../w/text()"/>
								</xsl:otherwise>
							</xsl:choose>
							<xsl:text>)</xsl:text>
						</xsl:when>
						<xsl:when test="local-name()='src'">
							<xsl:text> ([Source](</xsl:text>
							<xsl:value-of select="./text()"/>
							<xsl:text>)</xsl:text>
						</xsl:when>
						<xsl:when test="local-name()='w'"/>
						<xsl:otherwise>???</xsl:otherwise>
					</xsl:choose>
				</xsl:for-each>
			</xsl:for-each>
			<xsl:text>

</xsl:text>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>

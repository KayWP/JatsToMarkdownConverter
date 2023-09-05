<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  exclude-result-prefixes="xlink">

  <xsl:output method="text" encoding="UTF-8"/>

  <!-- Transform the root element (usually "article") -->
  <xsl:template match="article">
    <!-- Process the <front> and <body> tags -->
    <xsl:apply-templates select="front"/>
    <xsl:apply-templates select="body"/>
  </xsl:template>

  <!-- Transform the <front> tag -->
  <xsl:template match="front">
    <!-- Process elements inside <front> -->
    <xsl:apply-templates select="journal-meta"/>
    <xsl:apply-templates select="article-meta"/>
  </xsl:template>

  <!-- Transform the <journal-meta> tag -->
  <xsl:template match="journal-meta">
    <!-- Extract and transform journal information -->
    <xsl:text># Journal</xsl:text>
    <xsl:text>
</xsl:text>
    <xsl:text>**Title:** </xsl:text>
    <xsl:value-of select="journal-title-group/journal-title"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**ISSN (epub):** </xsl:text>
    <xsl:value-of select="issn[@pub-type='epub']"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**ISSN (ppub):** </xsl:text>
    <xsl:value-of select="issn[@pub-type='ppub']"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Publisher:** </xsl:text>
    <xsl:value-of select="publisher/publisher-name"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Publisher Location:** </xsl:text>
    <xsl:value-of select="publisher/publisher-loc"/>
    <xsl:text>
</xsl:text>
    <xsl:text>
</xsl:text>
  </xsl:template>

  <!-- Transform the <article-meta> tag -->
  <xsl:template match="article-meta">
    <!-- Extract and transform article information -->
    <xsl:text># Article</xsl:text>
    <xsl:text>
</xsl:text>
    <xsl:text>**Article ID (Publisher):** </xsl:text>
    <xsl:value-of select="article-id[@pub-id-type='publisher-id']"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**DOI:** </xsl:text>
    <xsl:value-of select="article-id[@pub-id-type='doi']"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Category:** </xsl:text>
    <xsl:value-of select="article-categories/subj-group/subject"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Title:** </xsl:text>
    <xsl:value-of select="title-group/article-title"/>
    <xsl:text>
</xsl:text>
    <xsl:if test="subtitle">
      <xsl:text>**Subtitle:** </xsl:text>
      <xsl:value-of select="subtitle"/>
      <xsl:text>
</xsl:text>
    </xsl:if>
    <xsl:text>**Authors:** </xsl:text>
    <xsl:for-each select="contrib-group/contrib[@contrib-type='author']">
      <xsl:value-of select="normalize-space(name/surname)"/>
      <xsl:text>, </xsl:text>
      <xsl:value-of select="normalize-space(name/given-names)"/>
      <xsl:if test="position() != last()">
        <xsl:text>; </xsl:text>
      </xsl:if>
    </xsl:for-each>
    <xsl:text>
</xsl:text>
    <xsl:text>**Publication Date (epub):** </xsl:text>
    <xsl:value-of select="pub-date[@pub-type='epub']/year"/>
    <xsl:text>-</xsl:text>
    <xsl:value-of select="pub-date[@pub-type='epub']/month"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Volume:** </xsl:text>
    <xsl:value-of select="volume"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Issue:** </xsl:text>
    <xsl:value-of select="issue"/>
    <xsl:text>
</xsl:text>
    <xsl:text>**Pages:** </xsl:text>
    <xsl:value-of select="fpage"/>
    <xsl:text>-</xsl:text>
    <xsl:value-of select="lpage"/>
    <xsl:text>
</xsl:text>
  </xsl:template>

  <!-- Transform the <body> tag -->
  <xsl:template match="body">
    <xsl:apply-templates/>
  </xsl:template>

  <!-- Transform <title> elements into Markdown headers -->
  <xsl:template match="title">
    <xsl:text>### </xsl:text>
    <xsl:apply-templates/>
    <xsl:text>
</xsl:text>
  </xsl:template>

  <!-- Transform paragraphs with four spaces after each paragraph -->
  <xsl:template match="p">
    <xsl:text>
</xsl:text>
    <xsl:apply-templates/>
    <xsl:text>
</xsl:text>
    <xsl:text>    </xsl:text> <!-- Add four spaces after each paragraph -->
  </xsl:template>

<xsl:template match="*[local-name()='ext-link']">
  <xsl:text>[</xsl:text>
  <xsl:apply-templates/>
  <xsl:text>](&lt;</xsl:text>
  <xsl:value-of select="@xlink:href"/>
  <xsl:text>&gt;)</xsl:text>
</xsl:template>

  <!-- Transform figures -->
  <xsl:template match="fig">
    <xsl:text>
![Image](</xsl:text>
    <xsl:value-of select="graphic/@xlink:href"/>
    <xsl:text>)
</xsl:text>
    <!-- No handling for figure caption -->
    <xsl:text>
</xsl:text>
  </xsl:template>

  <!-- Transform tables -->
  <xsl:template match="table-wrap">
    <xsl:text>
</xsl:text>
    <xsl:text>[tbl: </xsl:text>
    <xsl:value-of select="@id"/>
    <xsl:text>]</xsl:text>
    <xsl:text>
</xsl:text>
  </xsl:template>

  <!-- Transform the <sc> tag (capitalize its contents) -->
  <xsl:template match="sc">
    <xsl:value-of select="translate(., 'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')"/>
  </xsl:template>

  <!-- Transform <italic> tags -->
  <xsl:template match="italic">
    <xsl:text>_</xsl:text>
    <xsl:apply-templates/>
    <xsl:text>_</xsl:text>
  </xsl:template>

  <!-- Transform <bold> tags -->
  <xsl:template match="bold">
    <xsl:text>**</xsl:text>
    <xsl:apply-templates/>
    <xsl:text>**</xsl:text>
  </xsl:template>

  <!-- Transform footnote references -->
  <xsl:template match="sup[xref[@ref-type='fn']]">
    <xsl:text>[fn:</xsl:text>
    <xsl:value-of select="xref/@rid"/>
    <xsl:text>]</xsl:text>
  </xsl:template>

  <!-- New Rule: Transform <ext-link> tags into Markdown URLs -->
  <xsl:template match="ext-link">
    <xsl:text>[</xsl:text>
    <xsl:apply-templates/>
    <xsl:text>](&#x27;</xsl:text>
    <xsl:value-of select="@xlink:href"/>
    <xsl:text>&#x27;)</xsl:text>
  </xsl:template>

  <!-- Transform any other elements (not explicitly matched) -->
  <xsl:template match="*">
    <xsl:apply-templates/>
  </xsl:template>

</xsl:stylesheet>
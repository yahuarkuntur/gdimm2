<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="formula"/>
<xsl:param name="condicion"/>

<xsl:template match="/">
    <root>
    <xsl:choose>

    <xsl:when test="$condicion">
        <value><xsl:value-of select="$formula"/></value>
    </xsl:when>

    <xsl:otherwise>
        <value></value>
    </xsl:otherwise>

    </xsl:choose>

    </root>
    
</xsl:template>

</xsl:stylesheet> 

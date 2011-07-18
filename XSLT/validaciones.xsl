<xsl:stylesheet version="2.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="formula"/>
<xsl:param name="condicion"/>

<xsl:template match="/">
    <root>

    <value>
    <xsl:if test="$condicion">
        <xsl:if test="not($formula)">
            ERR
        </xsl:if>
    </xsl:if>
    </value>

    </root>
    
</xsl:template>

</xsl:stylesheet> 

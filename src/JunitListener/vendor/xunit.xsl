<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:output method="xml" omit-xml-declaration="no" indent="yes"/>

    <xsl:template match="testsuites/@disabled" />
    <xsl:template match="testsuites/@errors" />
    <xsl:template match="testsuites/@failures" />
    <xsl:template match="testsuites/@tests" />
    <xsl:template match="testsuites/@time" />
    <xsl:template match="testsuite/@file" />
    <xsl:template match="testsuite/@disabled" />
    <xsl:template match="properties" />
    <xsl:template match="skipped"/>
    <xsl:template match="testsuite/system-out" />
    <xsl:template match="testsuite/system-err" />
    <xsl:template match="testcase/system-out" />
    <xsl:template match="testcase/system-err" />
    <xsl:template match="testsuite/@id">
      <xsl:attribute name="{name(.)}">
          <xsl:value-of select="translate(., 'st-','')" />
      </xsl:attribute>
    </xsl:template>
    <xsl:template match="testsuite/@timestamp">
        <xsl:attribute name="{name(.)}">
            <xsl:value-of select="substring(., 1, 19)" />
        </xsl:attribute>
    </xsl:template>      

    <!--identity template copies everything forward by default-->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>

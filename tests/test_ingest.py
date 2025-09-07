import unittest
import os
from datetime import datetime
from src.ingest import ingest_newsletters_from_feed, strip_html_tags, clean_title
from src.newsletter import Newsletter


class TestIngestNewsletters(unittest.TestCase):
    def setUp(self):
        self.test_rss = "test_feed.xml"
        with open(self.test_rss, "w") as f:
            f.write(
                """<?xml version="1.0" encoding="UTF-8"?>
<rss><channel>
<item>
<title><![CDATA[<a href="/cro/cro-veeda-picks-mangos-generative-ai-platform-clinical-trials" hreflang="en">CRO Veeda picks Mango’s generative AI platform for clinical trials</a>]]></title>
<description>Content 1</description>
<pubDate>Fri, 22 Aug 2025 10:00:00 +0000</pubDate>
</item>
<item>
<title>Newsletter 2</title>
<description>Content 2</description>
<pubDate>Sat, 23 Aug 2025 11:00:00 +0000</pubDate>
</item>
</channel></rss>
"""
            )

    def tearDown(self):
        os.remove(self.test_rss)

    def test_ingest_newsletters_from_feed(self):
        newsletters = ingest_newsletters_from_feed(self.test_rss)
        self.assertEqual(len(newsletters), 2)
        self.assertEqual(
            newsletters[0].title,
            "CRO Veeda picks Mango’s generative AI platform for clinical trials",
        )
        self.assertEqual(newsletters[0].content, "Content 1")
        self.assertEqual(newsletters[1].title, "Newsletter 2")
        self.assertEqual(newsletters[1].content, "Content 2")
        self.assertIsInstance(newsletters[0].publication_date, datetime)

    def test_strip_html_tags(self):
        html_title = '<a href="/cro/cro-veeda-picks-mangos-generative-ai-platform-clinical-trials" hreflang="en">CRO Veeda picks Mango’s generative AI platform for clinical trials</a>'
        clean_title_result = strip_html_tags(html_title)
        self.assertEqual(
            clean_title_result,
            "CRO Veeda picks Mango’s generative AI platform for clinical trials",
        )
        # Additional cases
        self.assertEqual(strip_html_tags("<b>Bold</b> text"), "Bold text")
        self.assertEqual(strip_html_tags("No tags here"), "No tags here")
        self.assertEqual(strip_html_tags("<div>foo</div><span>bar</span>"), "foobar")
        self.assertEqual(strip_html_tags("<a href='x'>link</a>"), "link")
        self.assertEqual(strip_html_tags(""), "")

    def test_clean_title(self):
        self.assertEqual(clean_title("STAT+: <b>AI News</b>"), "AI News")
        self.assertEqual(clean_title("STAT+:Hello"), "Hello")
        self.assertEqual(clean_title("<i>STAT+:Test</i>"), "Test")
        self.assertEqual(clean_title("NoPrefix Title"), "NoPrefix Title")
        self.assertEqual(clean_title(""), "")


if __name__ == "__main__":
    unittest.main()

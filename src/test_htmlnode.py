import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    
    def test_1(self):
        node = HTMLNode("<p>", "This is a test node", props={"href": "test link"})
        props_string = node.props_to_html()
        self.assertEqual(props_string, "href=\"test link\"")
    
    def test2(self):
        node = HTMLNode("<h1>", "This is a test heading", children=None, props={"href": "Test Link", "target": "_blank"})
        props_string = node.props_to_html()
        self.assertEqual(props_string, 'href="Test Link" target="_blank"')
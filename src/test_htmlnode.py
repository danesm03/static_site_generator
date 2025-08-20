from textnode import TextNode, TextType
from htmlnode import HTMLNode
import unittest

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "h1", "hello world", 
                        [HTMLNode("p", "hello again", None, {"href": "https://www.google.com", "target": "_blank",})],
                          {"href": "https://boot.dev", "target": "Boot Dev",}
                          )
        self.assertEqual(node.__repr__(), 
                         'HTMLNode("h1", "hello world", "HTMLNode("p", "hello again", None,  href="https://www.google.com" target="_blank")",  href="https://boot.dev" target="Boot Dev")')
        
    def test_propstohtml(self):
        node = HTMLNode(
            "h1", "hello world", 
                        [HTMLNode("p", "hello again", None, {"href": "https://www.google.com", "target": "_blank",})],
                          {"href": "https://boot.dev", "target": "Boot Dev",}
                          )
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="Boot Dev"')

    def test_props2(self):
        node = HTMLNode(
            "h1", "hello world", 
                        [HTMLNode("p", "hello again", None, {"href": "https://www.google.com", "target": "_blank",})],
                          {"href": "https://boot.dev", "target": "Boot Dev", "charset": "utf-8"}
                          )  
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="Boot Dev" charset="utf-8"')
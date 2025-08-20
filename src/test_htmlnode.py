from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
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



class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_ahref(self):
        node = LeafNode("a", "Boot.Dev Dashboard", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Boot.Dev Dashboard</a>')


    def test_leaf_to_html_noval(self):
        node = LeafNode("a", None, {"href": "https://boot.dev"})
        self.assertRaises(ValueError, node.to_html)



class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')

    def test_parent_to_html_with_ahref(self):
        node = ParentNode(
            "h1",
            [
                LeafNode("a", "Boot.Dev Dashboard", {"href": "https://boot.dev"}),
                LeafNode("b", "This is some bold text"),
            ]
        )

        self.assertEqual(node.to_html(), '<h1><a href="https://boot.dev">Boot.Dev Dashboard</a><b>This is some bold text</b></h1>')

    def test_parent_to_html_with_prop(self):
        node = ParentNode(
            "a",
            [
                LeafNode("a", "Boot.Dev Dashboard", {"href": "https://boot.dev"}),
                LeafNode("b", "This is some bold text"),
            ],
            {"href": "https://www.google.com"}
        )
        self.assertEqual(node.to_html(), '<a href="https://www.google.com"><a href="https://boot.dev">Boot.Dev Dashboard</a><b>This is some bold text</b></a>')


class TestTEXTNodetoHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertEqual(html_node.value, "This is a link node")

    def test_img(self):
        node = TextNode("This is an image node", TextType.IMAGE, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"src": "https://www.google.com", "alt": "This is an image node"})
        self.assertEqual(html_node.value, "")
import unittest

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_links ,split_nodes_image 


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq(self):
        node = TextNode("This is a text node", TextType.BOLD, url="https://bood.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_difftexttype(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

class TestSplitDelimiter(unittest.TestCase):
    def test_code_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT),])

    def test_bold_split(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_italic_split(self):
        node = TextNode("This is text with a _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ])

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ]
        )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def text_extract_multiple_img(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![one](https://www.google.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("one, https://www.google.com")], matches)    

    def text_extract_md_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
            )
        self.assertEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
            TextType.TEXT,
        )
        self.assertEqual(split_nodes_links([node]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev" ),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
        ])

    def test_split_links_listed(self):
        nodes = [
            TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", 
            TextType.TEXT,
            ),
            TextNode(
                "This is text with a link [to google](https://www.google.com) and [to my GithHub](https://github.com/danesm03/static_site_generator)", 
                TextType.TEXT     
            ),
            TextNode(
                "This is a **bold** text that should stay the same",
                TextType.BOLD,
            ),
            TextNode(
                "", TextType.TEXT
            )
        ] 

        self.assertEqual(split_nodes_links(nodes), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, url="https://www.boot.dev" ),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to google", TextType.LINK, "https://www.google.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to my GithHub", TextType.LINK, "https://github.com/danesm03/static_site_generator"),
            TextNode("This is a **bold** text that should stay the same", TextType.BOLD),
        ])


if __name__ == "__main__":
    unittest.main()
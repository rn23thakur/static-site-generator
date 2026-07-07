import unittest
from textnode import TextNode, TextType
from splitnode import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes

class TestSplitNode(unittest.TestCase):
    
    def test_basic(self):
        """Test a standard string with a single pair of delimiters in the middle."""
        node = TextNode("This is a text with `code block` word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is a text with ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_multiple_delimiters(self):
        """Test a string containing multiple separate pairs of the same delimiter."""
        node = TextNode("This has `code1` and also `code2` here", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.PLAIN),
            TextNode("code1", TextType.CODE),
            TextNode(" and also ", TextType.PLAIN),
            TextNode("code2", TextType.CODE),
            TextNode(" here", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_start(self):
        """Test when the string starts immediately with a delimited section."""
        node = TextNode("**Bold** at the very beginning", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" at the very beginning", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_delimiter_at_end(self):
        """Test when the string ends exactly with a delimited section."""
        node = TextNode("This sentence ends in *italic*", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This sentence ends in ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)

    def test_ignore_non_plain_nodes(self):
        """Test that the function skips processing nodes that aren't TextType.PLAIN."""
        node1 = TextNode("Leave `me` alone", TextType.CODE)
        node2 = TextNode("Process `this` please", TextType.PLAIN)
        
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        expected = [
            TextNode("Leave `me` alone", TextType.CODE), # Unchanged
            TextNode("Process ", TextType.PLAIN),
            TextNode("this", TextType.CODE),
            TextNode(" please", TextType.PLAIN),
        ]
        self.assertEqual(new_nodes, expected)

    def test_missing_closing_delimiter(self):
        """Test that our guard clause correctly raises a ValueError for unclosed markdown."""
        node = TextNode("This is text with an unclosed `code block element", TextType.PLAIN)
        
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("closing delimiter", str(cm.exception))

    ## --- IMAGE SPLITTING TESTS ---

    def test_split_images(self):
        """Test processing multiple images in a single node text."""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start_and_end(self):
        """Test images that directly begin and end a string with no surrounding whitespace."""
        node = TextNode("![start](https://link1.com)mid text![end](https://link2.com)", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "https://link1.com"),
                TextNode("mid text", TextType.PLAIN),
                TextNode("end", TextType.IMAGE, "https://link2.com"),
            ],
            new_nodes
        )

    def test_split_image_no_images(self):
        """Test that a node with no images remains completely untouched."""
        node = TextNode("Just plain text with no markdown images here.", TextType.PLAIN)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([node], new_nodes)

    ## --- LINK SPLITTING TESTS ---

    def test_split_links(self):
        """Test processing multiple links in a single node text."""
        node = TextNode(
            "Click [here](https://boot.dev) to learn or search on [Google](https://google.com).",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Click ", TextType.PLAIN),
                TextNode("here", TextType.LINK, "https://boot.dev"),
                TextNode(" to learn or search on ", TextType.PLAIN),
                TextNode("Google", TextType.LINK, "https://google.com"),
                TextNode(".", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_split_link_at_start(self):
        """Test when a link sits right at index 0."""
        node = TextNode("[Boot.dev](https://boot.dev) is great.", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Boot.dev", TextType.LINK, "https://boot.dev"),
                TextNode(" is great.", TextType.PLAIN),
            ],
            new_nodes
        )

    def test_split_link_no_links(self):
        """Test that a node with no links returns seamlessly."""
        node = TextNode("Just plain text with no anchor elements.", TextType.PLAIN)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes_full(self):
        """Test the master conversion function handles all inline Markdown elements concurrently."""
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        new_nodes = text_to_textnodes(text)
        
        expected = [
            TextNode("This is ", TextType.PLAIN),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.PLAIN),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, new_nodes)

    def test_text_to_textnodes_plain_only(self):
        """Test the pipeline when there is absolutely no markdown syntax present."""
        text = "Just a completely normal sentence with zero markdown elements."
        new_nodes = text_to_textnodes(text)
        expected = [TextNode("Just a completely normal sentence with zero markdown elements.", TextType.PLAIN)]
        self.assertListEqual(expected, new_nodes)

    def test_text_to_textnodes_adjacent_elements(self):
        """Test when multiple markdown tokens sit back-to-back with no spaces separating them."""
        text = "**Bold**_Italic_`code`[link](https://url.com)"
        new_nodes = text_to_textnodes(text)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode("Italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("link", TextType.LINK, "https://url.com"),
        ]
        self.assertListEqual(expected, new_nodes)

if __name__ == "__main__":
    unittest.main()
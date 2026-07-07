import unittest
from links_and_images import extract_markdown_images, extract_markdown_links

class TestTextNode(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/39go92W.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("second image", "https://i.imgur.com/39go92W.png")
            ], 
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link to boot.dev](https://www.boot.dev) and [Google](https://www.google.com)"
        )
        self.assertListEqual(
            [
                ("link to boot.dev", "https://www.boot.dev"),
                ("Google", "https://www.google.com")
            ], 
            matches
        )

    def test_extract_mixed_markdown(self):
        text = "Here is an ![image](https://i.imgur.com/zjjcJKZ.png) and here is a [link](https://boot.dev)."
        
        # Ensure image extractor ONLY finds the image
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], image_matches)
        
        # Ensure link extractor ONLY finds the link (and ignores the image due to the lookbehind assertion)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://boot.dev")], link_matches)

if __name__ == "__main__":
    unittest.main()
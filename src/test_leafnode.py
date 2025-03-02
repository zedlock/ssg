import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html_simple(self):
        node = LeafNode("Hello, world!", "p")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    def test_to_html_adv(self):
        node = LeafNode(
            "Hello, world!",
            "div",
            {
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "test-class",
                "style": "height: 100%"
            },
        )
        self.assertEqual(
            node.to_html(),
            (
                "<div "
                "href=\"https://www.google.com\" "
                "target=\"_blank\" "
                "class=\"test-class\" "
                "style=\"height: 100%\""
                ">Hello, world!</div>"
            )
        )

if __name__ == "__main__":
    unittest.main()

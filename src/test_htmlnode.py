import unittest

from htmlnode import HTMLNode


class TestHtmlNode(unittest.TestCase):
    def test_repr_simp(self):
        node = HTMLNode(
            'div',
            'test',
            [],
            None
        )
        expect = "tag: div\nvalue: test\nchildren: 0\nprops: None"
        self.assertEqual(expect, repr(node))
    def test_repr_adv(self):
        child_node = HTMLNode('<a>', 'test2', None, None)
        child_node2 = HTMLNode('<a>', 'test2', None, None)
        node = HTMLNode(
            'p',
            'test',
            [child_node, child_node2],
            {
                "href": "https://www.google.com",
                "target": "_blank"
            }
        )
        expect = "tag: p\nvalue: test\nchildren: 2\nprops: {'href': 'https://www.google.com', 'target': '_blank'}"
        self.assertEqual(expect, repr(node))
    def test_props_to_html(self):
        node = HTMLNode(
            'div',
            None,
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "test-class",
                "style": "height: 100%"
            },
        )
        expect = (
            "href=\"https://www.google.com\" "
            "target=\"_blank\" "
            "class=\"test-class\" "
            "style=\"height: 100%\""
        )
        self.assertEqual(expect, node.props_to_html())
if __name__ == "__main__":
    unittest.main()

import unittest

from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType

class TestParentNode(unittest.TestCase):

    def test_to_html_child(self):
        leaf_node = LeafNode(
            "I'm a test",
            "p",
        )
        leaf_node_2 = LeafNode(
            "Bold test",
            "b",
            None
        )


        node = ParentNode(
            'div',
            [leaf_node, leaf_node_2],
            {
                "id": "root node"
            }
        )
        expect = (
            "<div id=\"root node\">"
                "<p>I'm a test</p>"
                "<b>Bold test</b>"
            "</div>"
        )
        self.assertEqual(expect, node.to_html())

    def test_to_html_grandchild(self):
        leaf_node = LeafNode(
            "Hello, world!",
            "p",
            {
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "test-class",
                "style": "height: 100%"
            },
        )
        leaf_node_2 = LeafNode(
            "Bold test",
            "b",
            None
        )

        child_node = ParentNode(
            'div',
            [leaf_node, leaf_node_2],
            {
                "class": "test-class",
                "style": "height: 100%"
            },
        )

        node = ParentNode(
            'body',
            [child_node],
            None
        )

        expect = (
            "<body>"
                "<div class=\"test-class\" style=\"height: 100%\">"
                    "<p "
                        "href=\"https://www.google.com\" "
                        "target=\"_blank\" "
                        "class=\"test-class\" "
                        "style=\"height: 100%\""
                    ">"
                        "Hello, world!"
                    "</p>"
                    "<b>Bold test</b>"
                "</div>"
            "</body>"
        )
        self.assertEqual(expect, node.to_html())



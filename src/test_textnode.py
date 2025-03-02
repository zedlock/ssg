import unittest

from textnode import TextNode, TextType, text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq_w_url(self):
        node = TextNode(
            "This is a text node",
            TextType.ITALIC,
            "https://www.text.com"
        )
        node2 = TextNode(
            "This is a text node",
            TextType.ITALIC,
            "https://www.text.com"
        )
        self.assertEqual(node, node2)
    def test_not_eq_type(self):
        node = TextNode(
            "This is a text node",
            TextType.ITALIC,
            "https://www.text.com"
        )
        node2 = TextNode(
            "This is a text node",
            TextType.BOLD,
            "https://www.text.com"
        )
        self.assertNotEqual(node, node2)
    def test_not_eq_text(self):
        node = TextNode(
            "This could be a text node",
            TextType.BOLD,
            "https://www.text.com"
        )
        node2 = TextNode(
            "This is a text node",
            TextType.BOLD,
            "https://www.text.com"
        )
        self.assertNotEqual(node, node2)
    def test_not_eq_url(self):
        node = TextNode(
            "This is a text node",
            TextType.BOLD,
            "https://wWw.text.co.uk"
        )
        node2 = TextNode(
            "This is a text node",
            TextType.BOLD,
            "https://www.text.com"
        )
        self.assertNotEqual(node, node2)
    def test_text_node_to_html_node(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_bold_node_to_html_node(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "This is a bold node")
    def test_link_node_to_html_node(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.link.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.link.com")
    def test_img_node_to_html_node(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.image.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "https://www.image.com")
        self.assertEqual(html_node.props["alt"], "This is an image node")


if __name__ == "__main__":
    unittest.main()

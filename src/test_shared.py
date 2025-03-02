import unittest

import shared
from textnode import TextNode, TextType

class TestSharedFunctions(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This **is** a text node", TextType.TEXT)
        node2 = TextNode("This **is** a **text** node", TextType.TEXT)
        node3= TextNode("**just bold**", TextType.TEXT)

        nodes = shared.split_nodes_delimiter([node, node2, node3], '**', TextType.BOLD)
        expections = [
            ('This ', TextType.TEXT),
            ('is', TextType.BOLD),
            (' a text node', TextType.TEXT),
            ('This ', TextType.TEXT),
            ('is', TextType.BOLD),
            (' a ', TextType.TEXT),
            ('text', TextType.BOLD),
            (' node', TextType.TEXT),
            ('just bold', TextType.BOLD),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This _is_ a text node", TextType.TEXT)
        node2 = TextNode("This _is_ a _text_ node", TextType.TEXT)
        node3= TextNode("_just italic_", TextType.TEXT)

        nodes = shared.split_nodes_delimiter([node, node2, node3], '_', TextType.ITALIC)
        expections = [
            ('This ', TextType.TEXT),
            ('is', TextType.ITALIC),
            (' a text node', TextType.TEXT),
            ('This ', TextType.TEXT),
            ('is', TextType.ITALIC),
            (' a ', TextType.TEXT),
            ('text', TextType.ITALIC),
            (' node', TextType.TEXT),
            ('just italic', TextType.ITALIC),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This `is` a text node", TextType.TEXT)
        node2 = TextNode("This `is` a `text` node", TextType.TEXT)
        node3= TextNode("`just code`", TextType.TEXT)

        nodes = shared.split_nodes_delimiter([node, node2, node3], '`', TextType.CODE)
        expections = [
            ('This ', TextType.TEXT),
            ('is', TextType.CODE),
            (' a text node', TextType.TEXT),
            ('This ', TextType.TEXT),
            ('is', TextType.CODE),
            (' a ', TextType.TEXT),
            ('text', TextType.CODE),
            (' node', TextType.TEXT),
            ('just code', TextType.CODE),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)


    def test_split_nodes_delimiter_invalid(self):
        bold = TextNode("This **i** a** text node", TextType.TEXT)
        italic = TextNode("_This is a text node", TextType.TEXT)
        code= TextNode("`just `code`", TextType.TEXT)
        self.assertRaises(
            Exception,
            shared.split_nodes_delimiter,
            [bold],
            '**',
            TextType.BOLD
        )
        self.assertRaises(
            Exception,
            shared.split_nodes_delimiter,
            [italic],
            '_',
            TextType.ITALIC
        )
        self.assertRaises(
            Exception,
            shared.split_nodes_delimiter,
            [code],
            '`',
            TextType.CODE
        )
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]",
            repr(shared.extract_markdown_images(text))
        )
    def test_extract_markdown_images_none(self):
        text = "This is some text with no markdown images"
        self.assertEqual(
            "[]",
            repr(shared.extract_markdown_images(text))
        )
    def test_extract_markdown_images_link(self):
        text = "This is some text with a [link](https://www.google.com) that shouldn't be extracted"
        self.assertEqual(
            "[]",
            repr(shared.extract_markdown_images(text))
        )
    def test_extract_markdown_link(self):
        text = "This is text with a [rick roll](https://www.rickroll.com/test) and [obi wan](https://obi-wan.com/jedi)"
        self.assertEqual(
            "[('rick roll', 'https://www.rickroll.com/test'), ('obi wan', 'https://obi-wan.com/jedi')]",
            repr(shared.extract_markdown_links(text))
        )
    def test_extract_markdown_none(self):
        text = "This is some text with no liks"
        self.assertEqual(
            "[]",
            repr(shared.extract_markdown_links(text))
        )
    def test_extract_markdown_link_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            "[]",
            repr(shared.extract_markdown_links(text))
        )

    def test_split_nodes_link(self):
        text = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
                " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        node = TextNode(text, TextType.TEXT)

        text2 = (
            "This is text with a [rick roll](https://www.rickroll.com/test)"
                " and [obi wan](https://obi-wan.com/jedi)"
                "![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        node2 = TextNode(text2, TextType.TEXT)

        nodes = shared.split_nodes_link([node, node2])
        expections = [
            (text , TextType.TEXT, None),
            ("This is text with a ", TextType.TEXT, None),
            ("rick roll", TextType.LINK, "https://www.rickroll.com/test"),
            (" and ", TextType.TEXT, None),
            ("obi wan", TextType.LINK, "https://obi-wan.com/jedi"),
            ("![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT, None),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)
            self.assertEqual(expections[i][2], nodes[i].url)

    def test_split_nodes_link_none(self):
        text = "text with no links"
        node = TextNode(text, TextType.TEXT)

        text2 = "Still no links here![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        node2 = TextNode(text2, TextType.TEXT)

        nodes = shared.split_nodes_link([node, node2])
        expections = [
            (text , TextType.TEXT, None),
            (text2 , TextType.TEXT, None),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)
            self.assertEqual(expections[i][2], nodes[i].url)

    def test_split_nodes_image(self):
        text = (
            "This is text with a [rick roll](https://www.rickroll.com/test)"
                " and [obi wan](https://obi-wan.com/jedi)"
        )

        text2 = (
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
                " and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
                "[obi wan](https://obi-wan.com/jedi)"
        )
        node = TextNode(text, TextType.TEXT)

        node2 = TextNode(text2, TextType.TEXT)

        nodes = shared.split_nodes_img([node, node2])
        expections = [
            (text , TextType.TEXT, None),
            ("This is text with a ", TextType.TEXT, None),
            ("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            (" and ", TextType.TEXT, None),
            ("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ("[obi wan](https://obi-wan.com/jedi)", TextType.TEXT, None),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)
            self.assertEqual(expections[i][2], nodes[i].url)

    def test_split_nodes_img_none(self):
        text = "text with no images"
        node = TextNode(text, TextType.TEXT)

        text2 = "Still no images here! [obi wan](https://www.website.com)"
        node2 = TextNode(text2, TextType.TEXT)

        nodes = shared.split_nodes_img([node, node2])
        expections = [
            (text , TextType.TEXT, None),
            (text2 , TextType.TEXT, None),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)
            self.assertEqual(expections[i][2], nodes[i].url)

    def test_text_to_text_nodes(self):
        text = (
            "This is **text** "
                "with an _italic_ word "
                "and a `code block` "
                "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
                "and a [link](https://boot.dev)"
        )
        nodes = shared.text_to_text_nodes(text)
        expections = [
            ("This is " , TextType.TEXT, None),
            ("text", TextType.BOLD, None),
            (" with an " , TextType.TEXT, None),
            ("italic", TextType.ITALIC, None),
            (" word and a " , TextType.TEXT, None),
            ("code block", TextType.CODE, None),
            (" and an " , TextType.TEXT, None),
            ("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            (" and a ", TextType.TEXT, None),
            ("link", TextType.LINK, "https://boot.dev"),
        ]

        for i in range(len(expections)):
            self.assertEqual(expections[i][0], nodes[i].text)
            self.assertEqual(expections[i][1], nodes[i].text_type)
            self.assertEqual(expections[i][2], nodes[i].url)

    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.  


- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        expections = [
            "# This is a heading",
            (
                "This is a paragraph of text. "
                    "It has some **bold** and _italic_ words inside of it."
            ),
            (
                "- This is the first list item in a list block"
                    "\n- This is a list item"
                    "\n- This is another list item"
            )
        ]
        self.assertEqual(expections, shared.markdown_to_blocks(text))

    def test_markdown_to_blocks_2(self):
        text = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = shared.markdown_to_blocks(text)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_block_to_block_type(self):
        heading_text = """### this is a heading
fasd

``
        """
        not_heading_text = """
        ### 
        """
        code_text = """```
        test
        fdas
```"""
        not_code_text = """ ```
        test
        fdas
```f"""

        quote_text = """> quote1
>quote2
> quote3"""
        not_quote_text = """> quote1
 > quote2
> quote3"""
        ulist_text = """- quote1
- quote2
- quote3"""
        not_ulist_text = """-quote1
-quote2
- quote3"""

        olist_text = """83. quote1
84. quote2
85. quote3"""
        not_olist_text = """1. quote1
3. quote2
2. quote3"""

        self.assertEqual(shared.BlockType.CODE, shared.block_to_block_type(code_text))
        self.assertEqual(shared.BlockType.PARAGRAPH, shared.block_to_block_type(not_code_text))
        self.assertEqual(shared.BlockType.HEADING, shared.block_to_block_type(heading_text))
        self.assertEqual(shared.BlockType.PARAGRAPH, shared.block_to_block_type(not_heading_text))
        self.assertEqual(shared.BlockType.QUOTE, shared.block_to_block_type(quote_text))
        self.assertEqual(shared.BlockType.PARAGRAPH, shared.block_to_block_type(not_quote_text))
        self.assertEqual(shared.BlockType.UNORDERED_LIST, shared.block_to_block_type(ulist_text))
        self.assertEqual(shared.BlockType.PARAGRAPH, shared.block_to_block_type(not_ulist_text))
        self.assertEqual(shared.BlockType.ORDERED_LIST, shared.block_to_block_type(olist_text))
        self.assertEqual(shared.BlockType.PARAGRAPH, shared.block_to_block_type(not_olist_text))
        
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = shared.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```This is text that _should_ remain
the **same** even with inline stuff
```"""
        node = shared.markdown_to_html_node(md)

        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_ol(self):
        md = """231. Hi! I'm a list item :)
232. Hey I'm a list item too!! :D
233. OMG now way! I'm also a list item!!

1. Hi! I'm a list item :)
2. Hey I'm a list item too!! :D
3. OMG now way! I'm also a list item!!
"""
        node = shared.markdown_to_html_node(md)

        html = node.to_html()
        self.assertEqual(
            html,
            (
                (
                    "<div>"
                        "<ol start=\"231\">"
                        "<li>Hi! I'm a list item :)</li>"
                        "<li>Hey I'm a list item too!! :D</li>"
                        "<li>OMG now way! I'm also a list item!!</li>"
                        "</ol>"
                        "<ol start=\"1\">"
                        "<li>Hi! I'm a list item :)</li>"
                        "<li>Hey I'm a list item too!! :D</li>"
                        "<li>OMG now way! I'm also a list item!!</li>"
                        "</ol>"
                        "</div>"
                )
            )
        )
    def test_ul(self):
        md = """- Hi! I'm a list item :D
- Hey I'm a list item too!! :D
- OMG now way! I'm also a list item!!

- Hi! I'm a list item :D
- Hey I'm a list item too!! :D
- OMG now way! I'm also a list item!!
"""
        node = shared.markdown_to_html_node(md)

        html = node.to_html()
        self.assertEqual(
            html,
            (
                (
                    "<div>"
                        "<ul>"
                        "<li>Hi! I'm a list item :D</li>"
                        "<li>Hey I'm a list item too!! :D</li>"
                        "<li>OMG now way! I'm also a list item!!</li>"
                        "</ul>"
                        "<ul>"
                        "<li>Hi! I'm a list item :D</li>"
                        "<li>Hey I'm a list item too!! :D</li>"
                        "<li>OMG now way! I'm also a list item!!</li>"
                        "</ul>"
                        "</div>"
                )
            )
        )

    def test_quote(self):
        md = """>I'm a quote
>Something deep and thought provoking


> Another quote"""

        node = shared.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                (
                    "<div>"
                    "<blockquote>"
                        "I'm a quote "
                        "Something deep and thought provoking"
                    "</blockquote>"
                    "<blockquote>"
                        " Another quote"
                    "</blockquote>"
                    "</div>"
                )
            )
        )

    def test_heading(self):
        md = "### This is a heading **bold bit** okay"

        node = shared.markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            (
                (
                    "<div>"
                    "<h3>"
                    "This is a heading "
                    "<b>bold bit</b>"
                    " okay"
                    "</h3>"
                    "</div>"
                )
            )
        )
    def test_extract_title(self):
        md = """
test

test

# I'm the title

test
        """
        self.assertEqual(
            "I'm the title",
            shared.extract_title(md)
        )

if __name__ == "__main__":
    unittest.main()

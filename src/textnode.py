from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    def __eq__(self, value) -> bool:
        return self.text == value.text and \
            self.text_type == value.text_type and \
            self.url == value.url
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(text_node.text, None)
        case TextType.BOLD:
            return LeafNode(text_node.text, 'b')
        case TextType.ITALIC:
            return LeafNode(text_node.text, 'i')
        case TextType.CODE:
            return LeafNode(text_node.text, 'code')
        case TextType.LINK:
            return LeafNode(text_node.text, 'a', {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode('', 'img', {"src": text_node.url, "alt": text_node.text})

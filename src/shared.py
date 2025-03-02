from enum import Enum
from parentnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
import functools
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "Heading"
    CODE = "CODE"
    QUOTE = "QUOte"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    for node in old_nodes:
        sub_text = node.text.split(delimiter)
        if len(sub_text) == 1:
            new_nodes.append(node)
        elif len(sub_text) % 2 == 0:
            new_nodes.append(node)
        else:
            new_nodes.extend(make_delimited_nodes(sub_text, text_type))
    return new_nodes

def split_nodes_link(nodes):
    new_nodes = []
    for node in nodes:
        text = node.text
        links = extract_markdown_links(node.text)
        if len(links) < 1:
            new_nodes.append(node)
        else:
            for link in links:
                split = text.split(f"[{link[0]}]({link[1]})", 1)
                text = split[1]
                new_nodes.extend(
                    make_link_or_img_nodes(
                        split[0],
                        link[0],
                        link[1],
                        TextType.LINK
                    )
                )
            if len(text) > 0:
                new_nodes.append(
                    TextNode(
                        text,
                        TextType.TEXT
                    )
                )

    return new_nodes

def split_nodes_img(nodes):
    new_nodes = []
    for node in nodes:
        text = node.text
        images = extract_markdown_images(node.text)
        if len(images) < 1:
            new_nodes.append(node)
        else:
            for image in images:
                split = text.split(f"![{image[0]}]({image[1]})", 1)
                text = split[1]
                new_nodes.extend(
                    make_link_or_img_nodes(
                        split[0],
                        image[0],
                        image[1],
                        TextType.IMAGE
                    )
                )
            if len(text) > 0:
                new_nodes.append(
                    TextNode(
                        text,
                        TextType.TEXT
                    )
                )

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)


def make_delimited_nodes(sub_text, text_type, url=None):
    new_nodes = []
    for i in range(0, len(sub_text)):
        if i % 2 != 0:
            new_nodes.append(
                TextNode(
                    sub_text[i],
                    text_type,
                    url
                )
            )
        else:
            if len(sub_text[i]) > 0:
                new_nodes.append(
                    TextNode(
                        sub_text[i],
                        TextType.TEXT
                    )
                )
    return new_nodes

def make_link_or_img_nodes(left_neighbor, text, url, type):
    new_nodes = []
    if len(left_neighbor) > 0:
        new_nodes.append(
            TextNode(
                left_neighbor,
                TextType.TEXT
            )
        )

    new_nodes.append(
        TextNode(
            text,
            type,
            url
        )
    )

    return new_nodes

def text_to_text_nodes(text):
    delimit_nodes = functools.reduce(
        lambda nodes, deli: split_nodes_delimiter(nodes, deli[0], deli[1]),
        [('**', TextType.BOLD), ('_', TextType.ITALIC), ('`', TextType.CODE)],
        [TextNode(text, TextType.TEXT)],
    )

    all_nodes = functools.reduce(
        lambda nodes, func: func(nodes),
        [split_nodes_img, split_nodes_link],
        delimit_nodes
    )

    return all_nodes

def markdown_to_blocks(markdown):
    blocks = filter(
        lambda block: len(block) > 0,
        map(
            lambda block: block.strip(),
            markdown.split("\n\n")
        )
    )
    return list(blocks)

def block_to_block_type(block):
    if len(re.findall(r"^(#{1,6} )(?:.|\n)*$", block)) > 0:
        return BlockType.HEADING
    if len(re.findall(r"^(```(?:.|\n)*```)$", block)) > 0:
        return BlockType.CODE

    lines = block.split('\n')
    is_quote = True
    for line in lines:
        if len(line) == 0:
            is_quote = False
            break
        if line[0] != '>':
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    is_ulist = True
    for line in lines:
        if len(line) == 0:
            is_ulist = False
            break
        if line[0] != '-' or line[1] != ' ':
            is_ulist = False
            break
    if is_ulist:
        return BlockType.UNORDERED_LIST

    nums = re.findall(r"^(\d+).", block)
    if len(nums) > 0:
        is_olist = True
        n = int(nums[0])
        for line in lines:
            if len(line) == 0:
                is_olist = False
                break
            if line[0:len(str(n)) + 2] != f"{n}. ":
                is_olist = False
                break
            n += 1
        if is_olist:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.ORDERED_LIST:
                n_start = int(re.findall(r"^(\d+).", block)[0])
                block_lines = block.split("\n")

                n = n_start
                for i in range(len(block_lines)):
                    block_lines[i] = block_lines[i][len(str(n)) + 2:] # . and space
                    n += 1

                def lines_to_children(lines, line):
                    return lines + [ParentNode('li', text_to_children(line))]

                children = functools.reduce(
                    lines_to_children,
                    block_lines,
                    list([])
                )

                node = ParentNode(
                    'ol',
                    children,
                    {"start": n_start}
                )
                nodes.append(node)
            case BlockType.UNORDERED_LIST:
                block_lines = block.split("\n")

                for i in range(len(block_lines)):
                    block_lines[i] = block_lines[i][2:] # : and space

                def lines_to_children(lines, line):
                    return lines + [ParentNode('li', text_to_children(line))]

                children = functools.reduce(
                    lines_to_children,
                    block_lines,
                    list([])
                )

                node = ParentNode(
                    'ul',
                    children
                )
                nodes.append(node)
            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                node = ParentNode('p', children)
                nodes.append(node)
            case BlockType.QUOTE:
                block_lines = list(filter(
                    lambda line: len(line) > 2, # just empty > and space
                    block.split("\n")
                ))

                for i in range(len(block_lines)):
                    block_lines[i] = block_lines[i][2:]

                block = "\n".join(block_lines)

                node = ParentNode(
                    'blockquote',
                    text_to_children(block)
                )
                nodes.append(node)
            case BlockType.HEADING:
                n = 0
                while n < 6:
                    if block[n] == '#':
                        n += 1
                    else:
                        break


                block = block[n + 1:];
                children = text_to_children(block)
                node = ParentNode(f"h{n}", children)
                nodes.append(node)
            case BlockType.CODE:
                block = block[4:-4] #``` and \n
                code_node = TextNode(
                    block,
                    TextType.CODE
                )
                children = [text_node_to_html_node(code_node)]
                node = ParentNode(
                    'pre',
                    children
                )
                nodes.append(node)
    return ParentNode(
        'div',
        nodes
    )
def text_to_children(text):
    text = text.replace("\n", " ")
    children = list(map(
        text_node_to_html_node,
        text_to_text_nodes(text)
    ))

    return children
def extract_title(markdown):
    title = False

    for line in markdown.split("\n"):
        if line[0:2] == "# ":
            title = line[2:]
            break

    if not title:
        raise Exception("markdown file needs a tile")

    return title


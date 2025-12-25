from mkdn_to_blocks import markdown_to_blocks
from blocktype_enum import block_to_block_type, BlockType
from htmlnode import ParentNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode
from inline_par import text_to_children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        node = block_to_html_node(block)
        children.append(node)
    return ParentNode(tag="div", children=children)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    return paragraph_to_html_node(block)

def heading_to_html_node(block):
    level = len(block.split()[0])
    text = " ".join(block.split()[1:])
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    text = block[4:-3].strip()
    return ParentNode("pre", [
        LeafNode("code", text)
    ])

def quote_to_html_node(block):
    lines = [line[1:].strip() for line in block.split("\n")]
    text = " ".join(lines)
    children = text_to_children(text)
    return ParentNode("blockquote", children)

def unordered_list_to_html_node(block):
    items = block.split("\n")
    children = [list_item_to_html_node(item[2:]) for item in items]
    return ParentNode("ul", children=children)

def ordered_list_to_html_node(block):
    items = block.split("\n")
    children = [list_item_to_html_node(item.split(". ", 1)[1]) for item in items]
    return ParentNode("ol", children=children)

def list_item_to_html_node(text):
    children = text_to_children(text)
    return ParentNode("li", children)

def paragraph_to_html_node(block):
    children = text_to_children(block)
    return ParentNode("p", children)

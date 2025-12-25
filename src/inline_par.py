from textnode import TextNode, TextType
from htmlnode import text_node_to_html_node
from delim import split_nodes_delimiter
from splitnodes import split_nodes_image, split_nodes_link


def text_to_children(text):
    node = TextNode(text, TextType.TEXT)
    nodes = [node]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return [text_node_to_html_node(n) for n in nodes]

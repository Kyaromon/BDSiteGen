from typing import List, Tuple
from textnode import TextNode, TextType
from bdregex import extract_markdown_images, extract_markdown_links


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        text = node.text
        for alt, url in images:
            parts = text.split(f"![{alt}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text = node.text
        for anchor, url in links:
            parts = text.split(f"[{anchor}]({url})", 1)
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text = parts[1]

        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

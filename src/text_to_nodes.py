from typing import List

def text_to_textnodes(text: str) -> List[TextNode]:
    node = [TextNode(text, TextType.TEXT)]
    nodes = [node]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes

from inline_markdown import text_to_textnodes
from textnode import TextType
from htmlnode import LeafNode
from gencontent import text_node_to_html_node  # or wherever that function lives

text = "Disney _didn't ruin it_ (okay, but Amazon might have)"
nodes = text_to_textnodes(text)

print("RAW TEXT NODES:")
for n in nodes:
    print(repr(n.text), n.text_type)

print("\nHTML NODES:")
for n in nodes:
    html_node = text_node_to_html_node(n)
    print(html_node.to_html())

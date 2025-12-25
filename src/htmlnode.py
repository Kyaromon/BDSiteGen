from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html not implemented")

    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f'{k}="{v}"' for k, v in self.props.items()])
    def __repr__(self):
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        return f"<{self.tag}{(' ' + props_str) if props_str else ''}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have children")
        children_html = "".join(child.to_html() for child in self.children)
        props_str = self.props_to_html()
        return f"<{self.tag}{(' ' + props_str) if props_str else ''}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode(
            tag="a",
            value=text_node.text,
            props={"href": text_node.url}
        )
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode(
            tag="img",
            value="",
            props={"src": text_node.url, "alt": text_node.text}
        )
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")

import os
import shutil

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode
from mkdn_to_blocks import markdown_to_blocks
from extract_title_mkdn import extract_title
from mkdn_to_html import markdown_to_html_node

def copy_static_to_public(source_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        print(f"Deleted {dest_dir}")

    os.mkdir(dest_dir)
    print(f"Created {dest_dir}")

    copy_recursive(source_dir, dest_dir)

def copy_recursive(src, dst):
    items = os.listdir(src)
    for item in items:
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)

        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Copied {src_path} -> {dst_path}")
        else:
            os.mkdir(dst_path)
            print(f"Created directory {dst_path}")
            copy_recursive(src_path, dst_path)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as f:
        markdown_content = f.read()

    with open(template_path, 'r') as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_string = html_node.to_html()
    title = extract_title(markdown_content)

    page = template.replace("{{ Title }}", title)
    page = page.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path) and item.endswith(".md"):
            relative_path = os.path.relpath(item_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, relative_path)
            dest_path = dest_path.replace(".md", ".html")
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            generate_page(item_path, template_path, dest_path)
        elif os.path.isdir(item_path):
            sub_dest = os.path.join(dest_dir_path, os.path.basename(item_path))
            generate_pages_recursive(item_path, template_path, sub_dest)

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    content_dir = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")

    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)

    copy_static_to_public(static_dir, public_dir)
    generate_pages_recursive(content_dir, template_path, public_dir)
    print("Website generated.")

if __name__ == "__main__":
    main()

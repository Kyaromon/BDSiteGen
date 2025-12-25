from enum import Enum

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith("#") and " " in block and block.lstrip("#").startswith(" "):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(
        line.split(". ", 1)[0].isdigit() and
        int(line.split(". ", 1)[0]) == i + 1
        for i, line in enumerate(lines)
    ):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

from htmlnode import ParentNode
from textnode import text_node_to_html_node
from inline_markdown import text_to_textnodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return "paragraph"
        return "unordered_list"
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return "paragraph"
            i += 1
        return "ordered_list"
    return "paragraph"


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == "paragraph":
        return paragraph_block_to_node(block)

    if block_type == "heading":
        return heading_block_to_node(block)

    if block_type == "code":
        return code_block_to_node(block)

    if block_type == "ordered_list":
        return ordered_block_to_node(block)

    if block_type == "unordered_list":
        return unordered_block_to_node(block)

    if block_type == "quote":
        return quote_block_to_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for t_node in text_nodes:
        html_node = text_node_to_html_node(t_node)
        children.append(html_node)
    return children


def paragraph_block_to_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_block_to_node(block):
    count = 0
    for char in block:
        if char != "#":
            break
        else:
            count += 1
    if count + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {count}")

    text = block[count + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)


def code_block_to_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def ordered_block_to_node(block):
    list_items = block.split("\n")
    html_lst_items = []
    for item in list_items:
        text = item[3:]
        children = text_to_children(text)
        html_lst_items.append(ParentNode("li", children))
    return ParentNode("ol", html_lst_items)


def unordered_block_to_node(block):
    list_items = block.split("\n")
    html_lst_items = []
    for item in list_items:
        text = item[2:]
        children = text_to_children(text)
        html_lst_items.append(ParentNode("li", children))
    return ParentNode("ul", html_lst_items)


def quote_block_to_node(block):
    lines = block.split("\n")
    filtered_lines = []
    for line in lines:
        if not line.startswith(">"):
            return ValueError("Invalid quote block")
        filtered_lines.append(line.lstrip(">").strip())
    content = " ".join(filtered_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

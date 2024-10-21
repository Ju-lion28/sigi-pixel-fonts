import os
import json
import xml.etree.ElementTree as ET

def create_svg(glyph: dict, height: int) -> ET.ElementTree:
    
    glyph_width: int = glyph["width"]
    glyph_coords: list[list[int]] = glyph['coords']

    svg = ET.Element("svg", width=str(glyph_width), height=str(height), 
                     xmlns="http://www.w3.org/2000/svg", version="1.1")

    visited = set()
    paths = []

    for x, y in glyph_coords:
        if (x, y) in visited:
            continue

        # Start a new path
        path_data = []
        current_path = [(x, y)]
        visited.add((x, y))

        # Horizontal continuation
        while (x + 1, y) in glyph_coords and (x + 1, y) not in visited:
            x += 1
            current_path.append((x, y))
            visited.add((x, y))

        # Close the horizontal path
        if len(current_path) > 1:
            path_data.append(f"M{current_path[0][0]} {current_path[0][1]}")
            path_data.append(f"H{current_path[-1][0] + 1}")

        # Add vertical continuation if needed
        for (x, y) in current_path:
            if (x, y + 1) in glyph_coords and (x, y + 1) not in visited:
                path_data.append(f"V{y + 1}")
                visited.add((x, y + 1))

        if path_data:
            paths.append(' '.join(path_data))
    
    # Create path element and add to the SVG
    if paths:
        path_element = ET.Element("path", d=' '.join(paths), fill="black")
        svg.append(path_element)

    tree = ET.ElementTree(svg)
    return tree

def format_name(codepoint: int) -> str:
    replacements = {
        '<': 'LESS_THAN',
        '>': 'GREATER_THAN',
        ':': 'COLON',
        '"': 'QUOTE',
        '/': 'SLASH',
        '\\': 'BACKSLASH',
        '|': 'PIPE',
        '?': 'QUESTION_MARK',
        '*': 'ASTERISK',
        ' ': 'SPACE'
    }
    
    name = chr(codepoint)
    for char, replacement in replacements.items():
        name = name.replace(char, replacement)
    
    return name

def save_svg(tree: ET.ElementTree, font_name: str, glyph_codepoint: int):
    formatted_glyph_name: str = format_name(glyph_codepoint)
    tree.write(f"./svg_fonts/{font_name}/{formatted_glyph_name}.svg")


if __name__ == "__main__":
    if not os.path.exists(f"./svg_fonts"):
        os.mkdir(f"./svg_fonts")

    # use test directories (temporary)
    for file in os.listdir("./test_json_fonts"):
        if file.endswith('.json'):
            with open(f"./test_json_fonts/{file}", 'r') as f:
                font_data: dict= json.load(f)

            font_name: str = font_data['name']
            font_height: int = font_data['height']
            glyphs: list[dict] = font_data['glyphs']

            if not os.path.exists(f"./svg_fonts/{font_name}"):
                os.mkdir(f"./svg_fonts/{font_name}")

            for glyph in glyphs:
                glyph_svg: ET.ElementTree = create_svg(glyph, font_height)
                save_svg(glyph_svg, font_name, glyph['codepoint'])

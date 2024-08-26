import os
import json
import xml.etree.ElementTree as ET

def create_svg(glyph: dict, height: int) -> ET.ElementTree:
    
    glyph_width: int = glyph["width"]
    glyph_coords: list[list[int]] = glyph['coords']

    svg = ET.Element("svg", width=str(glyph_width), height=str(height), 
                     xmlns="http://www.w3.org/2000/svg", version="1.1")

    for x, y in glyph_coords:
        neighbours: dict[tuple[int,int],int] = {
            ( 1, 0): 0,
            ( 0, 1): 0,
            (-1, 0): 0,
            ( 0,-1): 0
        }
        for dx, dy in neighbours.keys():
            nx, ny = x + dx, y + dy
            while (0<=nx < glyph_width) and (0<=ny < height) and ([nx,ny] in glyph_coords):
                neighbours[(dx,dy)] += 1
                nx, ny = nx + dx, ny + dy
                
        print(f"{x,y} -> {neighbours}")

    # for coord in glyph_coords:
    #     x: int = coord[0]
    #     y: int = coord[1]
    #     rect = ET.Element("rect", x=str(x), y=str(y), width="1", height="1", fill="black")
    #     svg.append(rect)

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

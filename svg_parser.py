import re
import xml.etree.ElementTree as ET

from svg.path import parse_path
from PIL import Image, ImageDraw
# matplotlib
import matplotlib.pyplot as plt
import cairosvg



svg_file_path = "chart.svg"



def parse_svg_rectangles(svg_file_path):
    tree = ET.parse(svg_file_path)
    root = tree.getroot()

    # which path node and start with d=...
    rectangles = []

    g_nodes = root.findall("{http://www.w3.org/2000/svg}g")[0]
    x_offset, y_offset = g_nodes.attrib['transform'].split('(')[1].split(')')[0].split(',')[0:2]

    # using regex to find all path-d nodes
    regex = re.compile(r'path d="M(\d+\.?\d*),(\d+\.?\d*)h(\d+\.?\d*)v(\d+\.?\d*)h-(\d+\.?\d*)Z"\s *style="fill: (#[0-9a-fA-F]*)')

    # load svg file to string
    svg_str = ET.tostring(root, encoding='utf8', method='xml').decode('utf8')

    # for all path nodes
    for path_node in regex.findall(svg_str):
        x, y, w, h, _, c = path_node
        # add x, y offset
        x, y = float(x) + float(x_offset), float(y) + float(y_offset)
        rectangles.append((x, y, float(w), float(h), c))

    return rectangles


# main
if __name__ == "__main__":
    rectangles = parse_svg_rectangles(svg_file_path)

    # Convert SVG to PNG
    cairosvg.svg2png(url='chart.svg', write_to='test.png')

    # draw rectangles on raw image via PIL
    im = Image.open('test.png')
    draw = ImageDraw.Draw(im)

    for rectangle in rectangles:
        x, y, w, h, c = rectangle
        # hex color to rgb, for example: #ff0000 -> (255, 0, 0)
        c = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
        draw.rectangle((x, y, x + w, y + h), outline=c)
        # draw a + in the center of rectangle, color is red
        draw.text((x + w / 2, y + h / 2), "+", fill=(255, 0, 0))

    # save to image
    im.save('test.png')



import os
import re
import glob
import random
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw
# matplotlib
import matplotlib.pyplot as plt
import cairosvg
# from svglib.svglib import svg2rlg
# from reportlab.graphics import renderPDF, renderPM
import tqdm


def convert_svg_to_png(svg_file_path):
    # get svg file name without extension
    svg_file_name = os.path.splitext(svg_file_path)[0]
    # convert svg to png
    cairosvg.svg2png(url=svg_file_path, write_to=svg_file_name + '.png')
    return svg_file_name + '.png'


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


def parse_svg_lines(svg_file_path):
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    # which path node and start with d=...
    lines = []
    g_nodes = root.findall("{http://www.w3.org/2000/svg}g")[0]
    x_offset, y_offset = g_nodes.attrib['transform'].split('(')[1].split(')')[0].split(',')[0:2]
    print("x_offset: ", x_offset, "\ny_offset: ", y_offset)
    # using regex to find all path-d nodes
    regex = re.compile(r'd=\"M[L0-9,.]{4,}\"')
    regex2 = re.compile(r'[ML](\d+\.?\d*),(\d+\.?\d*)]*')
    # load svg file to string
    svg_str = ET.tostring(root, encoding='utf8', method='xml').decode('utf8')
    # for all path nodes
    for idx, line_node in enumerate(regex.findall(svg_str)):
        for xy_node in regex2.findall(line_node):
            x, y = xy_node
            # ad x, y offset
            x, y = float(x) + float(x_offset), float(y) + float(y_offset)
            print(x, y)
            lines.append((x, y, idx))

    return lines


def parse_svg_area(svg_file_path):
    tree = ET.parse(svg_file_path)
    root = tree.getroot()
    # which path node and start with d=...
    lines = []
    g_nodes = root.findall("{http://www.w3.org/2000/svg}g")[0]
    x_offset, y_offset = g_nodes.attrib['transform'].split('(')[1].split(')')[0].split(',')[0:2]
    print("x_offset: ", x_offset, "\ny_offset: ", y_offset)
    # using regex to find all path-d nodes
    regex = re.compile(r'd=\"M[L0-9,.]{4,}Z\"')
    regex2 = re.compile(r'[ML](\d+\.?\d*),(\d+\.?\d*)]*')
    # load svg file to string
    svg_str = ET.tostring(root, encoding='utf8', method='xml').decode('utf8')
    # for all path nodes
    for idx, line_node in enumerate(regex.findall(svg_str)):
        for xy_node in regex2.findall(line_node):
            x, y = xy_node
            # ad x, y offset
            x, y = float(x) + float(x_offset), float(y) + float(y_offset)
            lines.append((x, y, idx))

    return lines


def svg2yolo_bar(dir_path):
    svgs = glob.glob(os.path.join(dir_path, '*.svg'))
    for svg_file_path in tqdm.tqdm(svgs):
        # get svg file name without extension
        svg_file_name = os.path.splitext(svg_file_path)[0]
        # write to yolo txt file format as (x, y, w, h, c)
        rectangles = parse_svg_rectangles(svg_file_path)
        # convert svg to png
        convert_svg_to_png(svg_file_path)
        # write to txt file
        with open(svg_file_name + '.txt', 'w') as f:
            for rectangle in rectangles:
                x, y, w, h, c = rectangle
                # write to file
                f.write(f'{x},{y},{w},{h},{c}\n')


def svg2yolo_line(dir_path):
    svgs = glob.glob(os.path.join(dir_path, '*.svg'))
    for svg_file_path in tqdm.tqdm(svgs):
        # get svg file name without extension
        svg_file_name = os.path.splitext(svg_file_path)[0]
        # write to yolo txt file format as (x, y, w, h, c)
        lines = parse_svg_lines(svg_file_path)
        # convert svg to png
        convert_svg_to_png(svg_file_path)
        # write to txt file
        with open(svg_file_name + '.txt', 'w') as f:
            for line in lines:
                x, y, c = line
                # write to file
                f.write(f'{x},{y},{c}\n')


def svg2yolo_area(dir_path):
    svgs = glob.glob(os.path.join(dir_path, '*.svg'))
    for svg_file_path in tqdm.tqdm(svgs):
        # get svg file name without extension
        svg_file_name = os.path.splitext(svg_file_path)[0]
        # write to yolo txt file format as (x, y, w, h, c)
        lines = parse_svg_area(svg_file_path)
        # convert svg to png
        convert_svg_to_png(svg_file_path)
        # write to txt file
        with open(svg_file_name + '.txt', 'w') as f:
            for line in lines:
                x, y, c = line
                # write to file
                f.write(f'{x},{y},{c}\n')


def show_data_bar(svg_path):
    rectangles = parse_svg_rectangles(svg_path)
    # Convert SVG to PNG
    png_path = convert_svg_to_png(svg_path)
    # draw rectangles on raw image via PIL
    im = Image.open(png_path)
    draw = ImageDraw.Draw(im)

    for rectangle in rectangles:
        x, y, w, h, c = rectangle
        # hex color to rgb, for example: #ff0000 -> (255, 0, 0)
        c = tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))
        draw.rectangle((x, y, x + w, y + h), outline=(0, 255, 0))
        # draw a + in the center of rectangle, color is red
        draw.text((x + w / 2, y + h / 2), "+", fill=(255, 0, 0))

    # save to image
    im.save(png_path)


def show_data_line(svg_path):
    lines = parse_svg_lines(svg_path)
    # Convert SVG to PNG
    png_path = convert_svg_to_png(svg_path)
    # draw rectangles on raw image via PIL
    im = Image.open(png_path)
    draw = ImageDraw.Draw(im)

    for line in lines:
        x, y, idx = line
        draw.point((x, y), fill=(255, 0, 0))
        draw.text((x, y), "#", fill=(255, 0, 0))

    # save to image
    im.save(png_path)


def show_data_area(svg_path):
    lines = parse_svg_area(svg_path)
    # Convert SVG to PNG
    # png_path = convert_svg_to_png(svg_path)
    png_path = svg_path.replace('.svg', '.png')
    # draw rectangles on raw image via PIL
    im = Image.open(png_path)
    draw = ImageDraw.Draw(im)

    for line in lines:
        x, y, idx = line
        draw.point((x, y), fill=(255, 0, 0))
        draw.text((x, y), "#", fill=(255, 0, 0))

    # save to image
    im.save(png_path)


# main
if __name__ == "__main__":
    # # convert all svg files to png and yolo txt file
    # svg2yolo_bar('')
    svg2yolo_line('data')
    # svg2yolo_area('')

    # # show data
    # show_data_bar('debug.svg')
    # show_data_line('debug.svg')
    # show_data_area('debug.svg')

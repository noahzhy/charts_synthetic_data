import os
import time
import random
import hashlib

import tqdm
import numpy as np
import pandas as pd
import altair as alt
from altair_saver import save
from vega_datasets import data
from random_words import RandomWords


# random words as x-axis
words = RandomWords().random_words(count=200)
fonts = [
    'Arial', 'Helvetica', 'Times', 'Garamond', 'Courier',
    'Verdana', 'Georgia', 'Palatino', 'Gill Sans', 'Comic Sans MS',
    'Arial Unicode MS', 'Impact', 'Lucida Console', 'Tahoma',
]
colors = [
    '#e35331', '#001b76', '#be7668', '#854059', '#7c8e6e',
    '#bac588', '#59755c', '#525775', '#aa2b0b', '#eaa177',
    '#56769d', '#d4b2a1', '#753b4f', '#eda64a', '#ca663f',
    '#f1b89c', '#9a0800', '#e29782', '#d2a235', '#b1b789',
    '#f7cf56', '#b3c2a1', '#e1524c', '#526484', '#a5c4bf',
    '#e5c1b4', '#9e5d68', '#f0b080', '#e5a0a3', '#964324',
]
backgrounds = [
    '#ffffff', '#f0f0f0', '#f5f5f5', '#f8f8f8', '#fbfbfb',
    '#f9f9f9', '#fafafa', '#fcfcfc', '#fefefe', '#ffe7c9',
    '#fffae0', '#fffacd', '#fff8dc', '#fff68f', '#fffafa',
    '#fff5ee', '#fff0f5', '#fffff0', '#ffffe0', '#fff5e6',
    '#ffe8d1', '#ffe7d0', '#ffe8c9', '#fff0dd', '#ffeddc',
    '#ffecd5', '#ffdba0', '#fff1e3', '#ffebd8', '#ffe6cd',
    '#fff2bb', '#ffe7cf', '#fff2df', '#ffe8ca', '#fff8e7',
]

# random hex color
def random_color():
    return random.choice(colors)


current_bg_color = ""
def random_background():
    global current_bg_color
    current_bg_color = random.choice(backgrounds)
    return current_bg_color


def old_theme():
    theme_config = {
        "config": {
            "title": {
                "font": random.choice(fonts),
                "anchor": "middle",
                "fontColor": "#000000",
                # title padding
                "offset": random.randint(0, 15),
            },
            # hide legend
            "legend": {
                "title": "",
                # hide label
                "labelFontSize": 0,
                # hide symbol
                "symbolSize": 0,
                # hide title
                "titleFontSize": 0,
            },
            "axisX": {
                # hide axis x
                "title": "",
                "bandPosition": random.choice([0, 0.5, 1]),
                "grid": True,
                # hide stick
                "ticks": False,
                "gridColor": '#000000',
                # transparent
                "gridOpacity": random.uniform(0.2, 0.8),
                "gridWidth": random.uniform(0.2, 1.0),
                "labelAngle": 0,
                # font
                "labelFont": random.choice(fonts),
                # font size
                "labelFontSize": random.randint(8, 16),
                # padding
                "labelPadding": random.randint(2, 5),
            },
            "axisY": {
                # hide axis y
                "title": "",
                "bandPosition": random.choice([0, 0.5, 1]),
                "labels": True,
                "grid": True,
                "gridColor": '#000000',
                "gridOpacity": random.uniform(0.2, 0.8),
                "gridWidth": random.uniform(0.2, 1.5),
                "labelAngle": 0,
                # font
                "labelFont": random.choice(fonts),
                # font size
                "labelFontSize": random.randint(8, 16),
                # tick interval
                "tickCount": random.randint(5, 20),
                # hide stick
                "ticks": False if random.uniform(0, 1) > 0.5 else True,
            },
            # transparent background
            "background": random_background(),
            # line color
            "line": {
                "filled": False,
                "strokeWidth": random.uniform(2.5, 4.5),
                "fillOpacity": 1,
                # point color
                "point": {
                    "filled": False,
                    "size": random.uniform(25, 40),
                    "fillOpacity": 1,
                    "fill": current_bg_color,
                    # stroke width
                    "strokeWidth": random.uniform(0.5, 1.0),
                } if random.uniform(0, 1) > 0.5 else {
                    "filled": True,
                },
            } if random.uniform(0, 1) > 0.5 else {
                "filled": False,
                "strokeWidth": random.uniform(1.0, 3.5),
                "fillOpacity": 1,
            },
            # color range
            "range": {
                "category": colors,
            },
        }
    }
    return theme_config


# register
alt.themes.register("old_theme", old_theme)
alt.themes.enable("old_theme")

print('current background color:', current_bg_color)


# random name with md5 hash
def random_file_name():
    _name = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    return _name


# func to generate random data
def random_data(x_num=10, y_max=100, y_min=0):
    # random pick via x_num if list
    if isinstance(x_num, list):
        x_num = random.randint(x_num[0], x_num[1])

    # random year invertal
    _y_step = random.randint(5, 20)

    datas = pd.DataFrame()
    for i in range(random.randint(2, 3)):
        # random date
        _date = pd.date_range('1900', '2000', freq='{}Y'.format(_y_step))[:x_num]
        _date = _date.strftime('%Y')
        # random price
        _price = np.random.randint(50, 200, size=len(_date))
        # /= random.uniform(1, 10)
        _price = _price / random.choice([1, 3, 5, 8])
        # add to datas
        symbol_data = pd.DataFrame({
            'c': i,
            'x': _date,
            'y': _price,
        })
        # pandas data extend
        datas = pd.concat([datas, symbol_data])
    return datas


def random_title():
    _title = ' '.join(random.sample(words, random.randint(2, 3)))
    # random lower case or upper case or first letter upper case
    _title = random.choice([_title.lower(), _title.upper(), _title.title()])
    return {
        'text': _title if random.uniform(0, 1) > 0.25 else '',
        'anchor': 'middle',
        'fontSize': random.randint(12, 18),
        'fontStyle': random.choice(['normal', 'italic', 'oblique']),
        'font': random.choice(fonts),
        'color': '#000000',
    }


def synth_data(save_dir='data', debug=False):
    # properties = random_properties()
    data = random_data(x_num=[5, 25])

    charts = alt.Chart(
        data,
        title=random_title(),
    ).mark_line(
    ).encode(
        x="x:T",
        y="y:Q",
        # 根据 c 列的值来着色
        color=alt.Color("c:N", scale=alt.Scale(range=random.sample(colors, 10))),
    ).properties(
        # x-axis scale
        width=random.randint(300, 400),
        height=random.randint(300, 400),
    )

    _fname = random_file_name() if not debug else 'debug'

    # save to .svg file
    # print('===========')
    # get theme background color
    charts.save(os.path.join(save_dir, _fname + '.svg'))
    # print('save to', os.path.join(save_dir, _fname + '.svg'))


# main
if __name__ == "__main__":
    for i in tqdm.tqdm(range(30000)):
        synth_data(save_dir='data', debug=False)

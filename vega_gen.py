import time
import random
import hashlib

import tqdm
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
    '#bbbdb4', '#001b76', '#c9b598', '#854059', '#252900',
    '#bac588', '#947360', '#2d0e00', '#aa2b0b', '#eaa177',
    '#937c6f', '#d4b2a1', '#e5cfbe', '#ad9585', '#ca663f',
    '#b7b1a4', '#9a0800', '#947c6f', '#d2a235', '#c8beae',
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


def old_theme():
    return {
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
                "grid": random.choice([True, False]),
                # hide stick
                "ticks": False,
                "gridColor": '#000000',
                # transparent
                "gridOpacity": random.uniform(0.1, 1),
                "gridWidth": random.uniform(0, 1.0),
                "labelAngle": random.choice([45, 60, -90, -45, -60]),
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
                # hide label
                "labels": random.choice([True, False]),
                "grid": random.choice([True, False]),
                "gridColor": '#000000',
                "gridOpacity": random.uniform(0.1, 1),
                "gridWidth": random.uniform(0, 1.5),
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
            "background": random.choice(backgrounds),
            # bar color
            "mark": {
                "color": random_color(),
                "stroke": "#000" if random.uniform(0, 1) > 0.5 else "transparent",
                "strokeWidth": random.uniform(0.5, 1.5),
            },
            # color range
            "range": {
                "category": colors,
            },
        }
    }


# register
alt.themes.register("old_theme", old_theme)
alt.themes.enable("old_theme")


# random name with md5 hash
def random_file_name():
    _name = hashlib.md5(str(time.time()).encode('utf-8')).hexdigest()
    return _name


# func to generate random properties
def random_properties():
    return {
        'width': random.randint(18, 25),
    }


# func to generate random data
def random_bar(x_num=10, y_max=100, y_min=0):
    # random pick via x_num if list
    if isinstance(x_num, list):
        x_num = random.randint(x_num[0], x_num[1])

    _words = random.sample(words, x_num)

    # random y-axis
    _y_list = []
    # scale in [5, 10, 20, 50, 100]
    scale = random.choice([1, 5, 10, 20, 50, 100])
    for i in range(x_num):
        _y_list.append(random.randint(y_min, y_max) / scale)

    # colors = []
    # # random number
    # for i in range(x_num):
    #     colors.append(random.randint(1, 5))

    return {
        'x': _words,
        'y': _y_list,
        # 'c': colors,
    }


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

def synth_data():
    properties = random_properties()
    data = pd.DataFrame(random_bar(x_num=[5, 25]))

    charts = alt.Chart(
        data,
        title=random_title(),
    ).mark_bar(
        size=properties['width'] + random.randint(-8, -2),
    ).encode(
        x="x:N",
        y="y:Q",
        # random color or fixed color
        color="x:N" if random.uniform(0, 1) > 0.5 else alt.value(random_color()),
        # color="c:N",
    ).properties(
        width=alt.Step(properties['width']),
    )

    _fname = random_file_name()
    # save to .svg file
    charts.save('data/' + _fname + '.svg')
    print('save to data/' + _fname + '.svg')

# main
if __name__ == "__main__":
    # generate 100 random charts
    for i in tqdm.tqdm(range(10000)):
        synth_data()

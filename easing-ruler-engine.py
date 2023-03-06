#!/usr/bin/env python3

ruler_easing_functions = {
    "linear":     lambda t: t,
    "squared":    lambda t: t * t,
    "smoothstep": lambda t: t * t * (3 - 2 * t)
}

ruler_svg_style = """
    <style>
    .primary {
        fill: none;
        stroke-width: 2px;
        stroke: #000000;
    }
    .secondary {
        fill: none;
        stroke-width: 1px;
        stroke: #000000;
        stroke-miterlimit: 4;
        stroke-dasharray: 1, 2;
        stroke-dashoffset: 0;
    }
    </style>
"""

import os
from textwrap import dedent

# Easing ruler - straight

for (ruler_easing_function_name, ruler_easing_function) in ruler_easing_functions.items():
    os.makedirs(
        "rulers/easing-straight-{}".format(
            ruler_easing_function_name,
        ),
        exist_ok = True,
    )

    for frames in range(4, 11):
        ruler_svg_path = "rulers/easing-straight-{}/ruler-easing-straight-{}-{}f.svg".format(
            ruler_easing_function_name,
            ruler_easing_function_name,
            frames,
        )

        ruler_primary_lines = ""
        for t in map(lambda line: line / (frames - 1), range(1, frames - 1)):
            ruler_primary_lines += '<line class="primary" x1="{x}" y1="0" x2="288" y2="384" />'.format(
                x = ruler_easing_function(t) * 576,
            )

        ruler_secondary_lines = ""
        for t in map(lambda line: line / 12, range(1, 12)):
            ruler_secondary_lines += '<line class="secondary" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" />'.format(
                x1 = t * 288,
                x2 = 576 - (t * 288),
                y = t * 384,
            )
        ruler_secondary_lines += '<line class="secondary" x1="288" y1="0" x2="288" y2="384" />'

        ruler_svg_data = dedent("""\
            <svg width="576" height="384" viewBox="0 0 576 384" xmlns="http://www.w3.org/2000/svg">
                {}
                <g id="ruler">
                    <polygon class="primary" points="0,0 576,0 288,384" />
                    {}
                    {}
                </g>
            </svg>
        """).format(
            ruler_svg_style,
            ruler_primary_lines,
            ruler_secondary_lines
        )

        with open(ruler_svg_path, "w") as ruler_svg_file:
            ruler_svg_file.write(ruler_svg_data)

# Easing ruler - radial

for (ruler_easing_function_name, ruler_easing_function) in ruler_easing_functions.items():
    os.makedirs(
        "rulers/easing-radial-{}".format(
            ruler_easing_function_name,
        ),
        exist_ok = True,
    )

    for frames in range(4, 11):
        for degrees in [90, 120, 180, 240, 270, 360]:
            ruler_svg_path = "rulers/easing-radial-{}/ruler-easing-radial-{}-{}deg-{}f.svg".format(
                ruler_easing_function_name,
                ruler_easing_function_name,
                degrees,
                frames,
            )
            # TODO
            print(ruler_svg_path)

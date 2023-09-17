#!/usr/bin/env python3

import os
from textwrap import dedent

from svg_utils import svg_style, svg_format_float

head_body_ratios = {
    #                    head_width_ratio
    #                    |      shoulder_width_ratio
    #                    |      |      waist_width_ratio
    #                    |      |      |      hip_width_ratio
    #                    |      |      |      |      feet_width_ratio
    #                    |      |      |      |      |      neck_length_ratio
    #                    |      |      |      |      |      |      upper_body_length_ratio
    #                    |      |      |      |      |      |      |      lower_body_length_ratio
    #                    |      |      |      |      |      |      |      |      legs_length_ratio
    #                    |      |      |      |      |      |      |      |      |
    "1:2-female":       [1.000, 0.450, 0.400, 0.500, 0.250, 0.025, 1 / 4, 1 / 4, 1 / 2],
    "1:2-long-torso":   [1.000, 0.450, 0.400, 0.500, 0.250, 0.025, 1 / 3, 1 / 3, 1 / 3],
    "1:2-standard":     [1.000, 0.600, 0.530, 0.660, 0.333, 0.025, 1 / 4, 1 / 4, 1 / 2],
    "1:2.5-standard":   [1.000, 0.675, 0.600, 0.750, 0.375, 0.050, 1 / 3, 1 / 3, 5 / 6],
    "1:3-female":       [1.000, 0.450, 0.400, 0.500, 0.250, 0.050, 1 / 2, 1 / 2,     1],
    "1:6-standard":     [1.000, 0.900, 0.800, 1.000, 0.500, 0.100,     1,     1,     3],
}

# Viewbox coordinates:
#
#    |--------VIEWBOX--------|
#          |--CONTENT--|
#  -128   -64    0     64   128
#    +-----|----ooo----|-----+ 0     -  -
#    |     | ooo   ooo |     |       |  |
#    |     |o         o|     |       |  |
#    |     o   |   |   o     |       |  |
#    |     |o         o|     |       |  |
#    |     | ooo   ooo |     |       |  |
#    +-----ooooooooooooo-----+ 128   C  V
#    |     o           o     |       O  I
#    |     |o         o|     |       N  E
#    |     | ooooooooo |     |       T  W
#    |     | o       o |     |       E  B
#    |     |o         o|     |       N  O
#    +-----|ooooooooooo|-----+ 256   T  X
#    |     |o    o    o|     |       |  |
#    |     | o   o   o |     |       |  |
#    |     | o   o   o |     |       |  |
#    |     |  o  o  o  |     |       |  |
#    |     |  o  o  o  |     |       |  |
#    +-----|---ooooo---|-----+ 384   -  -

def create_hbr_guide(body_ratios):
    head_width_ratio,        shoulder_width_ratio,    waist_width_ratio, \
    hip_width_ratio,         feet_width_ratio,        neck_length_ratio, \
    upper_body_length_ratio, lower_body_length_ratio, legs_length_ratio, \
        = body_ratios

    svg_content_width = 128
    svg_contents = ""

    svg_width = svg_content_width * 2
    svg_height = (1 + neck_length_ratio + upper_body_length_ratio + lower_body_length_ratio + legs_length_ratio) * svg_content_width

    def draw_lines(lines):
        svg_data = ""
        for ([x1, y1, x2, y2], mirror) in lines:
            svg_data += '<line class="secondary" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'.format(
                x1 = svg_format_float(x1), y1 = svg_format_float(y1),
                x2 = svg_format_float(x2), y2 = svg_format_float(y2),
            )
            if mirror:
                svg_data += '<line class="secondary" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'.format(
                    x1 = svg_format_float(-x1), y1 = svg_format_float(y1),
                    x2 = svg_format_float(-x2), y2 = svg_format_float(y2),
                )
        return svg_data

    # Head
    head_width, head_height = head_width_ratio * svg_content_width, svg_content_width
    eyes_width, eyes_height = 0.5, 0.25

    svg_contents += '<ellipse class="secondary" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" />'.format(
        cx = svg_format_float(head_width  * 0.0),
        cy = svg_format_float(head_height * 0.5),
        rx = svg_format_float(head_width  * 0.5),
        ry = svg_format_float(head_height * 0.5),
    )

    svg_contents += draw_lines([
        ([head_width * -0.5,               head_height * 0.5,                       head_width * 0.5,                head_height * 0.5                      ], False),
        ([head_width *  0.0,               head_height * 0.0,                       head_width * 0.0,                head_height * 1.0                      ], False),
        ([head_width * (eyes_width * 0.5), head_height * (0.5 - eyes_height * 0.5), head_width * (eyes_width * 0.5), head_height * (0.5 + eyes_height * 0.5)], True ),
    ])

    # Body
    x_shoulder = (shoulder_width_ratio * 0.5) * svg_content_width
    x_waist    = (waist_width_ratio    * 0.5) * svg_content_width
    x_hip      = (hip_width_ratio      * 0.5) * svg_content_width
    x_feet     = (feet_width_ratio     * 0.5) * svg_content_width

    x_groin    = 0

    y_shoulder = (1 + neck_length_ratio                                                                        ) * head_height
    y_waist    = (1 + neck_length_ratio + upper_body_length_ratio                                              ) * head_height
    y_hip      = (1 + neck_length_ratio + upper_body_length_ratio + lower_body_length_ratio                    ) * head_height
    y_feet     = (1 + neck_length_ratio + upper_body_length_ratio + lower_body_length_ratio + legs_length_ratio) * head_height

    svg_contents += draw_lines([
        ([-x_shoulder, y_shoulder,  x_shoulder, y_shoulder], False),
        ([-x_waist,    y_waist,     x_waist,    y_waist   ], False),
        ([-x_hip,      y_hip,       x_hip,      y_hip     ], False),
        ([-x_feet,     y_feet,      x_feet,     y_feet    ], False),
        ([ x_groin,    y_hip,       x_groin,    y_feet    ], False),
        ([ x_shoulder, y_shoulder,  x_waist,    y_waist   ], True ),
        ([ x_waist,    y_waist,     x_hip,      y_hip     ], True ),
        ([ x_hip,      y_hip,       x_feet,     y_feet    ], True ),
    ])

    return dedent("""\
        <svg width="{svg_width}" height="{svg_height}" viewBox="{svg_vbox_x} 0 {svg_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
            {svg_style}
            <g id="hbr">
                {svg_contents}
            </g>
        </svg>
    """).format(
        svg_width    = svg_format_float(svg_width),
        svg_height   = svg_format_float(svg_height),
        svg_vbox_x   = svg_format_float(-svg_width / 2),
        svg_style    = svg_style,
        svg_contents = svg_contents,
    )

for (hbr_name, body_ratios) in head_body_ratios.items():
    svg_path = "character/hbr_new/hbr-{}.svg".format(hbr_name)
    svg_document = create_hbr_guide(body_ratios)

    os.makedirs(os.path.dirname(svg_path), exist_ok = True)
    with open(svg_path, "w") as svg_file:
        svg_file.write(svg_document)

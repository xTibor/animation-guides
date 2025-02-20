#!/usr/bin/env python3

import argparse
import os
from textwrap import dedent

from svg_utils import svg_style, svg_format_float, copy_to_clipboard

################################################################################
# Constants

head_body_ratios = {
    #                   head_width_ratio
    #                   |      shoulder_width_ratio
    #                   |      |      waist_width_ratio
    #                   |      |      |      hip_width_ratio
    #                   |      |      |      |      feet_width_ratio
    #                   |      |      |      |      |      feet_separation_ratio
    #                   |      |      |      |      |      |      neck_length_ratio
    #                   |      |      |      |      |      |      |       upper_body_length_ratio
    #                   |      |      |      |      |      |      |       |        lower_body_length_ratio
    #                   |      |      |      |      |      |      |       |        |        legs_length_ratio
    #                   |      |      |      |      |      |      |       |        |        |
    "female-1:2.0-01": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  1 /  3,  1 /  3,  1 /  3],
    "female-1:2.0-02": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  1 /  4,  1 /  4,  1 /  2],
    "female-1:2.5-01": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  1 /  2,  1 /  3,  4 /  6],
    "female-1:2.5-02": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  1 /  2,  1 /  2,  1 /  2],
    "female-1:2.5-03": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  1 /  3,  1 /  3,  5 /  6],
    "female-1:3.0-01": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  1 /  2,  1 /  2,  1 /  1],
    "female-1:3.0-02": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  7 / 12,  7 / 12, 10 / 12],
    "female-1:3.0-03": [1.000, 0.600, 0.500, 0.650, 0.400, 0.000, 0.050,  2 /  3,  1 /  3,  1 /  1],
    "female-1:4.0-01": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.050,  2 /  3,  2 /  3,  5 /  3],
    "female-1:4.0-02": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.050,  5 /  6,  3 /  6,  5 /  3],
    "female-1:4.0-03": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.050,  1 /  1,  1 /  3,  5 /  3],
    "female-1:4.0-04": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.050,  1 /  1,  1 /  1,  1 /  1],
    "female-1:4.5-01": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.100,  3 /  4,  3 /  4,  2 /  1],
    "female-1:4.5-02": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.100,  1 /  1,  1 /  2,  2 /  1],
    "female-1:5.0-01": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.100,  1 /  1,  3 /  4,  9 /  4],
    "female-1:6.0-01": [1.000, 0.900, 0.800, 1.000, 0.600, 0.000, 0.100,  1 /  1,  1 /  1,  3 /  1],
    "female-1:7.0-01": [1.000, 1.000, 0.850, 1.100, 0.600, 0.000, 0.140,  4 /  3,  1 /  1, 11 /  3],
}

guide_styles = [
    "figure",
    "simple",
    "printable",
]

################################################################################
#  SVG document generator

def create_hbr_guide(body_ratios, guide_style):
    head_width_ratio,  shoulder_width_ratio,    waist_width_ratio,       \
    hip_width_ratio,   feet_width_ratio,        feet_separation_ratio,   \
    neck_length_ratio, upper_body_length_ratio, lower_body_length_ratio, \
    legs_length_ratio,                                                   \
        = body_ratios

    match guide_style:
        case "figure" | "simple":
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

            def draw_lines(lines):
                svg_data = ""
                for ([(x1, y1), (x2, y2)], mirror) in lines:
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

            svg_content_width = 128
            svg_contents = ""

            svg_width = svg_content_width * 2
            svg_height = (1 + neck_length_ratio + upper_body_length_ratio + lower_body_length_ratio + legs_length_ratio) * svg_content_width

            # Head
            head_width, head_height = head_width_ratio * svg_content_width, svg_content_width
            eyes_width, eyes_height = 0.5, 0.25

            match guide_style:
                case "figure":
                    svg_contents += '<ellipse class="secondary" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" />'.format(
                        cx = svg_format_float(head_width  * 0.0),
                        cy = svg_format_float(head_height * 0.5),
                        rx = svg_format_float(head_width  * 0.5),
                        ry = svg_format_float(head_height * 0.5),
                    )

                    svg_contents += draw_lines([
                        ([(head_width * -0.5, head_height * 0.5), (head_width * 0.5, head_height * 0.5)], False),
                        ([(head_width *  0.0, head_height * 0.0), (head_width * 0.0, head_height * 1.0)], False),
                    ])

                    svg_contents += draw_lines([
                        ([(head_width * (eyes_width * 0.5), head_height * (0.5 - eyes_height * 0.5)),
                        (head_width * (eyes_width * 0.5), head_height * (0.5 + eyes_height * 0.5))], True),
                    ])
                case "simple":
                    svg_contents += '<circle class="secondary" cx="{cx}" cy="{cy}" r="{r}" />'.format(
                        cx = svg_format_float(svg_content_width * 0.0),
                        cy = svg_format_float(svg_content_width * 0.5),
                        r  = svg_format_float(svg_content_width * 0.5),
                    )

            # Body
            x_shoulder = (shoulder_width_ratio  * 0.5) * svg_content_width
            x_waist    = (waist_width_ratio     * 0.5) * svg_content_width
            x_hip      = (hip_width_ratio       * 0.5) * svg_content_width
            x1_feet    = (feet_separation_ratio * 0.5) * svg_content_width
            x2_feet    = (feet_width_ratio      * 0.5) * svg_content_width + x1_feet
            x_groin    = 0

            y_shoulder = (1 + neck_length_ratio                                                                        ) * head_height
            y_waist    = (1 + neck_length_ratio + upper_body_length_ratio                                              ) * head_height
            y_hip      = (1 + neck_length_ratio + upper_body_length_ratio + lower_body_length_ratio                    ) * head_height
            y_feet     = (1 + neck_length_ratio + upper_body_length_ratio + lower_body_length_ratio + legs_length_ratio) * head_height

            match guide_style:
                case "figure":
                    svg_contents += draw_lines([
                        ([(-x_shoulder, y_shoulder), (x_shoulder, y_shoulder)], False),
                        ([(-x_waist,    y_waist   ), (x_waist,    y_waist   )], False),
                        ([(-x_hip,      y_hip     ), (x_hip,      y_hip     )], False),
                        ([( x_shoulder, y_shoulder), (x_waist,    y_waist   )], True ),
                        ([( x_waist,    y_waist   ), (x_hip,      y_hip     )], True ),
                        ([( x_groin,    y_hip     ), (x1_feet,    y_feet,   )], True ),
                        ([( x_hip,      y_hip     ), (x2_feet,    y_feet,   )], True ),
                        ([( x1_feet,    y_feet    ), (x2_feet,    y_feet    )], True ),
                    ])
                case "simple":
                    svg_contents += draw_lines([
                        ([(-svg_content_width * 0.5, y_shoulder), (svg_content_width * 0.5, y_shoulder)], False),
                        ([(-svg_content_width * 0.5, y_waist   ), (svg_content_width * 0.5, y_waist   )], False),
                        ([(-svg_content_width * 0.5, y_hip     ), (svg_content_width * 0.5, y_hip     )], False),
                        ([(-svg_content_width * 0.5, y_feet    ), (svg_content_width * 0.5, y_feet    )], False),
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

        case "printable":
            svg_contents = ""

            total_height   = 1 + upper_body_length_ratio + lower_body_length_ratio + legs_length_ratio
            line_positions = [
                (1                                                     ) / total_height,
                (1 +  upper_body_length_ratio                          ) / total_height,
                (1 +  upper_body_length_ratio + lower_body_length_ratio) / total_height,
            ]

            for t in line_positions:
                svg_contents += '<line class="primary" x1="0" y1="576" x2="576" y2="{y}" />'.format(
                    y = svg_format_float(t * 576),
                )

            for t in map(lambda line: line / 12, range(1, 12)):
                svg_contents += '<line class="secondary" x1="{x}" y1="{y}" x2="{x}" y2="576" />'.format(
                    x = svg_format_float(t * 576),
                    y = svg_format_float(576 - (t * 576)),
                )

            return dedent("""\
                <svg width="576" height="576" viewBox="0 0 576 576" xmlns="http://www.w3.org/2000/svg">
                    {svg_style}
                    <g id="hbr">
                        <polygon class="primary" points="0,576 576,576 576,0" />
                        {svg_contents}
                    </g>
                </svg>
            """).format(
                svg_style    = svg_style,
                svg_contents = svg_contents,
            )

################################################################################
# Main

parser = argparse.ArgumentParser()
parser.add_argument("--command", type = str,                                                           )
parser.add_argument("--target",  type = str,   default = "stdout"                                      )
parser.add_argument("--style",   type = str,   default = "figure"                                      )
parser.add_argument("--params",  type = float, default = list(head_body_ratios.values())[0], nargs = 10)

args = parser.parse_args()

match args.command:
    case "create-svg":
        svg_document = create_hbr_guide(args.params, args.style)
        match args.target:
            case "stdout":
                print(svg_document)
            case "clipboard":
                copy_to_clipboard(svg_document, "image/svg+xml")

    case "query-guide-styles":
        for guide_style in guide_styles:
            print(guide_style)

    case None:
        for guide_style in guide_styles:
            for (hbr_name, body_ratios) in head_body_ratios.items():
                svg_path = "character/hbr/{}/hbr-{}.svg".format(guide_style, hbr_name)
                svg_document = create_hbr_guide(body_ratios, guide_style)

                os.makedirs(os.path.dirname(svg_path), exist_ok = True)
                with open(svg_path, "w") as svg_file:
                    svg_file.write(svg_document)

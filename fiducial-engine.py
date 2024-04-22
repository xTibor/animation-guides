#!/usr/bin/env python3

import argparse
import os
from textwrap import dedent

from svg_utils import svg_to_clipboard

################################################################################
# Constants

fiducial_styles = [
    "xt16bfm",
]

################################################################################
#  SVG document generator

def create_fiducial(fiducial_value, fiducial_style):
    match fiducial_style:
        case "xt16bfm":
            svg_fiducial_style = """
                <style>
                .background {
                    fill: #FFFFFF;
                    stroke: #FFFFFF;
                    stroke-width: 1px;
                    stroke-linejoin: round;
                }

                .foreground {
                    fill: #000000;
                    stroke: #000000;
                    stroke-width: 1px;
                    stroke-linejoin: round;
                }
                </style>
            """

            svg_contents = ""

            tile_size = 144
            tile_positions = [
                [ 72,  72], [216,  72], [360,  72], [360, 216],
                [360, 360], [216, 360], [ 72, 360], [ 72, 216],
            ]

            for tile_position_index in range(0, 8):
                [tile_x, tile_y] = tile_positions[tile_position_index]
                tile_index = (fiducial_value >> (tile_position_index * 2)) & 0b11

                match tile_index:
                    case 0:
                        svg_contents += '<polygon class="foreground" points="{},{} {},{} {},{}" />'.format(
                            tile_x,             tile_y,
                            tile_x + tile_size, tile_y,
                            tile_x,             tile_y + tile_size,
                        )
                    case 1:
                        svg_contents += '<polygon class="foreground" points="{},{} {},{} {},{}" />'.format(
                            tile_x,             tile_y,
                            tile_x + tile_size, tile_y,
                            tile_x + tile_size, tile_y + tile_size,
                        )
                    case 2:
                        svg_contents += '<polygon class="foreground" points="{},{} {},{} {},{}" />'.format(
                            tile_x + tile_size, tile_y,
                            tile_x + tile_size, tile_y + tile_size,
                            tile_x,             tile_y + tile_size,
                        )
                    case 3:
                        svg_contents += '<polygon class="foreground" points="{},{} {},{} {},{}" />'.format(
                            tile_x,             tile_y,
                            tile_x + tile_size, tile_y + tile_size,
                            tile_x,             tile_y + tile_size ,
                        )

            return dedent("""\
                <svg width="576" height="576" viewBox="0 0 576 576" xmlns="http://www.w3.org/2000/svg">
                    {}
                    <g id="fiducial_{}_{}">
                        <rect class="background" x="0" y="0" width="576" height="576" />
                        <rect class="foreground" x="36" y="36" width="504" height="504" />
                        <rect class="background" x="54" y="54" width="468" height="468" />
                        <rect class="foreground" x="234" y="234" width="108" height="108" />
                        <rect class="background" x="252" y="252" width="72" height="72" />
                        <rect class="foreground" x="270" y="270" width="36" height="36" />
                        {}
                    </g>
                </svg>
            """).format(
                svg_fiducial_style,
                fiducial_style,
                fiducial_value,
                svg_contents,
            )

################################################################################
# Main

parser = argparse.ArgumentParser()
parser.add_argument("--command", type = str,                    )
parser.add_argument("--target",  type = str, default = "stdout" )
parser.add_argument("--style",   type = str, default = "xt16bfm")
parser.add_argument("--value",   type = int, default = 0        )

args = parser.parse_args()

match args.command:
    case "create-svg":
        svg_document = create_fiducial(args.value, args.style)
        match args.target:
            case "stdout":
                print(svg_document)
            case "clipboard":
                svg_to_clipboard(svg_document)

    case "query-fiducial-styles":
        for fiducial_style in fiducial_styles:
            print(fiducial_style)

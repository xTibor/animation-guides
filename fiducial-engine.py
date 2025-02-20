#!/usr/bin/env python3

import argparse
import os
from textwrap import dedent

from svg_utils import copy_to_clipboard

################################################################################
# Constants

svg_style = """
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

################################################################################
#  Fiducial - xt16bfm

def xt16bfm_canonicalize(value):
    def rotate(value):
        result = 0
        for [index_a, index_b] in enumerate([6, 7, 0, 1, 2, 3, 4, 5]):
            tmp = (value >> (index_b * 2)) & 0b11
            tmp = (tmp + 1) & 0b11
            result |= (tmp << (index_a * 2))
        return result

    def mirror(value):
        result = 0
        for [index_a, index_b] in enumerate([2, 1, 0, 7, 6, 5, 4, 3]):
            tmp = (value >> (index_b * 2)) & 0b11
            tmp = tmp ^ 0b01
            result |= (tmp << (index_a * 2))
        return result

    return min([
        value,
        rotate(value),
        rotate(rotate(value)),
        rotate(rotate(rotate(value))),
        mirror(value),
        rotate(mirror(value)),
        rotate(rotate(mirror(value))),
        rotate(rotate(rotate(mirror(value)))),
    ])

def xt16bfm_create_svg(fiducial_value):
    svg_contents = ""

    if fiducial_value == xt16bfm_canonicalize(fiducial_value):
        for tile_position_index in range(0, 8):
            tile_index = (fiducial_value >> (tile_position_index * 2)) & 0b11

            [tile_u, tile_v] = [
                [0, 0], [1, 0], [2, 0], [2, 1],
                [2, 2], [1, 2], [0, 2], [0, 1],
            ][tile_position_index]

            tile_size = 144

            tile_x0 = 72 + (tile_u * tile_size)
            tile_y0 = 72 + (tile_v * tile_size)

            tile_x1 = tile_x0 + tile_size
            tile_y1 = tile_y0 + tile_size

            svg_contents += '<polygon class="foreground" points="{},{} {},{} {},{}" />'.format(
                *[
                    [tile_x0, tile_y0, tile_x1, tile_y0, tile_x0, tile_y1],
                    [tile_x0, tile_y0, tile_x1, tile_y0, tile_x1, tile_y1],
                    [tile_x1, tile_y0, tile_x1, tile_y1, tile_x0, tile_y1],
                    [tile_x0, tile_y0, tile_x1, tile_y1, tile_x0, tile_y1],
                ][tile_index]
            )

    return dedent("""\
        <svg width="576" height="576" viewBox="0 0 576 576" xmlns="http://www.w3.org/2000/svg">
            {}
            <g id="fiducial_xt16bfm_{}">
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
        svg_style,
        fiducial_value,
        svg_contents,
    )

################################################################################
#  Fiducial styles

fiducial_styles = {
    "xt16bfm": xt16bfm_create_svg,
}

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
        svg_document = fiducial_styles[args.style](args.value)
        match args.target:
            case "stdout":
                print(svg_document)
            case "clipboard":
                copy_to_clipboard(svg_document, "image/svg+xml")

    case "query-fiducial-styles":
        for (fiducial_style, fiducial_callback) in fiducial_styles.items():
            print(fiducial_style)

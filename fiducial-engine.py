#!/usr/bin/env python3

import argparse
import os
from textwrap import dedent

from svg_utils import svg_style, svg_format_float, svg_to_clipboard

################################################################################
# Constants

fiducial_styles = [
    "xt16bfm",
]

################################################################################
#  SVG document generator

def create_fiducial(fiducial_value, fiducial_style):
    pass

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

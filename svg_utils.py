#!/usr/bin/env python3

svg_style = """
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

def svg_format_float(number):
    return "{:.3f}".format(number).rstrip("0").rstrip(".")

def svg_to_clipboard(svg_document):
    import subprocess
    subprocess.run(
        ["xclip", "-selection", "clipboard", "-t", "image/svg+xml"],
        encoding = "utf-8",
        input = svg_document,
    )

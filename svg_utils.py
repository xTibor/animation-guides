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

def format_float(number, precision = 3):
    return "{0:.{1}f}".format(number, precision).rstrip("0").rstrip(".")

def copy_to_clipboard(clipboard_data, mime_type):
    import subprocess
    subprocess.run(
        ["wl-copy", "--type", mime_type],
        encoding = "utf-8",
        input = clipboard_data,
    )

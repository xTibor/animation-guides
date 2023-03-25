#!/usr/bin/env python3

import argparse
import os
import subprocess
from math import sin, cos, radians, pi
from textwrap import dedent

################################################################################
# Easing functions

def concat(easing_function_a, easing_function_b):
    def inner(t):
        if t < 0.5:
            return 0.0 + easing_function_a(t * 2.0 - 0.0) / 2.0
        else:
            return 0.5 + easing_function_b(t * 2.0 - 1.0) / 2.0
    return inner

def first_half(easing_function):
    def inner(t):
        return easing_function(t / 2.0 + 0.0) * 2.0 - 0.0
    return inner

def second_half(easing_function):
    def inner(t):
        return easing_function(t / 2.0 + 0.5) * 2.0 - 1.0
    return inner

def ease_in(factor):
    return lambda t: pow(t, factor)

def ease_out(factor):
    return lambda t: 1.0 - pow(1.0 - t, factor)

def ease_inout_linear():
    return lambda t: t

def ease_inout_smoothstep():
    return lambda t: t * t * (3.0 - 2.0 * t)

def ease_inout_smootherstep():
    return lambda t: t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

def ease_inout_cosine():
    return lambda t: (1.0 - cos(t * pi)) / 2.0

easing_functions = {
    "ease-inout-linear":       ease_inout_linear(),
    "ease-inout-smoothstep":   ease_inout_smoothstep(),
    "ease-inout-smootherstep": ease_inout_smootherstep(),

    "ease-in-pow2":            ease_in(2.0),
    "ease-out-pow2":           ease_out(2.0),
    "ease-inout-pow2":         concat(ease_in(2.0), ease_out(2.0)),

    "ease-in-pow3":            ease_in(3.0),
    "ease-out-pow3":           ease_out(3.0),
    "ease-inout-pow3":         concat(ease_in(3.0), ease_out(3.0)),

    "ease-in-pow4":            ease_in(4.0),
    "ease-out-pow4":           ease_out(4.0),
    "ease-inout-pow4":         concat(ease_in(4.0), ease_out(4.0)),

    "ease-in-pow5":            ease_in(5.0),
    "ease-out-pow5":           ease_out(5.0),
    "ease-inout-pow5":         concat(ease_in(5.0), ease_out(5.0)),

    "ease-in-cosine":          first_half(ease_inout_cosine()),
    "ease-out-cosine":         second_half(ease_inout_cosine()),
    "ease-inout-cosine":       ease_inout_cosine(),
}

################################################################################
# SVG document generators

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

def create_svg_ruler_straight(easing_function, **kwargs):
    ruler_frames = kwargs["ruler_frames"]

    svg_contents = ""
    for t in map(lambda line: line / (ruler_frames - 1), range(0, ruler_frames)):
        svg_contents += '<line class="primary" x1="{x}" y1="0" x2="{x}" y2="24" />'.format(
            x = svg_format_float(easing_function(t) * 576),
        )

    return dedent("""\
        <svg width="576" height="24" viewBox="0 0 576 24" xmlns="http://www.w3.org/2000/svg">
            {}
            <g id="ruler">
                <line class="primary" x1="0" y1="12" x2="576" y2="12" />
                {}
            </g>
        </svg>
    """).format(
        svg_style,
        svg_contents,
    )

def create_svg_ruler_triangle(easing_function, **kwargs):
    ruler_frames = kwargs["ruler_frames"]

    svg_contents = ""
    for t in map(lambda line: line / (ruler_frames - 1), range(1, ruler_frames - 1)):
        svg_contents += '<line class="primary" x1="{x}" y1="0" x2="288" y2="384" />'.format(
            x = svg_format_float(easing_function(t) * 576),
        )

    for t in map(lambda line: line / 12, range(1, 12)):
        svg_contents += '<line class="secondary" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" />'.format(
            x1 = svg_format_float(t * 288),
            x2 = svg_format_float(576 - (t * 288)),
            y = svg_format_float(t * 384),
        )
    svg_contents += '<line class="secondary" x1="288" y1="0" x2="288" y2="384" />'

    return dedent("""\
        <svg width="576" height="384" viewBox="0 0 576 384" xmlns="http://www.w3.org/2000/svg">
            {}
            <g id="ruler">
                <polygon class="primary" points="0,0 576,0 288,384" />
                {}
            </g>
        </svg>
    """).format(
        svg_style,
        svg_contents,
    )

def create_svg_ruler_radial(easing_function, **kwargs):
    ruler_frames = kwargs["ruler_frames"]
    ruler_degrees = kwargs["ruler_degrees"]

    ruler_inner_radius = 22.5
    ruler_outer_radius = 288

    svg_contents = ""

    def circle_arc_point(arc_degrees, arc_radius):
        return (
            288 + cos(radians(arc_degrees)) * arc_radius,
            288 - sin(radians(arc_degrees)) * arc_radius,
        )

    def draw_circle_arc(style_class, arc_radius):
        arc_resolution = 9

        x, y = circle_arc_point(0, arc_radius)
        arc_path_data = "M{x} {y}".format(
            x = svg_format_float(x),
            y = svg_format_float(y),
        )

        for l in range(0, arc_resolution):
            x, y = circle_arc_point(l / (arc_resolution - 1) * ruler_degrees, arc_radius)
            arc_path_data += " A {arc_radius} {arc_radius} 0 0 0 {x} {y}".format(
                arc_radius = svg_format_float(arc_radius),
                x = svg_format_float(x),
                y = svg_format_float(y),
            )

        return '<path class="{}" d="{}" />'.format(style_class, arc_path_data)

    def draw_radius(style_class, arc_degrees):
        x1, y1 = circle_arc_point(arc_degrees, ruler_inner_radius)
        x2, y2 = circle_arc_point(arc_degrees, ruler_outer_radius)
        return '<line class="{}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" />'.format(
            style_class,
            x1 = svg_format_float(x1),
            y1 = svg_format_float(y1),
            x2 = svg_format_float(x2),
            y2 = svg_format_float(y2),
        )

    svg_contents += draw_circle_arc("primary", ruler_outer_radius)
    for l in range(1, 6):
        svg_contents += draw_circle_arc("secondary", (l / 6) * ruler_outer_radius)

    for l in range(0, ruler_frames):
        svg_contents += draw_radius("primary", easing_function(l / (ruler_frames - 1)) * ruler_degrees)

    return dedent("""\
        <svg width="576" height="576" viewBox="0 0 576 576" xmlns="http://www.w3.org/2000/svg">
            {}
            <g id="ruler">
                <circle class="secondary" cx="288" cy="288" r="288" />
                <circle class="primary" cx="288" cy="288" r="9" />
                <circle class="primary" cx="288" cy="288" r="22.5" />
                <line class="primary" x1="270" y1="288" x2="306" y2="288" />
                <line class="primary" x1="288" y1="270" x2="288" y2="306" />
                {}
            </g>
        </svg>
    """).format(
        svg_style,
        svg_contents,
    )

def create_svg_function_graph(easing_function, **kwargs):
    polyline_resolution = 64

    polyline_data = ""
    for t in map(lambda p: p / polyline_resolution, range(0, polyline_resolution + 1)):
        polyline_data += "{x},{y} ".format(
            x = svg_format_float(t * 576),
            y = svg_format_float(576 - easing_function(t) * 576),
        )

    svg_contents = '<polyline class="primary" points="{}" />'.format(polyline_data)

    return dedent("""\
        <svg width="576" height="576" viewBox="0 0 576 576" xmlns="http://www.w3.org/2000/svg">
            {}
            <g id="ruler">
                <line class="secondary" x1="0" y1="0" x2="0" y2="576" />
                <line class="secondary" x1="288" y1="0" x2="288" y2="576" />
                <line class="secondary" x1="576" y1="0" x2="576" y2="576" />
                <line class="secondary" x1="0" y1="0" x2="576" y2="0" />
                <line class="secondary" x1="0" y1="288" x2="576" y2="288" />
                <line class="secondary" x1="0" y1="576" x2="576" y2="576" />
                {}
            </g>
        </svg>
    """).format(
        svg_style,
        svg_contents,
    )

create_svg_constructors = {
    "straight":       create_svg_ruler_straight,
    "triangle":       create_svg_ruler_triangle,
    "radial":         create_svg_ruler_radial,
    "function-graph": create_svg_function_graph,
}

################################################################################
# SVG file writers

def write_svg_ruler_straight(easing_function_name, easing_function, ruler_frames):
    svg_path = "rulers/inbetweening/straight/{}/ruler-inbetweening-straight-{}-{}f.svg".format(
        easing_function_name,
        easing_function_name,
        ruler_frames,
    )

    svg_document = create_svg_ruler_straight(
        easing_function,
        ruler_frames = ruler_frames,
    )

    os.makedirs(os.path.dirname(svg_path), exist_ok = True)
    with open(svg_path, "w") as svg_file:
        svg_file.write(svg_document)

def write_svg_ruler_triangle(easing_function_name, easing_function, ruler_frames):
    svg_path = "rulers/inbetweening/triangle/{}/ruler-inbetweening-triangle-{}-{}f.svg".format(
        easing_function_name,
        easing_function_name,
        ruler_frames,
    )

    svg_document = create_svg_ruler_triangle(
        easing_function,
        ruler_frames = ruler_frames,
    )

    os.makedirs(os.path.dirname(svg_path), exist_ok = True)
    with open(svg_path, "w") as svg_file:
        svg_file.write(svg_document)

def write_svg_ruler_radial(easing_function_name, easing_function, ruler_frames, ruler_degrees):
    svg_path = "rulers/inbetweening/radial/{}/{}deg/ruler-inbetweening-radial-{}-{}deg-{}f.svg".format(
        easing_function_name,
        ruler_degrees,
        easing_function_name,
        ruler_degrees,
        ruler_frames,
    )

    svg_document = create_svg_ruler_radial(
        easing_function,
        ruler_frames = ruler_frames,
        ruler_degrees = ruler_degrees,
    )

    os.makedirs(os.path.dirname(svg_path), exist_ok = True)
    with open(svg_path, "w") as svg_file:
        svg_file.write(svg_document)

def write_svg_function_graph(easing_function_name, easing_function):
    svg_path = "rulers/inbetweening/function-graphs/{}.svg".format(
        easing_function_name,
    )

    svg_document = create_svg_function_graph(
        easing_function,
    )

    os.makedirs(os.path.dirname(svg_path), exist_ok = True)
    with open(svg_path, "w") as svg_file:
        svg_file.write(svg_document)

################################################################################
# Main

parser = argparse.ArgumentParser()
parser.add_argument("--command",              type = str,                              )
parser.add_argument("--target",               type = str,   default = "stdout"         )
parser.add_argument("--easing-function-name", type = str,   default = "ease-inout-pow2")
parser.add_argument("--ruler-name",           type = str,   default = "straight"       )
parser.add_argument("--ruler-frames",         type = int,   default = "8"              )
parser.add_argument("--ruler-degrees",        type = float, default = "360"            )

args = parser.parse_args()

match args.command:
    case "create-svg":
        svg_document = create_svg_constructors[args.ruler_name](
            easing_function = easing_functions[args.easing_function_name],
            ruler_frames = args.ruler_frames,
            ruler_degrees = args.ruler_degrees,
        )
        match args.target:
            case "stdout":
                print(svg_document)
            case "clipboard":
                subprocess.run(
                    ["xclip", "-selection", "clipboard", "-t", "image/svg+xml"],
                    encoding = "utf-8",
                    input = svg_document,
                )

    case "query-easing-function-names":
        for (easing_function_name, easing_function) in easing_functions.items():
            print(easing_function_name)

    case "query-ruler-names":
        for (ruler_name, ruler_constructor) in create_svg_constructors.items():
            print(ruler_name)

    case None:
        for (easing_function_name, easing_function) in easing_functions.items():
            for ruler_frames in range(4, 11):
                write_svg_ruler_straight(easing_function_name, easing_function, ruler_frames)

        for (easing_function_name, easing_function) in easing_functions.items():
            for ruler_frames in range(4, 11):
                write_svg_ruler_triangle(easing_function_name, easing_function, ruler_frames)

        for (easing_function_name, easing_function) in easing_functions.items():
            for ruler_frames in range(4, 11):
                for ruler_degrees in [90, 120, 180, 240, 270, 360]:
                    write_svg_ruler_radial(easing_function_name, easing_function, ruler_frames, ruler_degrees)

        for (easing_function_name, easing_function) in easing_functions.items():
            write_svg_function_graph(easing_function_name, easing_function)

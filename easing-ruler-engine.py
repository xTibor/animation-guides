#!/usr/bin/env python3

def compose(easing_function_a, easing_function_b):
    def composed(t):
        if t < 0.5:
            return 0.0 + easing_function_a(t * 2.0 - 0.0) / 2.0
        else:
            return 0.5 + easing_function_b(t * 2.0 - 1.0) / 2.0
    return composed

def ease_in(factor):
    return lambda t: pow(t, factor)

def ease_out(factor):
    return lambda t: 1.0 - pow(1.0 - t, factor)

easing_functions = {
    "linear":      lambda t: t,
    "smoothstep":  lambda t: t * t * (3.0 - 2.0 * t),

    "ease-in":     ease_in(2.0),
    "ease-out":    ease_out(2.0),
    "ease-in-out": compose(ease_in(2.0), ease_out(2.0)),
}

frames_range = range(4, 11)

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

import os
from math import sin, cos, radians
from textwrap import dedent

# Inbetweening ruler - straight

for (easing_function_name, easing_function) in easing_functions.items():
    os.makedirs(
        "rulers/inbetweening/straight-simple/{}".format(
            easing_function_name,
        ),
        exist_ok = True,
    )

    for ruler_frames in frames_range:
        svg_path = "rulers/inbetweening/straight-simple/{}/ruler-inbetweening-straight-simple-{}-{}f.svg".format(
            easing_function_name,
            easing_function_name,
            ruler_frames,
        )

        svg_contents = ""
        for t in map(lambda line: line / (ruler_frames - 1), range(0, ruler_frames)):
            svg_contents += '<line class="primary" x1="{x}" y1="0" x2="{x}" y2="24" />'.format(
                x = easing_function(t) * 576,
            )

        svg_document = dedent("""\
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

        with open(svg_path, "w") as svg_file:
            svg_file.write(svg_document)

# Inbetweening ruler - triangle

for (easing_function_name, easing_function) in easing_functions.items():
    os.makedirs(
        "rulers/inbetweening/straight-triangle/{}".format(
            easing_function_name,
        ),
        exist_ok = True,
    )

    for ruler_frames in frames_range:
        svg_path = "rulers/inbetweening/straight-triangle/{}/ruler-inbetweening-straight-triangle-{}-{}f.svg".format(
            easing_function_name,
            easing_function_name,
            ruler_frames,
        )

        svg_contents = ""
        for t in map(lambda line: line / (ruler_frames - 1), range(1, ruler_frames - 1)):
            svg_contents += '<line class="primary" x1="{x}" y1="0" x2="288" y2="384" />'.format(
                x = easing_function(t) * 576,
            )

        for t in map(lambda line: line / 12, range(1, 12)):
            svg_contents += '<line class="secondary" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" />'.format(
                x1 = t * 288,
                x2 = 576 - (t * 288),
                y = t * 384,
            )
        svg_contents += '<line class="secondary" x1="288" y1="0" x2="288" y2="384" />'

        svg_document = dedent("""\
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

        with open(svg_path, "w") as svg_file:
            svg_file.write(svg_document)

# Inbetweening ruler - radial

for (easing_function_name, easing_function) in easing_functions.items():
    for ruler_degrees in [90, 120, 180, 240, 270, 360]:
        os.makedirs(
            "rulers/inbetweening/radial/{}/{}deg".format(
                easing_function_name,
                ruler_degrees
            ),
            exist_ok = True,
        )

        for ruler_frames in frames_range:
            svg_path = "rulers/inbetweening/radial/{}/{}deg/ruler-inbetweening-radial-{}-{}deg-{}f.svg".format(
                easing_function_name,
                ruler_degrees,
                easing_function_name,
                ruler_degrees,
                ruler_frames,
            )

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
                arc_path_data = "M{} {}".format(x, y)

                for l in range(0, arc_resolution):
                    x, y = circle_arc_point(l / (arc_resolution - 1) * ruler_degrees, arc_radius)
                    arc_path_data += " A {} {} 0 0 0 {} {}".format(arc_radius, arc_radius, x, y)

                return '<path class="{}" d="{}" />'.format(style_class, arc_path_data)

            def draw_radius(style_class, arc_degrees):
                x1, y1 = circle_arc_point(arc_degrees, ruler_inner_radius)
                x2, y2 = circle_arc_point(arc_degrees, ruler_outer_radius)
                return '<line class="{}" x1="{}" y1="{}" x2="{}" y2="{}" />'.format(style_class, x1, y1, x2, y2)

            svg_contents += draw_circle_arc("primary", ruler_outer_radius)
            for l in range(1, 6):
                svg_contents += draw_circle_arc("secondary", (l / 6) * ruler_outer_radius)

            for l in range(0, ruler_frames):
                svg_contents += draw_radius("primary", easing_function(l / (ruler_frames - 1)) * ruler_degrees)

            svg_document = dedent("""\
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

            with open(svg_path, "w") as svg_file:
                svg_file.write(svg_document)

# Inbetweening function graphs

os.makedirs(
    "rulers/inbetweening/functions",
    exist_ok = True,
)
for (easing_function_name, easing_function) in easing_functions.items():
    svg_path = "rulers/inbetweening/functions/{}.svg".format(
        easing_function_name,
    )

    polyline_resolution = 64
    polyline_data = ""
    for t in map(lambda p: p / polyline_resolution, range(0, polyline_resolution + 1)):
        polyline_data += "{x},{y} ".format(
            x = t * 576,
            y = 576 - easing_function(t) * 576,
        )

    svg_contents = '<polyline class="primary" points="{}" />'.format(polyline_data)

    svg_document = dedent("""\
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

    with open(svg_path, "w") as svg_file:
        svg_file.write(svg_document)

#!/usr/bin/env python3

import argparse
from svg_utils import svg_format_float

################################################################################
# BPM calculation

standard_bpm = [
     40,  42,  44,  46,  48,  50,  52,  54,  56,  58,
     60,  63,  66,  69,  72,  76,  80,  84,  88,  92,
     96, 100, 104, 108, 112, 116, 120, 126, 132, 138,
    144, 152, 160, 168, 176, 184, 192, 200, 208, 216,
    224, 232, 240,
]

bpm_filters = {
    "standard": lambda bpm: bpm in standard_bpm,
    "round":    lambda bpm: bpm.is_integer(),
    "none":     lambda bpm: True,
}

def calculate_bpm(fps, bpm_filter):
    bpm_results = []

    for frames_per_beat in range(fps * 2, 0, -1):
        bpm = 60 * (fps / frames_per_beat)

        if bpm_filters[bpm_filter](bpm):
            bpm_results.append((bpm, frames_per_beat))

    return bpm_results

################################################################################
# Output formatters

def output_format_human(bpm_results):
    for [bpm, frames_per_beat] in bpm_results:
        print("{:>7} bpm -> {:>2} frames/beat".format(
            svg_format_float(bpm),
            frames_per_beat,
        ))

def output_format_csv(bpm_results):
    print("bpm, frames_per_beat")
    for [bpm, frames_per_beat] in bpm_results:
        print("{}, {}".format(
            bpm,
            frames_per_beat,
        ))

output_formatters = {
    "human": output_format_human,
    "csv":   output_format_csv,
}

################################################################################
# Main

parser = argparse.ArgumentParser()
parser.add_argument("--command",       type = str,                  )
parser.add_argument("--fps",           type = int, default = 24     )
parser.add_argument("--bpm-filter",    type = str, default = "round")
parser.add_argument("--output-format", type = str, default = "human")

args = parser.parse_args()

match args.command:
    case "calculate-bpm":
        bpm_results = calculate_bpm(args.fps, args.bpm_filter)
        output_formatters[args.output_format](bpm_results)

    case "query-bpm-filters":
        for (bpm_filter_name, bpm_filter) in bpm_filters.items():
            print(bpm_filter_name)

    case "query-output-formats":
        for (output_format, output_formatter) in output_formatters.items():
            print(output_format)

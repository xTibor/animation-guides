#!/usr/bin/env python3

template_engine = {
    "stamps/small-jp-en": {
        "template_prefix": "stamp",
        "template_file_names": ["horizontal", "vertical"],
        "template_field_names":         ["EN_LABEL",              "JP_LABEL"          ],
        "template_dataset": [
            ("back-bl-mask",            ["BACK BL MASK",          "ウラBLヌリ"        ]),
            ("balance-comp",            ["BALANCE COMP",          "他〜と合成"        ]),
            ("balance-do-t",            ["BALANCE DOⓉ",          "他〜を同トレス"    ]),
            ("balance-t",               ["BALANCEⓉ",             "他〜をトレス"      ]),
            ("balance",                 ["BALANCE",               "残りの部分"        ]),
            ("bl-efx-mask",             ["BL EFX MASK",           "透過光マスク"      ]),
            ("bl-efx",                  ["BL EFX",                "透過光"            ]),
            ("blink-action",            ["BLINK ACTION",          "中目パチ"          ]),
            ("brush",                   ["BRUSH",                 "ブラシ"            ]),
            ("clear",                   ["CLEAR",                 "ヌキ"              ]),
            ("clothes",                 ["CLOTHES",               "服"                ]),
            ("compound",                ["COMPOUND",              "合成"              ]),
            ("dial-com",                ["DIAL.COM",              "セリフ合成"        ]),
            ("disuse-shadow",           ["DISUSE SHADOW",         "カゲ不要"          ]),
            ("eye",                     ["EYE",                   "目"                ]),
            ("eyebrow",                 ["EYEBROW",               "眉"                ]),
            ("frame",                   ["FRAME",                 "フレーム"          ]),
            ("ground-shadow",           ["GROUND SHADOW",         "地面の影"          ]),
            ("hair",                    ["HAIR",                  "髪"                ]),
            ("half-open-eye",           ["HALF OPEN EYE",         "半分開き目"        ]),
            ("held",                    ["HELD",                  "止め"              ]),
            ("high-contrast",           ["HIGH CONTRAST",         "ハイコントラスト"  ]),
            ("kakikomi",                ["KAKIKOMI",              "〜に描き込み"      ]),
            ("lip-synch",               ["LIP SYNCH",             "セリフ"            ]),
            ("ls-action",               ["L.S.ACTION",            "中割り口パク"      ]),
            ("main-character",          ["MAIN CHARACTER",        "マインキャラクター"]),
            ("no-shadow-for-balance",   ["NO SHADOW FOR BALANCE", "他影不要"          ]),
            ("none",                    ["NONE",                  "なし"              ]),
            ("normal-color-1",          ["NORMAL COLOR",          "ノーマル"          ]),
            ("normal-color-2",          ["NORMAL COLOR",          "ノーマルカラー"    ]),
            ("one-tone-darker-1",       ["1 TONE DARKER",         "ノーマル段カゲ"    ]),
            ("one-tone-darker-2",       ["1 TONE DARKER",         "影１段落とし"      ]),
            ("one-tone-lighter",        ["1 TONE LIGHTER",        "ノーマル一段上げ"  ]),
            ("open-eye",                ["OPEN EYE",              "開きめ"            ]),
            ("open-mouth",              ["OPEN MOUTH",            "開け口"            ]),
            ("p-to-edge",               ["Ⓟ TO EDGE",            "セルバレ注意"      ]),
            ("reg-to",                  ["REG. TO",               "〜と組合せ"        ]),
            ("separate-cel",            ["SEPARATE CEL",          "別セル"            ]),
            ("shadow-1",                ["SHADOW",                "カゲ"              ]),
            ("shadow-2",                ["SHADOW",                "カゲ有り"          ]),
            ("shadow-for-only",         ["SHADOW FOR ONLY 〜",    "〜のみ影あり"      ]),
            ("shadow-two-darker",       ["SHADOW 2 DARKER",       "影２段落とし"      ]),
            ("skin",                    ["SKIN",                  "肌"                ]),
            ("slide",                   ["SLIDE",                 "スライド"          ]),
            ("sweat",                   ["SWEAT",                 "汗"                ]),
            ("tears",                   ["TEARS",                 "涙"                ]),
            ("touch",                   ["TOUCH",                 "タッチ"            ]),
            ("trace",                   ["Ⓣ",                    "トレス"            ]),
        ],
    },
    "stamps/large-jp": {
        "template_prefix": "stamp",
        "template_file_names": ["horizontal", "vertical"],
        "template_field_names":                   ["JP_LABEL",     "576"],
        "template_dataset": [
            ("confidential",                      ["社外秘",       "160"]),
            ("draft-final",                       ["決定稿",       "160"]),
            ("draft-preliminary",                 ["準備稿",       "160"]),
            ("keyframe-1",                        ["原画",         "110"]),
            ("layout-1",                          ["レイアウト",   "250"]),
            ("layout-2",                          ["原図",         "110"]),
            ("page-x",                            ["PAGE　　",     "200"]),
            ("prohibited-reproduction",           ["無断転載禁止", "310"]),
            ("revision",                          ["修正",         "110"]),
            ("revision-animation-director",       ["作監修正",     "210"]),
            ("revision-chief-animation-director", ["総作監修正",   "260"]),
            ("revision-episode-director",         ["演出修正",     "210"]),
            ("revision-series-director",          ["監督修正",     "210"]),
            ("scan-required",                     ["要SCAN",       "190"]),
            ("submitted",                         ["原図出済",     "210"]),
        ],
    }
}

for (template_base_directory, template) in template_engine.items():
    for template_file_name in template["template_file_names"]:
        template_svg_path = "{}/.templates/template-{}.svg".format(
            template_base_directory,
            template_file_name,
        )

        with open(template_svg_path, "r") as template_svg_file:
            template_svg_data = template_svg_file.read()

        for (instance_name, instance_data) in template["template_dataset"]:
            instance_svg_data = template_svg_data
            for (a, b) in zip(template["template_field_names"], instance_data):
                instance_svg_data = instance_svg_data.replace(a, b)

            instance_svg_path = "{}/{}/{}-{}.svg".format(
                template_base_directory,
                template_file_name,
                template["template_prefix"],
                instance_name
            )

            with open(instance_svg_path, "w") as instance_svg_file:
                instance_svg_file.write(instance_svg_data)

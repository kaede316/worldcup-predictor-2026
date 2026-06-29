#!/usr/bin/env python3
"""Fetch latest scores from worldcup26.ir and generate matchData.json"""
import json
import urllib.request
import sys
from datetime import datetime, timedelta
from collections import OrderedDict

EN_CN = {
    "Mexico": "墨西哥", "South Africa": "南非", "South Korea": "韩国", "Czech Republic": "捷克",
    "Canada": "加拿大", "Bosnia and Herzegovina": "波黑", "United States": "美国", "Paraguay": "巴拉圭",
    "Qatar": "卡塔尔", "Switzerland": "瑞士", "Brazil": "巴西", "Morocco": "摩洛哥",
    "Haiti": "海地", "Scotland": "苏格兰", "Australia": "澳大利亚", "Turkey": "土耳其", "Turkiye": "土耳其",
    "Germany": "德国", "Curaçao": "库拉索", "Curacao": "库拉索", "Netherlands": "荷兰", "Japan": "日本",
    "Ivory Coast": "科特迪瓦", "Ecuador": "厄瓜多尔", "Sweden": "瑞典", "Tunisia": "突尼斯",
    "Spain": "西班牙", "Cape Verde": "佛得角", "Belgium": "比利时", "Egypt": "埃及",
    "Saudi Arabia": "沙特阿拉伯", "Uruguay": "乌拉圭", "Iran": "伊朗", "New Zealand": "新西兰",
    "France": "法国", "Senegal": "塞内加尔", "Iraq": "伊拉克", "Norway": "挪威",
    "Argentina": "阿根廷", "Algeria": "阿尔及利亚", "Austria": "奥地利", "Jordan": "约旦",
    "Portugal": "葡萄牙", "DR Congo": "刚果(金)", "Democratic Republic of the Congo": "刚果(金)",
    "England": "英格兰", "Croatia": "克罗地亚", "Ghana": "加纳", "Panama": "巴拿马",
    "Uzbekistan": "乌兹别克斯坦", "Colombia": "哥伦比亚",
}

CN_CODE = {
    "墨西哥": "MEX", "南非": "RSA", "韩国": "KOR", "捷克": "CZE", "加拿大": "CAN", "波黑": "BIH",
    "美国": "USA", "巴拉圭": "PAR", "卡塔尔": "QAT", "瑞士": "SUI", "巴西": "BRA", "摩洛哥": "MAR",
    "海地": "HAI", "苏格兰": "SCO", "澳大利亚": "AUS", "土耳其": "TUR", "德国": "GER", "库拉索": "CUW",
    "荷兰": "NED", "日本": "JPN", "科特迪瓦": "CIV", "厄瓜多尔": "ECU", "瑞典": "SWE", "突尼斯": "TUN",
    "西班牙": "ESP", "佛得角": "CPV", "比利时": "BEL", "埃及": "EGY", "沙特阿拉伯": "KSA", "乌拉圭": "URU",
    "伊朗": "IRN", "新西兰": "NZL", "法国": "FRA", "塞内加尔": "SEN", "伊拉克": "IRQ", "挪威": "NOR",
    "阿根廷": "ARG", "阿尔及利亚": "ALG", "奥地利": "AUT", "约旦": "JOR", "葡萄牙": "POR", "刚果(金)": "COD",
    "英格兰": "ENG", "克罗地亚": "CRO", "加纳": "GHA", "巴拿马": "PAN", "乌兹别克斯坦": "UZB", "哥伦比亚": "COL",
}

STADIUMS = {
    "1": "墨西哥城阿兹特克体育场", "2": "瓜达拉哈拉体育场", "3": "多伦多体育场",
    "4": "洛杉矶SoFi体育场", "5": "圣克拉拉体育场", "6": "新泽西体育场", "7": "福克斯堡体育场",
    "8": "温哥华体育场", "9": "休斯顿体育场", "10": "达拉斯体育场", "11": "费城体育场",
    "12": "蒙特雷体育场", "13": "亚特兰大体育场", "14": "西雅图体育场", "15": "迈阿密体育场", "16": "堪萨斯城体育场",
}

WEEKDAYS = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]


def _get_flag(cn_name):
    flags = {
        "墨西哥": "🇲🇽", "南非": "🇿🇦", "韩国": "🇰🇷", "捷克": "🇨🇿", "加拿大": "🇨🇦", "波黑": "🇧🇦",
        "美国": "🇺🇸", "巴拉圭": "🇵🇾", "卡塔尔": "🇶🇦", "瑞士": "🇨🇭", "巴西": "🇧🇷", "摩洛哥": "🇲🇦",
        "海地": "🇭🇹", "澳大利亚": "🇦🇺", "土耳其": "🇹🇷", "德国": "🇩🇪", "库拉索": "🇨🇼",
        "荷兰": "🇳🇱", "日本": "🇯🇵", "科特迪瓦": "🇨🇮", "厄瓜多尔": "🇪🇨", "瑞典": "🇸🇪", "突尼斯": "🇹🇳",
        "西班牙": "🇪🇸", "佛得角": "🇨🇻", "比利时": "🇧🇪", "埃及": "🇪🇬", "沙特阿拉伯": "🇸🇦", "乌拉圭": "🇺🇾",
        "伊朗": "🇮🇷", "新西兰": "🇳🇿", "法国": "🇫🇷", "塞内加尔": "🇸🇳", "伊拉克": "🇮🇶", "挪威": "🇳🇴",
        "阿根廷": "🇦🇷", "阿尔及利亚": "🇩🇿", "奥地利": "🇦🇹", "约旦": "🇯🇴", "葡萄牙": "🇵🇹", "刚果(金)": "🇨🇩",
        "克罗地亚": "🇭🇷", "加纳": "🇬🇭", "巴拿马": "🇵🇦", "乌兹别克斯坦": "🇺🇿", "哥伦比亚": "🇨🇴",
        "苏格兰": "🏴", "英格兰": "🏴",
    }
    return flags.get(cn_name, "")


def _get_stage_label(g):
    t = g.get("type", "")
    if t == "group":
        return g.get("group", "") + "组"
    labels = {"r32": "1/16决赛", "r16": "1/8决赛", "qf": "1/4决赛", "sf": "半决赛", "final": "决赛"}
    return labels.get(t, t)


def main():
    req = urllib.request.Request("https://worldcup26.ir/get/games", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        api_data = json.loads(resp.read().decode("utf-8"))

    games = sorted(api_data["games"], key=lambda g: g["local_date"])
    match_data = OrderedDict()

    for g in games:
        dt_cst = datetime.strptime(g["local_date"], "%m/%d/%Y %H:%M")
        dt_bj = dt_cst + timedelta(hours=14)
        bj_date = dt_bj.strftime("%Y-%m-%d")
        bj_time = dt_bj.strftime("%H:%M")

        home_cn = EN_CN.get(g.get("home_team_name_en", "").strip(), g.get("home_team_name_en", "TBD"))
        away_cn = EN_CN.get(g.get("away_team_name_en", "").strip(), g.get("away_team_name_en", "TBD"))

        finished = g.get("finished") == "TRUE"
        elapsed = g.get("time_elapsed", "")
        is_live = not finished and elapsed not in ("", None, "finished", "notstarted")
        status = "done" if finished else ("live" if is_live else "upcoming")

        match = {
            "time": bj_time,
            "stadium": STADIUMS.get(g.get("stadium_id", ""), "未知球场"),
            "group": _get_stage_label(g),
            "home": {"name": home_cn, "flag": _get_flag(home_cn), "code": CN_CODE.get(home_cn, "")},
            "away": {"name": away_cn, "flag": _get_flag(away_cn), "code": CN_CODE.get(away_cn, "")},
            "status": status,
        }

        if finished and g.get("home_score") is not None:
            match["realScore"] = f"{g['home_score']} - {g['away_score']}"

        if bj_date not in match_data:
            match_data[bj_date] = {"matches": []}
        match_data[bj_date]["matches"].append(match)

    match_data = OrderedDict(sorted(match_data.items()))

    for d in match_data:
        day = match_data[d]
        day["matches"].sort(key=lambda m: m["time"])
        dt = datetime.strptime(d, "%Y-%m-%d")
        day["date"] = f"{dt.year}年{dt.month}月{dt.day}日 {WEEKDAYS[dt.weekday()]}"
        if d <= "2026-06-18":
            day["stage"] = "小组赛第1轮"
        elif d <= "2026-06-24":
            day["stage"] = "小组赛第2轮"
        elif d <= "2026-06-28":
            day["stage"] = "小组赛第3轮"
        elif d <= "2026-07-06":
            day["stage"] = "1/16决赛"
        elif d <= "2026-07-12":
            day["stage"] = "1/8决赛"
        elif d <= "2026-07-16":
            day["stage"] = "1/4决赛"
        elif d <= "2026-07-18":
            day["stage"] = "半决赛"
        else:
            day["stage"] = "决赛"

    with open("matchData.json", "w", encoding="utf-8") as f:
        json.dump(match_data, f, ensure_ascii=False, indent=2)

    total = sum(len(d["matches"]) for d in match_data.values())
    done = sum(1 for d in match_data.values() for m in d["matches"] if m["status"] == "done")
    live = sum(1 for d in match_data.values() for m in d["matches"] if m["status"] == "live")
    print(f"Updated matchData.json: {total} matches, {done} done, {live} live")


if __name__ == "__main__":
    main()

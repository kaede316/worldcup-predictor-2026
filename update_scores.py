#!/usr/bin/env python3
"""Fetch latest scores from worldcup26.ir and generate matchData.json"""
import json, urllib.request, sys
from datetime import datetime, timedelta
from collections import OrderedDict

EN_CN = {
  "Mexico": "\u58a8\u897f\u54e5",
  "South Africa": "\u5357\u975e",
  "South Korea": "\u97e9\u56fd",
  "Czech Republic": "\u6377\u514b",
  "Canada": "\u52a0\u62ff\u5927",
  "Bosnia and Herzegovina": "\u6ce2\u9ed1",
  "United States": "\u7f8e\u56fd",
  "Paraguay": "\u5df4\u62c9\u572d",
  "Qatar": "\u5361\u5854\u5c14",
  "Switzerland": "\u745e\u58eb",
  "Brazil": "\u5df4\u897f",
  "Morocco": "\u6469\u6d1b\u54e5",
  "Haiti": "\u6d77\u5730",
  "Scotland": "\u82cf\u683c\u5170",
  "Australia": "\u6fb3\u5927\u5229\u4e9a",
  "Turkey": "\u571f\u8033\u5176",
  "Turkiye": "\u571f\u8033\u5176",
  "Germany": "\u5fb7\u56fd",
  "Cura\u00e7ao": "\u5e93\u62c9\u7d22",
  "Curacao": "\u5e93\u62c9\u7d22",
  "Netherlands": "\u8377\u5170",
  "Japan": "\u65e5\u672c",
  "Ivory Coast": "\u79d1\u7279\u8fea\u74e6",
  "Ecuador": "\u5384\u74dc\u591a\u5c14",
  "Sweden": "\u745e\u5178",
  "Tunisia": "\u7a81\u5c3c\u65af",
  "Spain": "\u897f\u73ed\u7259",
  "Cape Verde": "\u4f5b\u5f97\u89d2",
  "Belgium": "\u6bd4\u5229\u65f6",
  "Egypt": "\u57c3\u53ca",
  "Saudi Arabia": "\u6c99\u7279\u963f\u62c9\u4f2f",
  "Uruguay": "\u4e4c\u62c9\u572d",
  "Iran": "\u4f0a\u6717",
  "New Zealand": "\u65b0\u897f\u5170",
  "France": "\u6cd5\u56fd",
  "Senegal": "\u585e\u5185\u52a0\u5c14",
  "Iraq": "\u4f0a\u62c9\u514b",
  "Norway": "\u632a\u5a01",
  "Argentina": "\u963f\u6839\u5ef7",
  "Algeria": "\u963f\u5c14\u53ca\u5229\u4e9a",
  "Austria": "\u5965\u5730\u5229",
  "Jordan": "\u7ea6\u65e6",
  "Portugal": "\u8461\u8404\u7259",
  "DR Congo": "\u521a\u679c(\u91d1)",
  "Democratic Republic of the Congo": "\u521a\u679c(\u91d1)",
  "England": "\u82f1\u683c\u5170",
  "Croatia": "\u514b\u7f57\u5730\u4e9a",
  "Ghana": "\u52a0\u7eb3",
  "Panama": "\u5df4\u62ff\u9a6c",
  "Uzbekistan": "\u4e4c\u5179\u522b\u514b\u65af\u5766",
  "Colombia": "\u54e5\u4f26\u6bd4\u4e9a"
}
CN_FLAG = {
  "\u58a8\u897f\u54e5": "\ud83c\uddf2\ud83c\uddfd",
  "\u5357\u975e": "\ud83c\uddff\ud83c\udde6",
  "\u97e9\u56fd": "\ud83c\uddf0\ud83c\uddf7",
  "\u6377\u514b": "\ud83c\udde8\ud83c\uddff",
  "\u52a0\u62ff\u5927": "\ud83c\udde8\ud83c\udde6",
  "\u6ce2\u9ed1": "\ud83c\udde7\ud83c\udde6",
  "\u7f8e\u56fd": "\ud83c\uddfa\ud83c\uddf8",
  "\u5df4\u62c9\u572d": "\ud83c\uddf5\ud83c\uddfe",
  "\u5361\u5854\u5c14": "\ud83c\uddf6\ud83c\udde6",
  "\u745e\u58eb": "\ud83c\udde8\ud83c\udded",
  "\u5df4\u897f": "\ud83c\udde7\ud83c\uddf7",
  "\u6469\u6d1b\u54e5": "\ud83c\uddf2\ud83c\udde6",
  "\u6d77\u5730": "\ud83c\udded\ud83c\uddf9",
  "\u82cf\u683c\u5170": "\ud83c\udff4\udb40\udc67\udb40\udc62\udb40\udc73\udb40\udc63\udb40\udc74\udb40\udc7f",
  "\u6fb3\u5927\u5229\u4e9a": "\ud83c\udde6\ud83c\uddfa",
  "\u571f\u8033\u5176": "\ud83c\uddf9\ud83c\uddf7",
  "\u5fb7\u56fd": "\ud83c\udde9\ud83c\uddea",
  "\u5e93\u62c9\u7d22": "\ud83c\udde8\ud83c\uddfc",
  "\u8377\u5170": "\ud83c\uddf3\ud83c\uddf1",
  "\u65e5\u672c": "\ud83c\uddef\ud83c\uddf5",
  "\u79d1\u7279\u8fea\u74e6": "\ud83c\udde8\ud83c\uddee",
  "\u5384\u74dc\u591a\u5c14": "\ud83c\uddea\ud83c\udde8",
  "\u745e\u5178": "\ud83c\uddf8\ud83c\uddea",
  "\u7a81\u5c3c\u65af": "\ud83c\uddf9\ud83c\uddf3",
  "\u897f\u73ed\u7259": "\ud83c\uddea\ud83c\uddf8",
  "\u4f5b\u5f97\u89d2": "\ud83c\udde8\ud83c\uddfb",
  "\u6bd4\u5229\u65f6": "\ud83c\udde7\ud83c\uddea",
  "\u57c3\u53ca": "\ud83c\uddea\ud83c\uddec",
  "\u6c99\u7279\u963f\u62c9\u4f2f": "\ud83c\uddf8\ud83c\udde6",
  "\u4e4c\u62c9\u572d": "\ud83c\uddfa\ud83c\uddfe",
  "\u4f0a\u6717": "\ud83c\uddee\ud83c\uddf7",
  "\u65b0\u897f\u5170": "\ud83c\uddf3\ud83c\uddff",
  "\u6cd5\u56fd": "\ud83c\uddeb\ud83c\uddf7",
  "\u585e\u5185\u52a0\u5c14": "\ud83c\uddf8\ud83c\uddf3",
  "\u4f0a\u62c9\u514b": "\ud83c\uddee\ud83c\uddf6",
  "\u632a\u5a01": "\ud83c\uddf3\ud83c\uddf4",
  "\u963f\u6839\u5ef7": "\ud83c\udde6\ud83c\uddf7",
  "\u963f\u5c14\u53ca\u5229\u4e9a": "\ud83c\udde9\ud83c\uddff",
  "\u5965\u5730\u5229": "\ud83c\udde6\ud83c\uddf9",
  "\u7ea6\u65e6": "\ud83c\uddef\ud83c\uddf4",
  "\u8461\u8404\u7259": "\ud83c\uddf5\ud83c\uddf9",
  "\u521a\u679c(\u91d1)": "\ud83c\udde8\ud83c\udde9",
  "\u82f1\u683c\u5170": "\ud83c\udff4\udb40\udc67\udb40\udc62\udb40\udc65\udb40\udc6e\udb40\udc67\udb40\udc7f",
  "\u514b\u7f57\u5730\u4e9a": "\ud83c\udded\ud83c\uddf7",
  "\u52a0\u7eb3": "\ud83c\uddec\ud83c\udded",
  "\u5df4\u62ff\u9a6c": "\ud83c\uddf5\ud83c\udde6",
  "\u4e4c\u5179\u522b\u514b\u65af\u5766": "\ud83c\uddfa\ud83c\uddff",
  "\u54e5\u4f26\u6bd4\u4e9a": "\ud83c\udde8\ud83c\uddf4"
}
CN_CODE = {
  "\u58a8\u897f\u54e5": "MEX",
  "\u5357\u975e": "RSA",
  "\u97e9\u56fd": "KOR",
  "\u6377\u514b": "CZE",
  "\u52a0\u62ff\u5927": "CAN",
  "\u6ce2\u9ed1": "BIH",
  "\u7f8e\u56fd": "USA",
  "\u5df4\u62c9\u572d": "PAR",
  "\u5361\u5854\u5c14": "QAT",
  "\u745e\u58eb": "SUI",
  "\u5df4\u897f": "BRA",
  "\u6469\u6d1b\u54e5": "MAR",
  "\u6d77\u5730": "HAI",
  "\u82cf\u683c\u5170": "SCO",
  "\u6fb3\u5927\u5229\u4e9a": "AUS",
  "\u571f\u8033\u5176": "TUR",
  "\u5fb7\u56fd": "GER",
  "\u5e93\u62c9\u7d22": "CUW",
  "\u8377\u5170": "NED",
  "\u65e5\u672c": "JPN",
  "\u79d1\u7279\u8fea\u74e6": "CIV",
  "\u5384\u74dc\u591a\u5c14": "ECU",
  "\u745e\u5178": "SWE",
  "\u7a81\u5c3c\u65af": "TUN",
  "\u897f\u73ed\u7259": "ESP",
  "\u4f5b\u5f97\u89d2": "CPV",
  "\u6bd4\u5229\u65f6": "BEL",
  "\u57c3\u53ca": "EGY",
  "\u6c99\u7279\u963f\u62c9\u4f2f": "KSA",
  "\u4e4c\u62c9\u572d": "URU",
  "\u4f0a\u6717": "IRN",
  "\u65b0\u897f\u5170": "NZL",
  "\u6cd5\u56fd": "FRA",
  "\u585e\u5185\u52a0\u5c14": "SEN",
  "\u4f0a\u62c9\u514b": "IRQ",
  "\u632a\u5a01": "NOR",
  "\u963f\u6839\u5ef7": "ARG",
  "\u963f\u5c14\u53ca\u5229\u4e9a": "ALG",
  "\u5965\u5730\u5229": "AUT",
  "\u7ea6\u65e6": "JOR",
  "\u8461\u8404\u7259": "POR",
  "\u521a\u679c(\u91d1)": "COD",
  "\u82f1\u683c\u5170": "ENG",
  "\u514b\u7f57\u5730\u4e9a": "CRO",
  "\u52a0\u7eb3": "GHA",
  "\u5df4\u62ff\u9a6c": "PAN",
  "\u4e4c\u5179\u522b\u514b\u65af\u5766": "UZB",
  "\u54e5\u4f26\u6bd4\u4e9a": "COL"
}
STADIUMS = {
  "1": "\u58a8\u897f\u54e5\u57ce\u963f\u5179\u7279\u514b\u4f53\u80b2\u573a",
  "2": "\u74dc\u8fbe\u62c9\u54c8\u62c9\u4f53\u80b2\u573a",
  "3": "\u591a\u4f26\u591a\u4f53\u80b2\u573a",
  "4": "\u6d1b\u6749\u77f6SoFi\u4f53\u80b2\u573a",
  "5": "\u5723\u514b\u62c9\u62c9\u4f53\u80b2\u573a",
  "6": "\u65b0\u6cfd\u897f\u4f53\u80b2\u573a",
  "7": "\u798f\u514b\u65af\u5821\u4f53\u80b2\u573a",
  "8": "\u6e29\u54e5\u534e\u4f53\u80b2\u573a",
  "9": "\u4f11\u65af\u987f\u4f53\u80b2\u573a",
  "10": "\u8fbe\u62c9\u65af\u4f53\u80b2\u573a",
  "11": "\u8d39\u57ce\u4f53\u80b2\u573a",
  "12": "\u8499\u7279\u96f7\u4f53\u80b2\u573a",
  "13": "\u4e9a\u7279\u5170\u5927\u4f53\u80b2\u573a",
  "14": "\u897f\u96c5\u56fe\u4f53\u80b2\u573a",
  "15": "\u8fc8\u963f\u5bc6\u4f53\u80b2\u573a",
  "16": "\u582a\u8428\u65af\u57ce\u4f53\u80b2\u573a"
}
WEEKDAYS = ["\u661f\u671f\u4e00", "\u661f\u671f\u4e8c", "\u661f\u671f\u4e09", "\u661f\u671f\u56db", "\u661f\u671f\u4e94", "\u661f\u671f\u516d", "\u661f\u671f\u65e5"]
NOT_LIVE = ("", None, "finished", "notstarted")

def main():
    req = urllib.request.Request("https://worldcup26.ir/get/games", headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        api_data = json.loads(resp.read().decode("utf-8"))
    
    games = sorted([g for g in api_data["games"] if g.get("type") == "group"], key=lambda g: g["local_date"])
    match_data = OrderedDict()

    for g in games:
        dt_cst = datetime.strptime(g["local_date"], "%m/%d/%Y %H:%M")
        dt_bj = dt_cst + timedelta(hours=14)
        bj_date = dt_bj.strftime("%Y-%m-%d")
        bj_time = dt_bj.strftime("%H:%M")

        home_cn = EN_CN.get(g.get("home_team_name_en","").strip(), g.get("home_team_name_en",""))
        away_cn = EN_CN.get(g.get("away_team_name_en","").strip(), g.get("away_team_name_en",""))
        
        finished = g.get("finished") == "TRUE"
        elapsed = g.get("time_elapsed","")
        is_live = not finished and elapsed not in NOT_LIVE
        status = "done" if finished else ("live" if is_live else "upcoming")

        match = {
            "time": bj_time,
            "stadium": STADIUMS.get(g.get("stadium_id",""), "未知球场"),
            "group": g.get("group","") + "组",
            "home": {"name": home_cn, "flag": CN_FLAG.get(home_cn, ""), "code": CN_CODE.get(home_cn, "")},
            "away": {"name": away_cn, "flag": CN_FLAG.get(away_cn, ""), "code": CN_CODE.get(away_cn, "")},
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
        else:
            day["stage"] = "小组赛第3轮"

    def safe_json_dump(obj, fp):
        text = json.dumps(obj, ensure_ascii=False, indent=2)
        cleaned = []
        for c in text:
            cp = ord(c)
            if 0xD800 <= cp <= 0xDFFF:
                cleaned.append('\u' + hex(cp)[2:].zfill(4))
            else:
                cleaned.append(c)
        fp.write(''.join(cleaned))

    with open("matchData.json", 'w', encoding='utf-8') as f:
        safe_json_dump(match_data, f)

    total = sum(len(d["matches"]) for d in match_data.values())
    done = sum(1 for d in match_data.values() for m in d["matches"] if m["status"]=="done")
    live = sum(1 for d in match_data.values() for m in d["matches"] if m["status"]=="live")
    print(f"Updated matchData.json: {total} matches, {done} done, {live} live")

if __name__ == "__main__":
    main()

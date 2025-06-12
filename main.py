import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="MLB 선수 평가 도구", layout="wide")
st.title("MLB 실시간 선수 평가 도구 (API 연동)")

players = {
    "김하성": 673490,
    "오타니 쇼헤이": 660271,
    "마이크 트라웃": 545361,
    "무키 베츠": 605141,
    "후안 소토": 665742
}

player_data = []
for name, pid in players.items():
    url = f"https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(group=[hitting],type=[season])"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        info = data.get("people", [{}])[0]
        team = info.get("currentTeam", {}).get("name", "팀 정보 없음")
        stats_list = info.get("stats", [])
        if stats_list and stats_list[0].get("splits"):
            stat = stats_list[0]["splits"][0]["stat"]
            avg = stat.get("avg", "N/A")
            ops = stat.get("ops", "N/A")
            hr = stat.get("homeRuns", "N/A")
            rbi = stat.get("rbi", "N/A")
        else:
            avg = ops = hr = rbi = "데이터 없음"
        player_data.append({
            "이름": name,
            "팀": team,
            "타율": avg,
            "OPS": ops,
            "홈런": hr,
            "타점": rbi
        })
    else:
        player_data.append({
            "이름": name,
            "팀": "API 오류",
            "타율": "-",
            "OPS": "-",
            "홈런": "-",
            "타점": "-"
        })

df = pd.DataFrame(player_data)
st.dataframe(df)

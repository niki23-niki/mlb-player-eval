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
    info = res.json()["people"][0]
    team = info["currentTeam"]["name"]
    stat = info["stats"][0]["splits"][0]["stat"]
    player_data.append({
        "이름": name,
        "팀": team,
        "타율": stat.get("avg", "N/A"),
        "OPS": stat.get("ops", "N/A"),
        "홈런": stat.get("homeRuns", "N/A"),
        "타점": stat.get("rbi", "N/A")
    })

df = pd.DataFrame(player_data)
st.dataframe(df)

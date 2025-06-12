import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="MLB 선수 평가 도구", layout="wide")
st.title("📊 MLB 선수 평가 도구 (CSV 없이 안정 버전)")

players = {
    "김하성": 673490,
    "오타니 쇼헤이": 660271,
    "마이크 트라웃": 545361,
    "무키 베츠": 605141,
    "후안 소토": 665742
}

player_data = []

for name, pid in players.items():
    try:
        basic_url = f"https://statsapi.mlb.com/api/v1/people/{pid}"
        res = requests.get(basic_url)
        res.raise_for_status()
        data = res.json()
        team = data.get("people", [{}])[0].get("currentTeam", {}).get("name", "팀 정보 없음")
    except:
        team = "팀 정보 없음"

    try:
        stat_url = f"https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(group=[hitting],type=[yearByYear])"
        stat_res = requests.get(stat_url)
        stat_res.raise_for_status()
        stat_data = stat_res.json()
        splits = stat_data.get("people", [{}])[0].get("stats", [{}])[0].get("splits", [])
        mlb_splits = [s for s in splits if s.get("league", {}).get("name") == "Major League Baseball"]
        if mlb_splits:
            latest = mlb_splits[-1].get("stat", {})
            avg = latest.get("avg", "데이터 없음")
            ops = latest.get("ops", "데이터 없음")
            hr = latest.get("homeRuns", "데이터 없음")
            rbi = latest.get("rbi", "데이터 없음")
        else:
            avg = ops = hr = rbi = "데이터 없음"
    except:
        avg = ops = hr = rbi = "데이터 없음"

    player_data.append({
        "이름": name,
        "팀": team,
        "타율": avg,
        "OPS": ops,
        "홈런": hr,
        "타점": rbi
    })

df = pd.DataFrame(player_data)
st.dataframe(df)

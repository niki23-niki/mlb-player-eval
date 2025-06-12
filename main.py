import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="MLB 선수 평가 도구", layout="wide")
st.title("📊 MLB 연도별 선수 평가 도구")

players = {
    "김하성": 673490,
    "오타니 쇼헤이": 660271,
    "마이크 트라웃": 545361,
    "무키 베츠": 605141,
    "후안 소토": 665742
}

player_data = []

for name, pid in players.items():
    # 🟢 팀 정보 불러오기
    try:
        basic_url = f"https://statsapi.mlb.com/api/v1/people/{pid}"
        basic_res = requests.get(basic_url)
        basic_res.raise_for_status()
        basic_info = basic_res.json().get("people", [{}])[0]
        team = basic_info.get("currentTeam", {}).get("name", "팀 정보 없음")
    except:
        team = "팀 정보 없음"

    # 🟢 통계 정보 불러오기
    try:
        stat_url = f"https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(group=[hitting],type=[yearByYear])"
        stat_res = requests.get(stat_url)
        stat_res.raise_for_status()
        stat_info = stat_res.json().get("people", [{}])[0]
        splits = stat_info.get("stats", [{}])[0].get("splits", [])
        # 최신 MLB 시즌 찾기
        mlb_seasons = [s for s in splits if s.get("league", {}).get("name") == "Major League Baseball"]
        if mlb_seasons:
            latest = mlb_seasons[-1]
            stat = latest.get("stat", {})
            avg = stat.get("avg", "N/A")
            ops = stat.get("ops", "N/A")
            hr = stat.get("homeRuns", "N/A")
            rbi = stat.get("rbi", "N/A")
        else:
            avg = ops = hr = rbi = "데이터 없음"
    except:
        avg = ops = hr = rbi = "불러오기 실패"

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

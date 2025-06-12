import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="MLB 선수 평가 도구", layout="wide")
st.title("📊 MLB 선수 평가 도구 (아이패드용 안정 버전)")

# 선수명과 ID 직접 코드 안에 포함
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
        # 팀 정보 불러오기
        basic_url = f"https://statsapi.mlb.com/api/v1/people/{pid}"
        basic_res = requests.get(basic_url)
        team = basic_res.json().get("people", [{}])[0].get("currentTeam", {}).get("name", "팀 정보 없음")
    except:
        team = "팀 정보 없음"

    try:
        # 연도별 타격 기록 불러오기
        stat_url = f"https://statsapi.mlb.com/api/v1/people/{pid}?hydrate=stats(group=[hitting],type=[yearByYear])"
        stat_res = requests.get(stat_url)
        splits = stat_res.json().get("people", [{}])[0].get("stats", [{}])[0].get("splits", [])
        mlb_splits = [s for s in splits if s.get("league", {}).get("name") == "Major League Baseball"]
        if mlb_splits:
            latest = mlb_splits[-1].get("stat", {})
            avg = latest.get("avg", "N/A")
            ops = latest.get("ops", "N/A")
            hr = latest.get("homeRuns", "N/A")
            rbi = latest.get("rbi", "N/A")
        else:
            avg = ops = hr = rbi = "데이터 없음"
    except:
        avg = ops = hr = rbi = "API 오류"

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

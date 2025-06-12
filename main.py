import streamlit as st
import requests
import pandas as pd

st.title("MLB 선수 평가 도구")

# 예시 선수 목록 (이름: MLB 선수ID)
players = {
    "김하성": 673490,
    "오타니 쇼헤이": 660271,
    "마이크 트라웃": 545361,
    "무키 베츠": 605141,
    "후안 소토": 665742
}

def fetch_player_stats(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting],type=[yearByYear])"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        stats = data.get("people", [{}])[0].get("stats", [])
        if stats:
            splits = stats[0].get("splits", [])
            if splits:
                latest_stats = splits[-1].get("stat", {})
                return {
                    "AVG": latest_stats.get("avg", "N/A"),
                    "OPS": latest_stats.get("ops", "N/A"),
                    "HR": latest_stats.get("homeRuns", "N/A"),
                    "RBI": latest_stats.get("rbi", "N/A"),
                }
        return {"AVG": "N/A", "OPS": "N/A", "HR": "N/A", "RBI": "N/A"}
    except:
        return {"AVG": "Error", "OPS": "Error", "HR": "Error", "RBI": "Error"}

def fetch_player_team(player_id):
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        team = data.get("people", [{}])[0].get("currentTeam", {}).get("name", "팀 정보 없음")
        return team
    except:
        return "팀 정보 없음"

# 데이터 수집
player_data = []
for name, pid in players.items():
    stats = fetch_player_stats(pid)
    team = fetch_player_team(pid)
    player_data.append({
        "선수명": name,
        "팀": team,
        "타율(AVG)": stats["AVG"],
        "OPS": stats["OPS"],
        "홈런(HR)": stats["HR"],
        "타점(RBI)": stats["RBI"]
    })

df = pd.DataFrame(player_data)

st.dataframe(df)

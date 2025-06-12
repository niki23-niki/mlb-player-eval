import streamlit as st
import pandas as pd
import requests

st.title("MLB + KBO 선수 평가 도구 (베타)")

league = st.radio("리그 선택", ["MLB", "KBO"])

if league == "MLB":
    st.header("MLB 선수 데이터")
    
    players = {
        "오타니 쇼헤이": 660271,
        "마이크 트라웃": 545361,
        "후안 소토": 665742,
    }
    
    player_name = st.selectbox("선수 선택", list(players.keys()))
    player_id = players[player_name]
    
    url = f"https://statsapi.mlb.com/api/v1/people/{player_id}?hydrate=stats(group=[hitting],type=[yearByYear])"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        stats = data["people"][0]["stats"][0]["splits"][-1]["stat"]
        st.write(f"**{player_name} 최근 시즌 스탯**")
        st.write(f"타율: {stats.get('avg', 'N/A')}")
        st.write(f"홈런: {stats.get('homeRuns', 'N/A')}")
        st.write(f"타점: {stats.get('rbi', 'N/A')}")
        st.write(f"OPS: {stats.get('ops', 'N/A')}")
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류 발생: {e}")

else:
    st.header("KBO 선수 데이터 (예시)")
    # 간단 샘플 데이터 (추후 실제 데이터로 교체 예정)
    kbo_data = {
        "선수명": ["박병호", "김광현", "양의지"],
        "타율": [0.280, 0.250, 0.270],
        "홈런": [20, 5, 12],
        "타점": [70, 40, 60]
    }
    df = pd.DataFrame(kbo_data)
    st.dataframe(df)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

# 예시용 데이터와 함수들 (실제 API 연동 코드는 별도 구성 필요)

# 한글-영문 선수명 매핑 (예시)
name_map = {
    "박찬호": "ChanHo Park",
    "류현진": "HyunJin Ryu",
    "Mike Trout": "마이크 트라우트"
}

def load_player_data(league="MLB"):
    # 실제로는 API 호출 또는 데이터 불러오기
    if league == "MLB":
        data = pd.DataFrame({
            "year": [2020,2021,2022],
            "WAR": [5.2,6.1,5.9],
            "OPS": [0.920,0.950,0.940],
        })
    else:  # KBO 예시
        data = pd.DataFrame({
            "year": [2020,2021,2022],
            "WAR": [3.1,3.5,3.7],
            "OPS": [0.850,0.870,0.880],
        })
    return data

def plot_trends(df):
    fig, ax1 = plt.subplots()
    ax1.plot(df["year"], df["WAR"], color="blue", label="WAR")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("WAR", color="blue")
    ax2 = ax1.twinx()
    ax2.plot(df["year"], df["OPS"], color="red", label="OPS")
    ax2.set_ylabel("OPS", color="red")
    plt.title("WAR & OPS 추이")
    plt.tight_layout()
    st.pyplot(fig)

def plot_strikezone_heatmap():
    # 스트라이크존 3x3 매트릭스 예시 (실제 데이터로 확장 가능)
    import numpy as np
    zone = np.array([
        [0.3, 0.2, 0.1],
        [0.2, 0.4, 0.2],
        [0.1, 0.2, 0.3]
    ])
    fig, ax = plt.subplots()
    cax = ax.matshow(zone, cmap="coolwarm")
    plt.colorbar(cax)
    ax.set_xticklabels(['','좌', '중', '우'])
    ax.set_yticklabels(['','상', '중', '하'])
    plt.title("스트라이크존 코스별 강약")
    st.pyplot(fig)

st.title("MLB & KBO 선수 평가 도구")

league = st.selectbox("리그 선택", ["MLB", "KBO"])
player_name = st.text_input("선수 이름 (한글/영문 가능)")

if player_name:
    # 한글->영문 매핑 적용 (간단히)
    eng_name = name_map.get(player_name, player_name)
    st.write(f"선수명 (영문): {eng_name}")

    data = load_player_data(league)
    plot_trends(data)

    st.write("스트라이크존 강약 지도")
    plot_strikezone_heatmap()

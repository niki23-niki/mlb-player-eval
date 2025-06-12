import streamlit as st
import pandas as pd

st.set_page_config(page_title="MLB 선수 평가 도구", layout="wide")

st.title("⚾ MLB 선수 평가 도구")

# 샘플 선수 데이터 (예시용)
sample_data = {
    "이름": ["이정후", "김하성", "오타니", "린드", "최지만"],
    "소속": ["NYM", "SD", "LAA", "NPB", "KBO"],
    "OPS+": [120, 112, 180, 105, 99],
    "wOBA+": [118, 109, 185, 103, 97],
    "KBO WAR 보정": [5.2, 4.6, "-", "-", 3.1],
    "도루 성공률": [0.85, 0.91, 0.78, "-", 0.62],
    "UZR": [1.2, 3.5, -0.3, "-", 0.7]
}
df = pd.DataFrame(sample_data)

st.dataframe(df)

st.subheader("🔍 선수별 스트라이크존 강약 시각화")
selected_player = st.selectbox("선수를 선택하세요", df["이름"])

# 스트라이크존 시각화 예시
import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()
zone = np.random.rand(3, 3) * 100  # 임의의 데이터

im = ax.imshow(zone, cmap="coolwarm", vmin=0, vmax=100)
ax.set_xticks(np.arange(3))
ax.set_yticks(np.arange(3))
ax.set_xticklabels(["인코스", "중앙", "아웃코스"])
ax.set_yticklabels(["상", "중", "하"])

for i in range(3):
    for j in range(3):
        text = ax.text(j, i, f"{zone[i, j]:.1f}", ha="center", va="center", color="black")

st.pyplot(fig)

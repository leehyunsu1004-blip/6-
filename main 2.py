# ==========================================
# [PRACTICE 3]
# ==========================================
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 한글 폰트 설정 (NanumGothic) 및 마이너스 부호 깨짐 방지
plt.rc("font", family="NanumGothic")
plt.rc("axes", unicode_minus=False)

# 1. study.csv 파일 읽기
df = pd.read_csv("study.csv")

# 2. 요약 통계 출력하기
print("=== [PRACTICE 3] 데이터 요약 통계 ===")
print(df.describe())

# 3. 1행 2열 서브플롯 생성
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 4. 왼쪽: 공부시간-점수 산점도 그리기
axes[0].scatter(df["공부시간"], df["점수"], color="blue", alpha=0.7)
axes[0].set_title("공부시간과 점수의 관계")
axes[0].set_xlabel("공부시간 (시간)")
axes[0].set_ylabel("점수 (점)")
axes[0].grid(True)

# 5. 오른쪽: 점수 히스토그램 그리기
axes[1].hist(df["점수"], bins=6, color="orange", edgecolor="black")
axes[1].set_title("점수 분포")
axes[1].set_xlabel("점수 (점)")
axes[1].set_ylabel("학생 수 (명)")
axes[1].grid(True)

# 6. 레이아웃 정돈 및 그래프 출력
plt.tight_layout()
plt.show()


# ==========================================
# [READING DATA]
# ==========================================
# 1. 각 변수 간 상관계수 계산
corr_study_score = df["공부시간"].corr(df["점수"])
corr_phone_score = df["스마트폰"].corr(df["점수"])
corr_phone_study = df["스마트폰"].corr(df["공부시간"])

# 2. 상관계수 결과 출력
print("\n=== [READING DATA] 상관계수 ===")
print(f"공부시간 - 점수 상관계수: {corr_study_score:.4f}")
print(f"스마트폰시간 - 점수 상관계수: {corr_phone_score:.4f}")
print(f"스마트폰시간 - 공부시간 상관계수: {corr_phone_study:.4f}")

# 3. 1행 2열 서브플롯 생성
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# 4. 왼쪽: 공부시간 vs 점수 산점도 및 추세선
axes[0].scatter(
    df["공부시간"], df["점수"], color="blue", alpha=0.7, label="학생 데이터"
)
slope1, intercept1 = np.polyfit(df["공부시간"], df["점수"], 1)  # 1차 추세선 계수 계산
axes[0].plot(
    df["공부시간"],
    slope1 * df["공부시간"] + intercept1,
    color="red",
    linestyle="--",
    label=f"추세선 (r = {corr_study_score:.2f})",
)
axes[0].set_title("공부시간 vs 점수")
axes[0].set_xlabel("공부시간 (시간)")
axes[0].set_ylabel("점수 (점)")
axes[0].legend()
axes[0].grid(True)

# 5. 오른쪽: 스마트폰사용시간 vs 점수 산점도 및 추세선
axes[1].scatter(
    df["스마트폰"], df["점수"], color="green", alpha=0.7, label="학생 데이터"
)
slope2, intercept2 = np.polyfit(df["스마트폰"], df["점수"], 1)  # 1차 추세선 계수 계산
axes[1].plot(
    df["스마트폰"],
    slope2 * df["스마트폰"] + intercept2,
    color="red",
    linestyle="--",
    label=f"추세선 (r = {corr_phone_score:.2f})",
)
axes[1].set_title("스마트폰사용시간 vs 점수")
axes[1].set_xlabel("스마트폰 사용시간 (시간)")
axes[1].set_ylabel("점수 (점)")
axes[1].legend()
axes[1].grid(True)

# 6. 레이아웃 정돈 및 그래프 출력
plt.tight_layout()
plt.show()


# ==========================================
# [PRACTICE 4]
# (터미널 실행: streamlit run 파일명.py)
# ==========================================
import streamlit as st

# 1. 웹 앱 제목 표시
st.title("공부 습관 대시보드")

# 2. st.metric으로 학생 수, 평균 점수, 평균 공부시간을 한 줄(3열)로 표시
col1, col2, col3 = st.columns(3)
col1.metric("학생 수", f"{len(df)}명")
col2.metric("평균 점수", f"{df['점수'].mean():.1f}점")
col3.metric("평균 공부시간", f"{df['공부시간'].mean():.1f}시간")

# 3. 최소 공부시간 선택 슬라이더 생성
min_study = st.slider(
    "최소 공부시간",
    float(df["공부시간"].min()),
    float(df["공부시간"].max()),
    float(df["공부시간"].min()),
    step=0.5,
)

# 4. 슬라이더 기준 이상인 데이터 필터링
filtered_df = df[df["공부시간"] >= min_study]

# 5. Streamlit 기본 내장 차트로 공부시간-점수 산점도 출력
st.subheader("공부시간 vs 점수 산점도")
st.scatter_chart(data=filtered_df, x="공부시간", y="점수")

# 6. Streamlit 기본 내장 차트로 학생별 점수 막대 그래프 출력
st.subheader("학생별 점수 막대 그래프")
st.bar_chart(data=filtered_df, x="학생ID", y="점수")
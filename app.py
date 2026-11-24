import random
import streamlit as st

st.set_page_config(page_title="두근두근 연애 시뮬레이터", page_icon="💖")

# 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "start"
if "me" not in st.session_state:
    st.session_state.me = ""
if "target" not in st.session_state:
    st.session_state.target = ""
if "score" not in st.session_state:
    st.session_state.score = 20
if "stage" not in st.session_state:
    st.session_state.stage = 0
if "msg" not in st.session_state:
    st.session_state.msg = ""

# 8개의 상황 + 각 4개의 선택지
EVENTS = [
    {
        "title": "1단계: 개학 첫날, 옆자리 배정",
        "desc": (
            "새 학기 첫날, 짝꿍을 뽑았는데 바로 {target}의 옆자리가 되었다!"
            " 어색한 공기가 흐르는데..."
        ),
        "options": [
            (
                "'안녕! 한 학기 동안 잘 부탁해!' 밝게 먼저 인사한다.",
                10,
                "{target}도 환하게 웃으며 인사를 받아주었다! (+10)",
            ),
            (
                "주머니에 있던 사탕이나 젤리를 슬쩍 건넨다.",
                15,
                "'고마워! 나 이거 완전 좋아하는데!' 의외의 취향 저격! (+15)",
            ),
            (
                "긴장해서 아무 말도 못 하고 책상만 쳐다본다.",
                -5,
                "{target}이(가) 자기를 싫어하나 오해한 것 같다... (-5)",
            ),
            (
                "'아, 짝꿍 잘못 걸렸네'라고 장난쳤다가 분위기가 싸해진다.",
                -15,
                "첫인상이 최악이 되어버렸다... (-15)",
            ),
        ],
    },
    {
        "title": "2단계: 체육 시간, 피구 경기",
        "desc": (
            "체육 시간 피구 경기 중! 상대 팀의 엄청 빠른 공이 {target}을(를)"
            " 향해 날아온다!"
        ),
        "options": [
            (
                "몸을 날려 대신 공을 맞고 아웃된다.",
                15,
                "'괜찮아?! 진짜 멋있었어...!' {target}이(가) 감동했다! (+15)",
            ),
            (
                "날아오는 공을 한 손으로 멋지게 잡아낸다!",
                20,
                "반 전체가 환호하고 {target}의 눈에서 하트가 나온다! (+20)",
            ),
            (
                "나도 살기 위해 {target} 뒤로 숨는다.",
                -20,
                "{target}이(가) 공에 맞고 나를 째려보았다... (-20)",
            ),
            (
                "공을 피하려다 혼자 발이 걸려 우스꽝스럽게 넘어진다.",
                5,
                "{target}이(가) 배를 잡고 웃으며 괜찮냐고 챙겨주었다. (+5)",
            ),
        ],
    },
    {
        "title": "3단계: 비 오는 날의 편의점",
        "desc": (
            "하굣길에 갑자기 폭우가 쏟아진다. 편의점 앞에서 비를 피하고 있는"
            " {target}을(를) 발견했다!"
        ),
        "options": [
            (
                "편의점에서 우산 두 개를 사서 하나를 쿨하게 건넨다.",
                15,
                "'헐, 진짜 고마워! 내일 꼭

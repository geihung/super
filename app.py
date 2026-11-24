import random
import streamlit as st

st.set_page_config(
    page_title="두근두근 고백 시뮬레이터 PRO", page_icon="💘", layout="centered"
)

# --- 1. 세션 상태 초기화 ---
def init_game():
    st.session_state.step = "intro"
    st.session_state.my_name = ""
    st.session_state.target_name = ""
    st.session_state.affection = 25  # 기본 호감도
    st.session_state.day = 1  # 현재 날짜 (총 7일 제한)
    st.session_state.max_days = 7
    st.session_state.money = 15000  # 초기 용돈
    st.session_state.stats = {"센스": 10, "다정함": 10, "용기": 10}
    st.session_state.inventory = []
    st.session_state.used_events = []
    st.session_state.current_event = None
    st.session_state.log = []  # 행동 기록 로그
    st.session_state.ending_type = ""


if "step" not in st.session_state:
    init_game()

# --- 2. 방대한 시나리오 데이터 (조건부 선택지 포함) ---
SCENARIOS = [
    {
        "id": 1,
        "title": "☔ 비 오는 날의 하굣길",
        "story": (
            "갑자기 소나기가 쏟아진다. 우산이 없어 발을 동동 구르고 있는데, 저쪽에"
            " {target}이(가) 우산을 쓰고 서 있다!"
        ),
        "choices": [
            {
                "text": "용기 내어 다가가 '혹시 우산 같이 쓸래?'라고 묻는다.",
                "req_stat": None,
                "aff": 15,
                "stat_up": ("용기", 5),
                "money": 0,
                "reaction": (
                    "{target}이(가) 살짝 놀라더니 환하게 웃으며 우산을 기울여"
                    " 주었다."
                ),
            },
            {
                "text": (
                    "✨ [센스 15 필요] 편의점에서 2인용 큰 우산을 사 와서"
                    " 건넨다."
                ),
                "req_stat": ("센스", 15),
                "aff": 25,
                "stat_up": ("센스", 5),
                "money": -5000,
                "reaction": (
                    "'와, 너 진짜 센스 대박이다!' 비 한 방울 안 맞고 둘이"
                    " 나란히 걸었다."
                ),
            },
            {
                "text": "부끄러워서 그냥 비를 맞으며 전력 질주한다.",
                "req_stat": None,
                "aff": -10,
                "stat_up": ("용기", -3),
                "money": 0,
                "reaction": (
                    "비가 다 젖은 채 뛰어가는 뒷모습을 {target}이(가) 어리둥절하게"
                    " 쳐다보았다."
                ),
            },
            {
                "text": "자연스럽게 가방으로 비를 가려주며 근처 카페로 피신한다.",
                "req_stat": None,
                "aff": 12,
                "stat_up": ("다정함", 4),
                "money": -4000,
                "reaction": (
                    "카페에서 따뜻한 음료를 마시며 한참 동안 수다를 떨었다."
                ),
            },
        ],
    },
    {
        "id": 2,
        "title": "🔥 떡볶이 맛집 탐방",
        "story": (
            "주말에 우연히 시내에서 마주친 {target}와(과) 함께 떡볶이를 먹으러"
            " 왔다. 그런데 떡볶이가 생각보다 엄청 맵다!"
        ),
        "choices": [
            {
                "text": "얼른 일어나 쿨피스와 단무지를 챙겨 {target} 앞에 놓는다.",
                "req_stat": None,
                "aff": 18,
                "stat_up": ("다정함", 5),
                "money": -2000,
                "reaction": (
                    "'어, 나 매운 거 약한 거 어떻게 알았어?' {target}의 눈이"
                    " 반짝인다!"
                ),
            },
            {
                "text": (
                    "✨ [다정함 15 필요] 계란찜을 추가 주문해주며 매운맛을"
                    " 중화시켜준다."
                ),
                "req_stat": ("다정함", 15),
                "aff": 25,
                "stat_up": ("다정함", 5),
                "money": -4000,
                "reaction": (
                    "세심한 배려에

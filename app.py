import random
import streamlit as st

st.set_page_config(page_title="두근두근 고백 시뮬레이터", page_icon="💖", layout="centered")

# 1. 세션 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "start"
if "me" not in st.session_state:
    st.session_state.me = ""
if "target" not in st.session_state:
    st.session_state.target = ""
if "target_gender" not in st.session_state:
    st.session_state.target_gender = "여학생"
if "love" not in st.session_state:
    st.session_state.love = 25
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "msg" not in st.session_state:
    st.session_state.msg = ""


# 캐릭터별 이미지 URL 생성 함수 (인터넷 연결 시 자동 로드, 깨짐 방지)
def get_avatar(seed_name, style="adventurer"):
    return f"https://api.dicebear.com/9.x/{style}/svg?seed={seed_name}&backgroundColor=ffd5dc,c0aede,b6e3f4"


# 2. 시나리오 데이터 (총 8단계, 각 4개 선택지, 제3자 개입 포함)
EVENTS = [
    {
        "title": "1단계: 설레는 첫 등굣길",
        "who": "target",
        "story": "아침 등굣길, 교문 앞에서 {target}와(과) 딱 마주쳤다! {target}이(가) 반갑게 손을 흔든다.",
        "choices": [
            ("밝게 웃으며 '안녕! 오늘 일찍 왔네?'라고 인사한다.", 10, "{target}도 환하게 웃으며 같이 교실까지 걸어갔다. (+10)"),
            ("무심한 척 고개만 까딱하고 먼저 걸어간다.", -5, "{target}이(가) 살짝 머쓱해하며 뒤따라왔다. (-5)"),
            ("'어제 숙제 다 했어?'라며 자연스럽게 대화를 이어간다.", 12, "함께 숙제 이야기를 하며 금세 분위기가 좋아졌다! (+12)"),
            ("너무 긴장해서 눈을 피하고 전력 질주한다.", -10, "{target}이(가) 어리둥절한 표정으로 쳐다보았다. (-10)"),
        ],
    },
    {
        "title": "2단계: 친구 '민수'의 장난 (제3자 개입!

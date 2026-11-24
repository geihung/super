import random
import streamlit as st

st.set_page_config(page_title="두근두근 고백 시뮬레이터", page_icon="💖")

# 세션 상태 초기화
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "my_name" not in st.session_state:
    st.session_state.my_name = ""
if "target_name" not in st.session_state:
    st.session_state.target_name = ""
if "affection" not in st.session_state:
    st.session_state.affection = 30
if "event_idx" not in st.session_state:
    st.session_state.event_idx = 0
if "last_reaction" not in st.session_state:
    st.session_state.last_reaction = ""

# 시나리오 데이터
SCENARIOS = [
    {
        "title": "첫 번째 만남: 비 오는 날의 하굣길",
        "story": (
            "갑자기 소나기가 쏟아진다. 우산이 없어 발을 동동 구르고 있는데, 저쪽에"
            " {target}이(가) 우산을 쓰고 서 있는 게 보인다!"
        ),
        "choices": [
            {
                "text": "용기 내어 다가가 '혹시 우산 같이 쓸래?'라고 묻는다.",
                "delta": 20,
                "reaction": (
                    "{target}이(가) 살짝 놀라더니 환하게 웃으며 우산을 기울여"
                    " 주었다. (호감도 +20)"
                ),
            },
            {
                "text": "부끄러워서 그냥 비를 맞으며 전력 질주한다.",
                "delta": -10,
                "reaction": (
                    "비가 다 젖은 채 뛰어가는 뒷모습을 {target}이(가) 어리둥절하게"
                    " 쳐다보았다. (호감도 -10)"
                ),
            },
            {
                "text": "편의점에 뛰어 들어가 우산 두 개를 사서 하나를 건넨다.",
                "delta": 25,
                "reaction": (
                    "'어, 나 우산 있는데... 고마워! 센스 있다!' {target}이(가)"
                    " 감동한 눈치다. (호감도 +25)"
                ),
            },
        ],
    },
    {
        "title": "두 번째 만남: 떡볶이 맛집 탐방",
        "story": (
            "주말에 우연히 시내에서 마주친 {target}와(과) 함께 떡볶이를 먹으러"
            " 왔다. 그런데 떡볶이가 생각보다 너무 맵다!"
        ),
        "choices": [
            {
                "text": "매운 걸 못 먹는 티를 안 내려고 땀을 뻘뻘 흘리며 먹는다.",
                "delta": 5,
                "reaction": (
                    "{target}이(가) 휴지를 건네며 귀엽다는 듯 피식 웃었다."
                    " (호감도 +5)"
                ),
            },
            {
                "text": (
                    "얼른 일어나서 쿨피스(음료수)와 단무지를 챙겨 {target} 앞에"
                    " 놓아준다."
                ),
                "delta": 20,
                "reaction": (
                    "'와, 나 매운 거 약한 거 어떻게 알았어?' {target}의 눈이"
                    " 반짝인다! (호감도 +20)"
                ),
            },
            {
                "text": "'아, 여기 너무 맵네. 맛없다.'라며 불평한다.",
                "delta": -20,
                "reaction": (
                    "{target}의 표정이 굳어졌다. 사실 여기는 {target}의 단골"
                    " 맛집이었다... (호감도 -20)"
                ),
            },
        ],
    },
    {
        "title": "세 번째 만남: 밤늦은 카톡",
        "story": (
            "밤 11시, 휴대폰이 울린다. {target}에게서 온 메시지다. '자니? 오늘"
            " 좀 우울한 일이 있어서...'"
        ),
        "choices": [
            {
                "text": (
                    "'무슨 일인데? 내가 다 들어줄게. 전화할까?'라고 바로"
                    " 답장한다."
                ),
                "delta": 25,
                "reaction": (
                    "한참 통화를 하고 나니 {target}의 목소리가 한결 밝아졌다."
                    " '고마워, {me}.' (호감도 +25)"
                ),
            },
            {
                "text": "'힘내! 내일 되면 다 괜찮아질 거야~'라고 짧게 보낸다.",
                "delta": 0,
                "reaction": (
                    "'응, 고마워 잘 자.' 대화가 뚝 끊겨버렸다. (호감도 0)"
                ),
            },
            {
                "text": "이미 자는 척하고 다음 날 아침에 읽씹한다.",
                "delta": -25,
                "reaction": (
                    "다음 날 학교에서 마주쳤지만 {target}이(가) 어색하게 시선을"
                    " 피한다. (호감도 -25)"
                ),
            },
        ],
    },
    {
        "title": "네 번째 만남: 축제 준비",
        "story": (
            "학교 축제 부스 준비로 둘만 교실에 남게 되었다. 어색하면서도 설레는"
            " 침묵이 흐른다."
        ),
        "choices": [
            {
                "text": "장난스럽게 페인트를 {target}의 코끝에 살짝 묻힌다.",
                "delta": 15,
                "reaction": (
                    "'야! 너 이리 와!' 서로 장난치며 한층 더 가까워진 느낌이다."
                    " (호감도 +15)"
                ),
            },
            {
                "text": "묵묵히 힘든 일을 도맡아 하며 {target}을(를) 챙겨준다.",
                "delta": 20,
                "reaction": (
                    "'너 진짜 듬직하다. 같이 하니까 금방 끝나네!' (호감도 +20)"
                ),
            },
            {
                "text": "'나 먼저 갈게, 수고해!' 하고 혼자 집에 가버린다.",
                "delta": -30,
                "reaction": (
                    "혼자 남은 {target}이(가) 허탈한 표정으로 뒷정리를 했다."
                    " (호감도 -30)"
                ),
            },
        ],
    },
]


# 화면 새로고침 호환 함수 (구버전/신버전 모두 지원)
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()


# 게임 초기화 콜백 함수
def reset_game():
    st.session_state.step = "intro"
    st.session_state.affection = 30
    st.session_state.event_idx = 0
    st.session_state.last_reaction = ""


# 선택지 클릭 콜백 함수
def handle_choice(delta, reaction_template):
    me = st.session_state.my_name
    target = st.session_state.target_name

    new_aff = min(100, max(0, st.session_state.affection + delta))
    st.session_state.affection = new_aff
    st.session_state.last_reaction = reaction_template.format(
        me=me, target=target
    )
    st.session_state.event_idx += 1

    if new_aff >= 100:
        st.session_state.step = "happy_ending"
    elif new_aff <= 0:
        st.session_state.step = "bad_ending"


# 고백 실행 콜백 함수
def try_confess():
    aff = st.session_state.affection
    dice = random.randint(1, 100)
    if dice <= aff:
        st.session_state.step = "happy_ending"
    else:
        st.session_state.step = "fail_ending"


# --- 화면 1: 이름 입력 ---
if st.session_state.step == "intro":
    st.title("💖 두근두근 고백 시뮬레이터")
    st.write(
        "당신의 선택에 따라 상대방의 호감도가 변합니다. 호감도 100을 달성해"
        " 사랑에 성공하세요!"
    )

    my_name = st.text_input("당신의 이름을 입력하세요", placeholder="예: 지훈")
    target_name = st.text_input(
        "좋아하는 상대의 이름을 입력하세요", placeholder="예: 서연"
    )

    if st.button("게임 시작하기"):
        if my_name.strip() and target_name.strip():
            st.session_state.my_name = my_name.strip()
            st.session_state.target_name = target_name.strip()
            st.session_state.step = "event"
            safe_rerun()
        else:
            st.warning("두 사람의 이름을 모두 입력해주세요!")

# --- 화면 2: 이벤트 진행 ---
elif st.session_state.step == "event":
    me = st.session_state.my_name
    target = st.session_state.target_name
    aff = st.session_state.affection

    st.subheader(f"💘 {target}의 현재 호감도: {aff}%")
    st.progress(aff / 100.0)

    if st.session_state.last_reaction:
        st.info(st.session_state.last_reaction)

    # 모든 이벤트를 다 겪었을 때
    if st.session_state.event_idx >= len(SCENARIOS):
        st.warning("모든 이벤트가 끝났습니다! 이제 마지막 결정을 내려야 합니다.")
        st.button(
            f"💌 {target}에게 고백하기 (성공 확률 {aff}%)",
            on_click=try_confess,
        )
    else:
        current_event = SCENARIOS[st.session_state.event_idx]
        st.markdown("---")
        st.header(current_event["title"])
        st.write(current_event["story"].format(me=me, target=target))

        st.write("**어떻게 행동할까?**")
        for i, choice in enumerate(current_event["choices"]):
            st.button(
                choice["text"],
                key=f"ev_{st.session_state.event_idx}_ch_{i}",
                on_click=handle_choice,
                args=(choice["delta"], choice["reaction"]),
            )

        st.markdown("---")
        if aff >= 40:
            st.write(
                f"💡 지금 고백하면 **{aff}%** 확률로 성공할 수 있습니다. (호감도"
                " 100%가 되면 무조건 성공!)"
            )
            st.button(
                f"💌 지금 바로 {target}에게 고백하기!", on_click=try_confess
            )
        else:
            st.caption("🔒 호감도가 40% 이상이어야 중간 고백을 할 수 있습니다.")

# --- 화면 3-1: 해피 엔딩 ---
elif st.session_state.step == "happy_ending":
    me = st.session_state.my_name
    target = st.session_state.target_name

    st.balloons()
    st.title("🎉 고백 성공! 오늘부터 1일!")
    st.success(
        f"**{me}**의 진심이 **{target}**에게 닿았습니다!\n\n"
        f"'{target}: 나도 사실 너 좋아하고 있었어... 우리 오늘부터 사귀자!'"
    )
    st.write(f"최종 호감도: **{st.session_state.affection}%**")
    st.button("다시 플레이하기", on_click=reset_game)

# --- 화면 3-2: 고백 실패 엔딩 ---
elif st.session_state.step == "fail_ending":
    me = st.session_state.my_name
    target = st.session_state.target_name

    st.title("💔 고백 실패...")
    st.error(
        f"**{me}**은(는) 용기를 내어 고백했지만, 아직 **{target}**의 마음이"
        " 충분히 열리지 않았던 것 같습니다.\n\n"
        f"'{target}: 미안해... 너는 정말 좋은 친구지만, 아직은 그런 마음은"
        " 아니야.'"
    )
    st.write(
        f"고백 당시 호감도: **{st.session_state.affection}%** (호감도를 더"
        " 높여서 도전해보세요!)"
    )
    st.button("다시 도전하기", on_click=reset_game)

# --- 화면 3-3: 호감도 바닥 엔딩 ---
elif st.session_state.step == "bad_ending":
    me = st.session_state.my_name
    target = st.session_state.target_name

    st.title("❄️ 인연의 끝...")
    st.error(
        f"연이은 실수로 **{target}**의 호감도가 0%가 되었습니다.\n\n"
        f"이제 **{target}**은(는) {me}와(과) 마주쳐도 인사조차 하지 않습니다."
    )
    st.button("처음부터 다시 하기", on_click=reset_game)

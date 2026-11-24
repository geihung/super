import random
import streamlit as st

# 화면 새로고침 호환 함수 (구버전/신버전 Streamlit 모두 오류 없이 작동)
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# 1. 변수 초기화
if "page" not in st.session_state:
    st.session_state.page = "start"
if "me" not in st.session_state:
    st.session_state.me = ""
if "target" not in st.session_state:
    st.session_state.target = ""
if "love" not in st.session_state:
    st.session_state.love = 30
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "msg" not in st.session_state:
    st.session_state.msg = ""

# 2. 시나리오 목록 (총 7개 상황, 제3자 개입 포함)
events = [
    {
        "title": "상황 1. 비 오는 날의 하굣길",
        "q": "갑자기 소나기가 쏟아진다! 우산이 없어 발을 동동 구르고 있는데, 저쪽에 {target}이(가) 우산을 쓰고 서 있다.",
        "a": [
            ("용기 내어 다가가 '혹시 우산 같이 쓸래?'라고 묻는다.", 15, "{target}이(가) 환하게 웃으며 우산을 기울여 주었다. (호감도 +15)"),
            ("편의점에 뛰어 들어가 우산 두 개를 사서 하나를 건넨다.", 20, "'어, 나 우산 있는데... 고마워! 센스 있다!' 감동한 눈치다. (호감도 +20)"),
            ("부끄러워서 그냥 비를 맞으며 전력 질주한다.", -10, "비가 다 젖은 채 뛰어가는 뒷모습을 어리둥절하게 쳐다보았다. (호감도 -10)"),
            ("마침 지나가던 다른 친구 우산에 쏙 들어가 버린다.", -15, "{target}이(가) 아쉽다는 표정으로 발길을 돌렸다. (호감도 -15)"),
        ],
    },
    {
        "title": "상황 2. [제3자 개입] 라이벌의 등장!",
        "q": "점심시간, 다른 반 인기남(녀) '민준'이(가) {target}에게 다가와 음료수를 건네며 말을 걸고 있다! 둘이 꽤 다정해 보인다.",
        "a": [
            ("자연스럽게 다가가 대화에 끼어들며 {target}을(를) 챙긴다.", 15, "민준이 머쓱해하며 자리를 떴고, {target}이(가) 반가워한다! (호감도 +15)"),
            ("나도 더 맛있는 음료수를 사 와서 {target} 책상에 슬쩍 올려둔다.", 20, "은근한 질투심과 센스에 {target}의 심장이 두근거렸다! (호감도 +20)"),
            ("질투가 나서 괜히 {target}에게 퉁명스럽게 대한다.", -20, "{target}: '얘가 갑자기 왜 이러지?' 영문을 몰라 당황했다. (호감도 -20)"),
            ("기죽어서 구석에서 혼자 씁쓸하게 지켜보기만 한다.", -5, "아무 일도 일어나지 않았지만 기회를 놓쳐버렸다. (호감도 -5)"),
        ],
    },
    {
        "title": "상황 3. 떡볶이 맛집 탐방",
        "q": "주말에 우연히 시내에서 마주쳐 함께 떡볶이를 먹으러 왔다. 그런데 생각보다 너무 맵다!",
        "a": [
            ("얼른 쿨피스와 단무지를 챙겨 {target} 앞에 먼저 놓아준다.", 20, "'와, 나 매운 거 약한 거 어떻게 알았어?' 눈이 반짝인다! (호감도 +20)"),
            ("매운 걸 못 먹는 티를 안 내려고 땀을 뻘뻘 흘리며 먹는다.", 5, "귀엽다는 듯 피식 웃으며 휴지를 건네주었다. (호감도 +5)"),
            ("'아, 여기 너무 맵네. 맛없다.'라며 투덜거린다.", -20, "사실 여기는 {target}의 단골 맛집이었다... 표정이 굳어졌다. (호감도 -20)"),
            ("매운 걸 중화시키자며 근처 아이스크림 가게로 2차를 제안한다.", 15, "자연스러운 데이트 코스로 이어져 즐거운 시간을 보냈다! (호감도 +15)"),
        ],
    },
    {
        "title": "상황 4. [제3자 개입] 눈치 없는 절친의 폭탄 발언",
        "q": "친구들과 다 같이 모인 자리에서 내 절친 '지우'가 장난으로 '야, {me} 너 {target} 좋아하지?'라고 큰소리로 떠들어버렸다!",
        "a": [
            ("당황하지 않고 웃으며 '응, 나 {target} 팬이잖아~'라고 유쾌하게 넘긴다.", 15, "센스 있는 대처에 분위기도 살고 {target}도 설렌 눈치다! (호감도 +15)"),
            ("얼굴이 새빨개져서 아무 말도 못 하고 고개를 숙인다.", 10, "순수하게 부끄러워하는 모습에 {target}의 입꼬리가 올라갔다. (호감도 +10)"),
            ("'무슨 소리야! 절대 아니거든!'이라며 정색하고 강하게 부정한다.", -25, "{target}이(가) 상처받은 표정으로 조용해졌다... (호감도 -25)"),
            ("절친 지우의 입을 막으며 밖으로 끌고 나간다.", 0, "상황은 모면했지만 {target}이(가) 조금 헷갈려한다. (호감도 0)"),
        ],
    },
    {
        "title": "상황 5. 밤늦은 카톡",
        "q": "밤 11시, 휴대폰이 울린다. {target}에게서 온 메시지다. '자니? 오늘 좀 우울한 일이 있어서...'",
        "a": [
            ("'무슨 일인데? 내가 다 들어줄게. 전화할까?'라고 바로 답장한다.", 20, "한참 통화 후 {target}의 목소리가 한결 밝아졌다! (호감도 +20)"),
            ("'지금 집 앞으로 잠깐 나올래? 바람 쐬면서 얘기하자.'라고 한다.", 25, "집 앞까지 찾아온 진심에 {target}이(가) 크게 감동했다! (호감도 +25)"),
            ("'힘내! 내일 되면 다 괜찮아질 거야~'라고 짧게 보낸다.", 0, "'응, 고마워 잘 자.' 대화가 뚝 끊겨버렸다. (호감도 0)"),
            ("귀찮아서 다음 날 아침까지 읽씹한다.", -25, "다음 날 학교에서 마주쳤지만 시선을 피한다. (호감도 -25)"),
        ],
    },
    {
        "title": "상황 6. [제3자 개입] 조별 과제와 빌런 조원",
        "q": "같은 조가 된 다른 조원이 발표 자료를 엉망으로 해놓고 연락이 두절됐다! {target}이(가) 혼자 끙끙대며 수습하고 있다.",
        "a": [
            ("'내가 자료 조사할게, 넌 디자인만 봐줘!'라며 밤새 함께 수습한다.", 25, "함께 고생하며 전우애와 깊은 신뢰가 싹텄다! (호감도 +25)"),
            ("달달한 간식과 커피를 사 와서 {target} 옆에서 응원하며 돕는다.", 15, "'덕분에 힘난다! 진짜 고마워.' 환하게 웃어주었다. (호감도 +15)"),
            ("잠수 탄 조원을 욕하며 불평만 늘어놓는다.", -15, "{target}이(가) 피곤한 표정으로 한숨을 쉬었다. (호감도 -15)"),
            ("'나도 바빠서 못 할 것 같아...'라며 발을 뺀다.", -30, "무책임한 모습에 {target}이(가) 크게 실망했다. (호감도 -30)"),
        ],
    },
    {
        "title": "상황 7. 축제 전날 밤의 교실",
        "q": "학교 축제 부스 준비로 둘만 교실에 남게 되었다. 노을이 지는 교실에 어색하면서도 설레는 침묵이 흐른다.",
        "a": [
            ("장난스럽게 페인트를 {target}의 코끝에 살짝 묻힌다.", 15, "'야! 너 이리 와!' 서로 장난치며 한층 더 가까워졌다. (호감도 +15)"),
            ("묵묵히 무거운 짐을 도맡아 옮기며 듬직한 모습을 보여준다.", 20, "'너 진짜 듬직하다. 같이 하니까 금방 끝나네!' (호감도 +20)"),
            ("조용히 음악을 틀어놓고 진솔한 속마음 대화를 나눈다.", 25, "서로의 진심을 확인하며 묘한 기류가 흘렀다. (호감도 +25)"),
            ("'나 먼저 갈게, 수고해!' 하고 혼자 집에 가버린다.", -30, "혼자 남은 {target}이(가) 허탈한 표정으로 뒷정리를 했다. (호감도 -30)"),
        ],
    },
]

# --- 화면 1: 시작 화면 ---
if st.session_state.page == "start":
    st.title("💖 두근두근 고백 시뮬레이터 (확장판)")
    st.write("다양한 상황과 주변 인물들의 개입 속에서 호감도를 100%까지 올려보세요!")
    
    my_input = st.text_input("당신의 이름", placeholder="예: 지훈")
    target_input = st.text_input("좋아하는 상대의 이름", placeholder="예: 서연")

    if st.button("게임 시작하기"):
        if my_input.strip() and target_input.strip():
            st.session_state.me = my_input.strip()
            st.session_state.target = target_input.strip()
            st.session_state.page = "play"
            safe_rerun()
        else:
            st.warning("두 사람의 이름을 모두 입력해주세요!")

# --- 화면 2: 게임 진행 화면 ---
elif st.session_state.page == "play":
    me = st.session_state.me
    target = st.session_state.target
    love = st.session_state.love

    # 상단 호감도 게이지
    st.subheader(f"💘 {target}의 현재 호감도: {love}%")
    st.progress(min(max(love, 0), 100) / 100)

    # 직전 선택 결과 메시지
    if st.session_state.msg:
        st.info(st.session_state.msg)

    # 즉시 엔딩 조건 체크
    if love >= 100:
        st.session_state.page = "win"
        safe_rerun()
    elif love <= 0:
        st.session_state.page = "bad"
        safe_rerun()

    # 모든 이벤트를 다 겪었을 때
    if st.session_state.idx >= len(events):
        st.warning("모든 이벤트가 종료되었습니다! 이제 마지막 고백을 할 시간입니다.")
        if st.button(f"💌 {target}에게 마지막 고백하기 (성공 확률 {love}%)"):
            if random.randint(1, 100) <= love:
                st.session_state.page = "win"
            else:
                st.session_state.page = "fail"
            safe_rerun()
    else:
        ev = events[st.session_state.idx]
        st.write("---")
        st.header(ev["title"])
        st.write(ev["q"].format(me=me, target=target))

        st.write("**어떻게 행동할까?**")
        for i, (text, delta, reaction) in enumerate(ev["a"]):
            btn_text = text.format(me=me, target=target)
            if st.button(btn_text, key=f"btn_{st.session_state.idx}_{i}"):
                st.session_state.love = min(100, max(0, love + delta))
                st.session_state.msg = reaction.format(me=me, target=target)
                st.session_state.idx += 1
                safe_rerun()

        # 중간 고백하기 기능
        st.write("---")
        if love >= 40:
            st.write(f"💡 지금 고백하면 **{love}%** 확률로 성공합니다. (호감도 100% 달성 시 무조건 성공!)")
            if st.button(f"💌 지금 바로 {target}에게 고백하기!"):
                if random.randint(1, 100) <= love:
                    st.session_state.page = "win"
                else:
                    st.session_state.page = "fail"
                safe_rerun()
        else:
            st.caption("🔒 호감도가 40% 이상이어야 중간 고백을 할 수 있습니다.")

# --- 화면 3: 엔딩 화면들 ---
elif st.session_state.page == "win":
    st.balloons()
    st.title("🎉 고백 성공! 오늘부터 1일!")
    st.success(
        f"**{st.session_state.me}**의 진심이 **{st.session_state.target}**에게 닿았습니다!\n\n"
        f"'{st.session_state.target}: 나도 사실 너 좋아하고 있었어... 우리 오늘부터 사귀자!'"
    )
    st.write(f"최종 호감도: **{st.session_state.love}%**")
    if st.button("처음부터 다시 하기"):
        st.session_state.clear()
        safe_rerun()

elif st.session_state.page == "fail":
    st.title("💔 고백 실패...")
    st.error(
        f"용기를 내어 고백했지만, 아직 **{st.session_state.target}**의 마음이 충분히 열리지 않았던 것 같습니다.\n\n"
        f"'{st.session_state.target}: 미안해... 너는 정말 좋은 친구지만, 아직은 그런 마음은 아니야.'"
    )
    st.write(f"고백 당시 호감도: **{st.session_state.love}%** (호감도를 더 높여서 도전해보세요!)")
    if st.button("다시 도전하기"):
        st.session_state.clear()
        safe_rerun()

elif st.session_state.page == "bad":
    st.title("❄️ 인연의 끝...")
    st.error(
        f"연이은 실수로 **{st.session_state.target}**의 호감도가 0%가 되었습니다.\n\n"
        f"이제 **{st.session_state.target}**은(는) 마주쳐도 인사조차 하지 않습니다."
    )
    if st.button("처음부터 다시 하기"):
        st.session_state.clear()
        safe_rerun()

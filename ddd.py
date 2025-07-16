import streamlit as st

# 이미지 또는 텍스트 아스키아트 저장
image = {
    "start": "🥟 고향만두 게임에 오신 걸 환영합니다!",
    "ending_success": "🎉 승리! 진정한 고향만두의 맛!",
    "ending_fail": "😭 실패! 다시 도전해보세요!",
}

mandu_inside = [
    '돼지고기', '두부', '양파', '양배추', '계란', '참기름', '에이스',
    '매운고추', '마늘', '치즈', '대파', '고추장', '옹스짱', '크림치즈',
]

mandu_pi = ['쌀가루', '밀가루', '콩가루']
mandu_water = ['막걸리', '와인', '주스', '물']
mandu_shape = ['긴반달모양', '또아리모양', '쭈그리모양']
mandu_cook = ['뜨거운 물에 삼기', '후라이펜에 굽기', '찜통에 찌기']

answer_mandu = ['돼지고기', '두부', '양파', '양배추', '참기름', '마늘', '대파']

# 초기 상태 설정
if 'page' not in st.session_state:
    st.session_state.page = 'start'
    st.session_state.ingredients = []
    st.session_state.pi = ''
    st.session_state.water = ''
    st.session_state.shape = ''
    st.session_state.cook = ''
    st.session_state.result = None


def reset_game():
    st.session_state.page = 'start'
    st.session_state.ingredients = []
    st.session_state.pi = ''
    st.session_state.water = ''
    st.session_state.shape = ''
    st.session_state.cook = ''
    st.session_state.result = None


# 페이지 구성
if st.session_state.page == 'start':
    st.title("🥟 고향만두 게임")
    st.markdown(image['start'])
    if st.button("게임 시작"):
        st.session_state.page = 'step1'
    if st.button("게임 방법"):
        st.info("""
        1. 순서대로 만두를 만듭니다.
        2. 재료를 잘 고르면 승리!
        3. 틀리면 다시 도전하세요.
        """)

elif st.session_state.page == 'step1':
    st.header("1단계: 만두속 만들기 (최소 5가지)")
    selected = st.multiselect("재료를 골라주세요", mandu_inside, default=st.session_state.ingredients)
    st.session_state.ingredients = selected

    if len(selected) >= 5:
        if st.button("다음 단계"):
            st.session_state.page = 'step2'
    else:
        st.warning("재료를 5개 이상 선택하세요.")

elif st.session_state.page == 'step2':
    st.header("2단계: 만두피 만들기")
    st.session_state.pi = st.selectbox("가루 선택", mandu_pi)
    st.session_state.water = st.selectbox("액체 선택", mandu_water)

    if st.button("다음 단계"):
        st.session_state.page = 'step3'

elif st.session_state.page == 'step3':
    st.header("3단계: 만두 모양 고르기")
    st.session_state.shape = st.radio("모양 선택", mandu_shape)

    if st.button("다음 단계"):
        st.session_state.page = 'step4'

elif st.session_state.page == 'step4':
    st.header("4단계: 요리 방식 고르기")
    st.session_state.cook = st.selectbox("요리 방식", mandu_cook)

    if st.button("만두 시식하기!"):
        st.session_state.page = 'result'

elif st.session_state.page == 'result':
    st.subheader("🍽️ 시식 결과")

    # 평가 로직
    win_cnt = sum(1 for i in st.session_state.ingredients if i in answer_mandu)
    win_cnt_2 = 1 if (st.session_state.pi == '밀가루' and st.session_state.water == '물') else 0
    win_cnt_3 = 0
    shape = st.session_state.shape
    cook = st.session_state.cook

    if (shape == '긴반달모양' and cook == '후라이펜에 굽기') or \
            (shape == '또아리모양' and cook in ['뜨거운 물에 삼기', '찜통에 찌기']) or \
            (shape == '쭈그리모양' and cook == '뜨거운 물에 삼기'):
        win_cnt_3 = 1

    if win_cnt == 7 and win_cnt_2 == 1 and win_cnt_3 == 1:
        st.success(image['ending_success'])
    else:
        st.error(image['ending_fail'])
        if st.session_state.pi == '쌀가루':
            st.write("만두피가 쫄깃하지 않아요.")
        if st.session_state.pi == '콩가루':
            st.write("콩가루 맛이 너무 강해요.")
        if st.session_state.water != '물':
            st.write(f"{st.session_state.water} 향이 나서 이상해요.")
        if win_cnt < 5:
            st.write("속재료가 이상해요.")
        if win_cnt_3 == 0:
            st.write("요리방식이 모양에 안 어울려요.")

    if st.button("다시 하기"):
        reset_game()

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy
import base64
from scipy.signal import savgol_filter, find_peaks

import streamlit as st
import pandas as pd
import time
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# CSV 파일 경로 (실시간 업데이트 중인 파일 경로)
# csv_file_path = "real_time_data.csv"  # 파일 경로를 정확히 지정하세요.


from PIL import Image



# 그래프 업데이트 함수
def plot_live_graph(csv_path):
    try:
        # 실시간 데이터를 읽기
        data = pd.read_csv(csv_path)
        if data.empty:
            st.warning("CSV 파일이 비어 있습니다.")
            return

        # 데이터가 있는 경우 그래프 그리기
        plt.figure(figsize=(10, 5))
        plt.plot(data["time"], data["value"], marker="o", linestyle="-")
        plt.title("실시간 데이터 그래프")
        plt.xlabel("시간")
        plt.ylabel("값")
        plt.grid(True)
        st.pyplot(plt)
    except FileNotFoundError:
        st.error("CSV 파일을 찾을 수 없습니다. 경로를 확인하세요.")
    except Exception as e:
        st.error(f"오류 발생: {e}")


# 카운트다운 함수 정의
def show_countdown(total_time=30):
    countdown_placeholder = st.empty()
    progress_bar = st.progress(0)
    
    for i in range(total_time, 0, -1):
        countdown_placeholder.markdown(
            f"<h2 style='text-align: center;'>운동 측정 시작: <span style='color:blue;'>{i}</span>초 후</h2>", 
            unsafe_allow_html=True
        )
        progress_bar.progress((total_time - i + 1) / total_time)
        time.sleep(1)
    
    countdown_placeholder.empty()
    progress_bar.empty()


def update_hight_from_slider():
    st.session_state.hight_input = st.session_state.hight_slider
    st.session_state.hight = st.session_state.hight_slider

def update_hight_from_input():
    st.session_state.hight_slider = st.session_state.hight_input
    st.session_state.hight = st.session_state.hight_input

def update_weight_from_slider():
    st.session_state.weight_input = st.session_state.weight_slider
    st.session_state.weight = st.session_state.weight_slider

def update_weight_from_input():
    st.session_state.weight_slider = st.session_state.weight_input
    st.session_state.weight = st.session_state.weight_input


# 운동 횟수 계산 함수
def count_reps(data, time, offset):
    reps = 0
    above_offset = False
    below_offset = False
    below_times = []
    above_times = []

    for i in range(1, len(data)):
        if data[i] > offset:
            if below_offset:
                below_offset = False
                above_times.append(time[i])
        elif data[i] <= offset:
            if above_offset:
                above_offset = False
                below_times.append(time[i])

                # 유효한 운동 사이클 확인
                if len(below_times) > 0 and len(above_times) > 0:
                    if below_times[-1] > above_times[-1]:
                        reps += 1

            below_offset = True
        above_offset = data[i] > offset

    return reps, below_times, above_times


# BMI 계산 함수
def calculate_bmi(weight, height):
    height_m = height / 100  # cm를 m로 변환
    return round(weight / (height_m ** 2), 2)

# BMR 계산 함수
def calculate_bmr(sex, weight, height, age):
    if sex == '남성':
        return round(66.5 + (13.75 * weight) + (5.003 * height) - (6.75 * age), 2)
    else:
        return round(655.1 + (9.563 * weight) + (1.850 * height) - (4.676 * age), 2)

# BMI 범위 판정 함수
def bmi_category(bmi):
    if bmi < 18.5:
        return "저체중"
    elif 18.5 <= bmi < 23:
        return "정상"
    elif 23 <= bmi < 25:
        return "과체중"
    else:
        return "비만"

# BMI 점의 위치를 계산하는 함수
def bmi_position(bmi):
    # BMI 범위: 저체중(0-18.5), 정상(18.5-23), 과체중(23-25), 비만(25-40+)
    min_bmi = 0
    max_bmi = 40
    position = (bmi - min_bmi) / (max_bmi - min_bmi) * 100  # 퍼센트로 변환
    return min(max(position, 0), 100)  # 0~100 범위 제한

# csv_data = pd.read_csv('data.csv')
# st.session_state.csv_data = csv_data  # Store data in session state
# st.write("업로드된 데이터 (처음 100줄):")
# st.dataframe(csv_data.head(100))


# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "start"  # Initial start page

# Function to set page
def set_page(page_name):
    st.session_state.page = page_name

# Caching function for loading CSV
@st.cache_data(show_spinner=True)
def load_csv(file):
    return pd.read_csv(file)

# Debugging output
st.write("현재 페이지 상태:", st.session_state.page)

# Render pages based on the session state

if st.session_state.page == "start":
    st.title("📋 앱 시작하기")
    st.text("이 앱은 운동 선택 및 CSV 데이터를 시각화하는 데 사용됩니다.")
    st.image("KakaoTalk_20241212_230003394.png")
    with open("fe3b41ff75f4e1e73d48ae338fbc80b2.gif", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Base64 이미지 삽입
        st.markdown(
            f"""
            <div style="position: fixed; bottom: 10px; left: 10px;">
                <img src="data:image/gif;base64,{encoded_string}" style="width: 100px; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )
    if st.button("Run"):
        set_page("basis")  # Navigate to the home page

# elif st.session_state.page == "basis":
#     st.title("👧 기본 정보를 입력해줘요~")
#     st.write("신체 정보 등을 업로드하세요.")
#     st.session_state.age = st.slider('나이', 0, 100) 
    
#     st.text('제 나이는' + str(st.session_state.age)+ '세 입니다')

#     selected = st.radio( 'Sex' , ['남성','여성'] )
#     st.session_state.sex = selected
#     st.session_state.hight = st.slider('키' , 0.0 , 250.0, step=0.1)
#     st.session_state.hight = st.number_input("키", min_value=0.0, max_value=300.0, value=165.0)
#     st.session_state.weight = st.slider('몸무게' , 0 , 200, step=1)
#     st.session_state.weight = st.number_input("몸무게", min_value=0.0, max_value=300.0, value=70.0)


elif st.session_state.page == "basis":
    st.title("👧 기본 정보를 입력해줘요~")
    st.write("신체 정보 등을 업로드하세요.")

    # 나이 입력
    st.session_state.age = st.slider('나이', 0, 100) 
    
    st.text('제 나이는' + str(st.session_state.age)+ '세 입니다')

    # 성별 선택
    selected = st.radio('성별', ['남성', '여성'], index=0 if st.session_state.get('sex', '남성') == '남성' else 1)
    st.session_state.sex = selected

    # 키 입력 (동기화 처리)
    st.slider(
        '키 (슬라이더)', 
        0.0, 250.0, 
        step=0.1, 
        value=float(st.session_state.get('hight_slider', 165.0)),
        key='hight_slider',
        on_change=update_hight_from_slider
    )
    st.number_input(
        '키 (입력창)', 
        min_value=0.0, 
        max_value=300.0, 
        value=float(st.session_state.get('hight_input', 165.0)), 
        step=0.1, 
        key='hight_input',
        on_change=update_hight_from_input
    )

    # 몸무게 입력 (동기화 처리)
    st.slider(
        '몸무게 (슬라이더)', 
        0.0, 200.0, 
        step=0.1, 
        value=float(st.session_state.get('weight_slider', 70.0)),
        key='weight_slider',
        on_change=update_weight_from_slider
    )
    st.number_input(
        '몸무게 (입력창)', 
        min_value=0.0, 
        max_value=300.0, 
        value=float(st.session_state.get('weight_input', 70.0)), 
        step=0.1, 
        key='weight_input',
        on_change=update_weight_from_input
    )

    if 'hight' not in st.session_state:
        st.session_state.hight = 165.0

    if 'weight' not in st.session_state:
        st.session_state.weight = 70.0

    if 'age' not in st.session_state:
        st.session_state.age = 25

    if 'sex' not in st.session_state:
        st.session_state.sex = '남성'

    if st.button("시작해"):
        set_page("home")


elif st.session_state.page == "home":
    st.title("🏋️‍♂️ 운동 선택 및 데이터 시각화")

    # 입력 데이터 출력
    st.text(
        f"저는 {st.session_state.sex}이며, {st.session_state.age}세, "
        f"{st.session_state.hight}cm, {st.session_state.weight}kg 입니다."
    )

    # BMI와 BMR 계산
    bmi = calculate_bmi(st.session_state.weight, st.session_state.hight)  # BMI 계산
    bmr = calculate_bmr(st.session_state.sex, st.session_state.weight, st.session_state.hight, st.session_state.age)  # BMR 계산
    category = bmi_category(bmi)  # BMI 카테고리
    
    # BMI 위치 계산
    bmi_pos = bmi_position(bmi)  # BMI 위치

    # BMI에 따라 점의 위치 결정
    bmi_pos = bmi_position(bmi)
    
    # 결과 출력
    st.subheader("📊 결과")
    st.write(f"**표준 BMI (체질량지수)**: {bmi} ({category})")
    st.write(f"**표준 기초대사량 (BMR)**: {bmr} kcal/day")
    
    # BMI 시각화
    st.write("### 표준 BMI 분류 및 위치 시각화")
    st.markdown(f"""
        <style>
            .bmi-bar {{ 
                display: flex; 
                position: relative;
                height: 30px;
                width: 100%;
            }}
            .bmi-bar div {{ 
                flex: 1; 
                text-align: center; 
                line-height: 30px;
                font-weight: bold;
                color: white;
            }}
            .underweight {{ background-color: #4da3ff; }}
            .normal {{ background-color: #9dd06e; }}
            .overweight {{ background-color: #f0a94e; }}
            .obese {{ background-color: #e85c4e; }}
            .bmi-dot {{
                position: absolute;
                top: -10px;
                left: {bmi_pos}%;
                transform: translateX(-50%);
                width: 0; 
                height: 0; 
                border-left: 10px solid transparent;
                border-right: 10px solid transparent;
                border-top: 15px solid black;  /* 아래 방향 화살표 */
                z-index: 2;
            }}
        </style>
        <div class="bmi-bar">
            <div class="underweight">저체중</div>
            <div class="normal">정상</div>
            <div class="overweight">과체중</div>
            <div class="obese">비만</div>
            <div class="bmi-dot"></div>
        </div>
    """, unsafe_allow_html=True)
        
    # 현재 BMI 상태 출력
    st.write(f"**현재 BMI 상태**: {category}")
    
    # 첫 번째 항목: 삼두
    col2, col1 = st.columns([1, 2])  # 비율 설정: 버튼 1, 이미지 2
    with col1:
        if st.button("삼두 페이지로 이동"):
            set_page("삼두")
    with col2:
       st.image("data:image/jpeg;base64,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", caption="삼두", use_container_width=True)

    # 두 번째 항목: 사레레
    col2, col1 = st.columns([1, 2])  # 비율 설정: 버튼 1, 이미지 2
    with col1:
        if st.button("사레레 페이지로 이동"):
            set_page("사레레")
    with col2:
       st.image("https://mblogthumb-phinf.pstatic.net/MjAyNDAyMjNfMjU1/MDAxNzA4NjE2NTAyODUx.Yz14QKhzSHdt-3JVbYCp5RP15Zhq5nhOZwaWJRLaqmMg.WeALWGNC-3Ry0yXiyhhtByGiaJTSC8JDkc_LWIVhEyUg.PNG/SE-4ebe176a-47fb-4d74-844c-39ec26681e52.png?type=w800", caption="사레레", use_container_width=True)


    # 세 번째 항목: 이두
    col2, col1 = st.columns([1, 2])  # 비율 설정: 버튼 1, 이미지 2
    with col1:
        if st.button("이두 페이지로 이동"):
            set_page("이두")
    with col2:
        st.image("https://blog.kakaocdn.net/dn/dSw3lH/btq54MXF9Rl/nDVQ5JhPbMq5RRMRvpFHS0/img.png", caption="이두", use_container_width=True)

    # 네 번째 항목: 숄더 프레스
    col2, col1 = st.columns([1, 2])  # 비율 설정: 버튼 1, 이미지 2
    with col1:
        if st.button("어깨 페이지로 이동"):
            set_page("어깨")
    with col2:
       st.image("data:image/jpeg;base64,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", caption="어깨", use_container_width=True)


    # 4 번째 항목: 이두
    col2, col1 = st.columns([1, 2])  # 비율 설정: 버튼 1, 이미지 2
    with col1:
        if st.button("하체 페이지로 이동"):
            set_page("업데이트")
    with col2:
        st.image("https://cdn.maxq.kr/news/photo/202307/10814_21182_3558.jpg", caption="하체", use_container_width=True)
    # 5 번째 항목: 이두
    col2, col1 = st.columns([1, 2])  # 비율 설정: 버튼 1, 이미지 2
    with col1:
        if st.button("가슴 페이지로 이동"):
            set_page("업데이트")
    with col2:
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR60xyV_yf96nCcamJPME4JmW2O5G48Iq-Opw&s", caption="가슴", use_container_width=True)


# elif st.session_state.page == "home":
#     st.title("🏋️‍♂️ 운동 선택 및 데이터 시각화")
#     st.text(
#         '저는 ' + str(st.session_state.age) + '세, ' +
#         str(st.session_state.hight) + 'cm, ' +
#         str(st.session_state.weight) + 'kg 입니다.'
#     ) 

#     # Layout for images with clickable buttons
#     # col1, col2, col3 = st.columns(3)
#     col1 = st.columns([0, 1])
#     col2 = st.columns([1, 2])
#     col3 = st.columns([2, 3])
#     with col1:
#         st.image("data:image/jpeg;base64,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", caption="삼두", use_container_width=True)
    #     if st.button("삼두 페이지로 이동"):
    #         set_page("csv")

    # with col2:
    #     st.image("https://mblogthumb-phinf.pstatic.net/MjAyNDAyMjNfMjU1/MDAxNzA4NjE2NTAyODUx.Yz14QKhzSHdt-3JVbYCp5RP15Zhq5nhOZwaWJRLaqmMg.WeALWGNC-3Ry0yXiyhhtByGiaJTSC8JDkc_LWIVhEyUg.PNG/SE-4ebe176a-47fb-4d74-844c-39ec26681e52.png?type=w800", caption="사레레", use_container_width=True)
    #     if st.button("사레레 페이지로 이동"):
    #         set_page("csv")

    # with col3:
    #     st.image("https://blog.kakaocdn.net/dn/dSw3lH/btq54MXF9Rl/nDVQ5JhPbMq5RRMRvpFHS0/img.png", caption="이두", use_container_width=True)
    #     if st.button("이두 페이지로 이동"):
    #         set_page("csv")


elif st.session_state.page == "삼두":
    st.title("삼두 페이지")
    st.write("삼두 관련 데이터를 표시합니다.")
    if st.button("홈으로 돌아가기"):
        set_page("home")
        
    if st.button("분석"):
        set_page("rs")
    

elif st.session_state.page == "사레레":
    st.title("사레레 페이지")
    st.write("사레레 관련 데이터를 표시합니다.")
    if st.button("홈으로 돌아가기"):
        set_page("home")
        
    if st.button("분석"):
        set_page("csv")
    
    

elif st.session_state.page == "이두":
    st.title("이두 페이지")
    st.write("이두 관련 데이터를 표시합니다.")
    
    if st.button("홈으로 돌아가기"):
        set_page("home")

    if st.button("분석"):
        set_page("csv")
    
elif st.session_state.page == "어깨":
    st.title("어깨 페이지")
    st.write("어깨깨 관련 데이터를 표시합니다.")
    
    if st.button("홈으로 돌아가기"):
        set_page("home")

    if st.button("분석"):
        set_page("csv")


elif st.session_state.page == "업데이트":
    st.title("2026년 2월 업데이트 예정")
    # st.image("https://i.pinimg.com/originals/61/4b/b4/614bb4d7982f87558039fc55fb223ef5.gif",  use_container_width=True)
    # st.image("computer-internet.gif", use_container_width=True)
    st.image("“26 Times Ryan Reynolds Was Really Fucking Funny On Instagram Seriously, give the man a medal_”.gif", use_container_width=True)
    # st.image("https://mblogthumb-phinf.pstatic.net/MjAyMDA3MDJfMjk4/MDAxNTkzNjc1MzM5NjIx.OjEij9RK6k3yFrvDhkRC0_3NXmfFqZiHUS1tyv-Fygwg.Wk6unZQiMuqoJeqfrDhIhUNIpiuj3tumQI_WyP7a2Wog.GIF.sjlhome/Despicable_Me_2_2013_1080p_BRRip_x264_AC3-JYK.mkv_001209458.gif?type=w800", use_container_width=True)
    st.write("Coming soon~")
    # 이미지 파일을 Base64로 변환
    with open("a39da85f22af0926a84525350928d076.gif", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Base64 이미지 삽입
        st.markdown(
            f"""
            <div style="position: fixed; bottom: 10px; left: 10px;">
                <img src="data:image/gif;base64,{encoded_string}" style="width: 100px; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )
#     st.markdown(
#     """
#     <div style="text-align: center;">
#         <img src="https://img.extmovie.com/files/attach/images/135/615/810/084/0de6596f9677fb2a73d50c5cc6c6f83e.gif" alt="GIF Example" style="width: 100%; max-width: 500px;">
#     </div>
#     """,
#     unsafe_allow_html=True
# )
    if st.button("홈으로 돌아가기"):
        set_page("home")

# current_page = st.session_state.page

# Streamlit 페이지 관리
elif st.session_state.page == "csv":
    st.title("🎈 CSV 데이터의 축 선택 및 정적 그래프")

        # 초기 상태 설정
    # if "countdown_done" not in st.session_state:
    #     st.session_state.countdown_done = False

    # # 5초 카운트다운 (처음에만 실행)
    # if not st.session_state.countdown_done:
    #     countdown_placeholder = st.empty()
    #     progress_bar = st.progress(0)
    #     total_time = 5  # 총 카운트다운 시간 (초)

    #     for i in range(total_time, 0, -1):
    #         countdown_placeholder.markdown(
    #             f"<h2 style='text-align: center;'>운동 측정 시작: <span style='color:blue;'>{i}</span>초 후</h2>", 
    #             unsafe_allow_html=True
    #         )
    #         progress_bar.progress((total_time - i + 1) / total_time)
    #         time.sleep(1)
        
    #     countdown_placeholder.empty()
    #     progress_bar.empty()
    #     st.session_state.countdown_done = True  # 카운트다운 완료 상태 저장

     # 버튼을 눌러서 카운트다운 실행
    # 카운트다운 초기 상태 설정
    if "countdown_done" not in st.session_state:
        st.session_state.countdown_done = False  # 카운트다운 완료 여부
        st.session_state.show_upload = False  # 업로드 창 표시 여부

    # 카운트다운 상태에 따른 버튼 표시 및 처리
    if not st.session_state.countdown_done:
        # 처음 상태에서 "카운트다운 시작" 버튼
        if st.button("카운트다운 시작"):
            show_countdown()  # 카운트다운 실행
            st.session_state.countdown_done = True  # 카운트다운 완료 상태 저장
            st.session_state.show_upload = True  # 파일 업로드 창 표시 상태로 전환
            st.session_state.show_button = False
            st.button("카운트다운 다시 시작")
    else:
    #     # 카운트다운 완료 후 "카운트다운 다시 시작" 버튼
        if st.button("카운트다운 다시 시작"):
            st.session_state.countdown_done = False  # 다시 초기 상태로 복원
            st.session_state.show_upload = False  # 파일 업로드 창 숨김
    
    # CSV 파일 업로드 (카운트다운 완료 후 실행)
    if st.session_state.countdown_done:
        uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])



        if uploaded_file is not None:
            try:
                # CSV 파일 읽기 및 세션 상태에 저장
                csv_data = load_csv(uploaded_file)
                st.session_state.csv_data = csv_data
                st.write("업로드된 데이터 (처음 100줄):")
                st.dataframe(csv_data)  # 처음 100줄 표시
    
                # X축과 Y축 선택
                x_axis = st.selectbox("X 축 선택", csv_data.columns, key="csv_x_axis")
                y_axes = st.multiselect("Y 축 선택 (복수 가능)", csv_data.columns, key="csv_y_axes")
    
                if x_axis and y_axes:
                    # 선택된 데이터를 기반으로 그래프 생성
                    chart_data = csv_data[[x_axis] + y_axes].set_index(x_axis)
                    st.line_chart(chart_data)
    
                    # 운동 분석 버튼
                    if st.button("운동 분석", key="csv_analyze_button"):
                        if "Pitch" in csv_data.columns and "Time (ms)" in csv_data.columns:
                            try:
                                pitch = csv_data["Pitch"].to_numpy()
                                time_ms = csv_data["Time (ms)"].to_numpy()
                                offset = -35  # 기준 오프셋 값
    
                                # 운동 횟수 계산 함수
                                reps, below_times, above_times = count_reps(pitch, time_ms, offset)
    
                                # 분석 결과 출력
                                st.write(f"총 운동 횟수: {reps}")
                                st.line_chart({"Pitch": pitch, "Offset": [offset] * len(pitch)})
    
                            except Exception as e:
                                st.error(f"운동 분석 중 오류 발생: {e}")
                        else:
                            st.warning("'Pitch'와 'Time (ms)' 열이 데이터에 포함되어야 합니다.")
    
                    # 실시간 분석으로 이동
                    if st.button("실시간 분석으로 이동", key="csv_to_realtime_button"):
                        set_page("realtime")
                else:
                    st.warning("X축과 Y축을 모두 선택하세요.")
            except Exception as e:
                st.error(f"CSV 데이터 처리 중 오류 발생: {e}")
        else:
            st.warning("CSV 파일을 업로드하세요.")



# 실시간 분석 페이지
elif st.session_state.page == "realtime":
    st.title("📈 실시간 그래프 애니메이션")

    if st.button("이전으로 돌아가기", key="back_to_csv"):
        set_page("csv")  # 이전 페이지로 돌아가기

    if "csv_data" in st.session_state and st.session_state.csv_data is not None:
        csv_data = st.session_state.csv_data

        # Select X and Y axes for real-time visualization
        realtime_x_axis = st.selectbox("X 축 선택 (실시간)", csv_data.columns, key="realtime_x_axis")
        realtime_y_axis = st.selectbox("Y 축 선택 (실시간)", csv_data.columns, key="realtime_y_axis")

        if realtime_x_axis and realtime_y_axis:
            # matplotlib Figure 생성
            fig, ax = plt.subplots()

            # Update 함수 정의 (애니메이션 프레임별 업데이트)
            def update(frame):
                ax.clear()
                x_data = csv_data[realtime_x_axis].iloc[:frame]
                y_data = csv_data[realtime_y_axis].iloc[:frame]
                ax.plot(x_data, y_data, marker="o", linestyle="-", color="b")
                ax.set_xlabel(realtime_x_axis)
                ax.set_ylabel(realtime_y_axis)
                ax.set_title(f"{realtime_x_axis} vs {realtime_y_axis} - Frame {frame}")
                ax.grid(True)

            # Limit frames to improve performance
            max_frames = min(len(csv_data), 100)

            # Create animation
            anim = FuncAnimation(fig, update, frames=max_frames, interval=500)

            # Save animation as GIF
            gif_path = "temp_animation.gif"
            anim.save(gif_path, writer="pillow", fps=10)

            # Read and display the GIF
            with open(gif_path, "rb") as gif_file:
                gif_bytes = gif_file.read()
            st.image(gif_bytes, caption="시간에 따른 데이터 변화")
        else:
            st.warning("X축과 Y축을 모두 선택하세요.")
    else:
        st.warning("CSV 데이터를 먼저 업로드하세요.")



# # if st.button("운동 분석"):
# #     if "x_axis" in st.session_state and "y_axes" in st.session_state:
# #         st.title("📊 운동 분석 결과")
# #         st.write("운동 데이터를 기반으로 분석 결과를 표시합니다.")

# #         if "csv_data" in st.session_state and st.session_state.csv_data is not None:
# #             csv_data = st.session_state.csv_data

# #             try:
# #                 # 사용자가 선택한 열 이름이 존재하는지 확인
# #                 if "Pitch" not in csv_data.columns or "Value" not in csv_data.columns:
# #                     st.warning("'Pitch'와 'Value' 열이 데이터에 포함되어야 합니다.")
# #                 else:
# #                     # Pitch와 Value 데이터 추출
# #                     pitch = csv_data["Pitch"].to_numpy()
# #                     value = csv_data["Value"].to_numpy()

# #                     # 분석 파라미터
# #                     threshold = st.slider("Pitch 기준값 (근방 값)", min_value=0, max_value=100, value=70, step=1)
# #                     near_zero = st.slider("Pitch 근처 0 값의 임계값", min_value=0, max_value=20, value=5, step=1)

# #                     # 운동 횟수 측정 및 Value 값 저장
# #                     count = 0
# #                     values_at_zero = []
# #                     in_motion = False  # 운동 중 상태
# #                     direction = None  # 상승 또는 하강 상태 ('down' 또는 'up')

# #                     for i in range(csv_data.shape[0]):  # CSV 데이터의 행 수를 사용
# #                         if not in_motion:
# #                             # 운동 시작 조건: 70 근방에서 시작하고 하강 중인 상태
# #                             if abs(pitch[i] - threshold) <= 5:
# #                                 in_motion = True
# #                                 direction = 'down'
# #                         else:
# #                             # 운동 중
# #                             if direction == 'down':
# #                                 # 하강 중이고 0 근방에 도달
# #                                 if abs(pitch[i]) <= near_zero:
# #                                     direction = 'up'  # 상승으로 전환
# #                             elif direction == 'up':
# #                                 # 상승 중이고 70 근방에 도달
# #                                 if abs(pitch[i] - threshold) <= 5:
# #                                     count += 1  # 반복 횟수 증가
# #                                     values_at_zero.append(value[i])  # Value 저장
# #                                     in_motion = False  # 운동 종료 후 대기 상태로 전환

# #                     # 분석 결과 표시
# #                     st.write(f"운동 반복 횟수: **{count}회**")
# #                     st.write("운동 종료 시점에서 기록된 Value 값 변화:")

# #                     # 변화 추이 그래프
# #                     fig, ax = plt.subplots(figsize=(10, 5))
# #                     ax.plot(values_at_zero, marker="o", linestyle="-", label="Value 변화 추이")
# #                     ax.set_title("운동 종료 시점의 Value 변화 추이")
# #                     ax.set_xlabel("운동 반복 횟수")
# #                     ax.set_ylabel("Value")
# #                     ax.legend()
# #                     ax.grid()
# #                     st.pyplot(fig)

# #             except Exception as e:
# #                 st.error(f"분석 중 오류 발생: {e}")
# #         else:
# #             st.warning("CSV 데이터를 먼저 업로드하세요.")
# #     else:
# #         st.warning("X축과 Y축을 모두 선택하세요.")



#     if st.button("실시간 그래프"):
#         if "x_axis" in st.session_state and "y_axis" in st.session_state:
#             set_page("realtime")  # Navigate to the real-time graph page
#         else:
#             st.warning("X축과 Y축을 모두 선택하세요.")

# # elif current_page == "realtime":
# #     st.title("📈 실시간 그래프 애니메이션")

# #     if st.button("이전"):
# #             set_page("csv")

# #     if "csv_data" in st.session_state and st.session_state.csv_data is not None:
# #         # Downsample the data
# #         max_points = 100
# #         csv_data = st.session_state.csv_data
# #         if len(csv_data) > max_points:
# #             csv_data = csv_data.iloc[::len(csv_data)//max_points, :]

# #         fig, ax = plt.subplots()

# #         # Update function for animation
# #         def update(frame):
# #             ax.clear()
# #             x_data = csv_data[st.session_state.x_axis][:frame]
# #             # y_data = csv_data[st.session_state.y_axis][:frame]
# #             y_data = csv_data["Value"][:frame]
# #             ax.plot(x_data, y_data, marker="o", linestyle="-")
# #             ax.set_xlabel(st.session_state.x_axis)
# #             ax.set_ylabel(st.session_state.y_axis)
# #             ax.set_title(f"{st.session_state.x_axis} vs {st.session_state.y_axis} - Frame {frame}")
            

# #         # Limit frames to improve performance
# #         max_frames = 100
# #         frames = min(len(csv_data), max_frames)

# #         # Create animation
# #         anim = FuncAnimation(fig, update, frames=frames, interval=300)

# #         # Save animation as GIF
# #         gif_path = "temp_animation.gif"
# #         try:
# #             anim.save(gif_path, writer="pillow", fps=10)

# #             # Read the GIF as binary and display it
# #             with open(gif_path, "rb") as gif_file:
# #                 gif_bytes = gif_file.read()
# #             st.image(gif_bytes, caption="시간에 따른 데이터 변화")  # Display the GIF
# #         except Exception as e:
# #             st.error(f"애니메이션 생성 중 오류 발생: {e}")
# #     if st.button("홈으로 돌아가기"):
# #         set_page("home")

# elif current_page == "realtime":
#     st.title("📈 실시간 그래프 애니메이션")

#     if st.button("이전"):
#         set_page("csv")

#     # CSV 데이터 확인
#     if "csv_data" in st.session_state and st.session_state.csv_data is not None:
#         csv_data = st.session_state.csv_data

#         # CSV 데이터 확인 및 열 이름 추출
#         if not csv_data.empty:
#             columns = csv_data.columns
#         else:
#             st.error("CSV 데이터가 비어 있습니다.")
#             st.stop()

#         # X축과 Y축 선택
#         x_axis = st.selectbox("X 축 선택", columns, key="realtime_x_axis")
#         y_axis = st.selectbox("Y 축 선택", columns, key="realtime_y_axis")

#         if x_axis and y_axis:
#             # Downsample the data
#             max_points = 100
#             if len(csv_data) > max_points:
#                 csv_data = csv_data.iloc[::len(csv_data) // max_points, :]

#             # matplotlib Figure 생성
#             fig, ax = plt.subplots()

#             # Update 함수 정의 (애니메이션 프레임별 업데이트)
#             def update(frame):
#                 ax.clear()
#                 x_data = csv_data[x_axis].iloc[:frame]  # 선택된 X축 데이터
#                 y_data = csv_data[y_axis].iloc[:frame]  # 선택된 Y축 데이터
#                 ax.plot(x_data, y_data, marker="o", linestyle="-", color="b")
#                 ax.set_xlabel(x_axis)  # X축 레이블
#                 ax.set_ylabel(y_axis)  # Y축 레이블
#                 ax.set_title(f"{x_axis} vs {y_axis} - Frame {frame}")
#                 ax.grid(True)

#             # Limit frames to improve performance
#             max_frames = min(len(csv_data), 100)

#             # Create animation
#             anim = FuncAnimation(fig, update, frames=max_frames, interval=300)

#             # Save animation as GIF
#             gif_path = "temp_animation.gif"
#             try:
#                 anim.save(gif_path, writer="pillow", fps=10)

#                 # Read the GIF as binary and display it
#                 with open(gif_path, "rb") as gif_file:
#                     gif_bytes = gif_file.read()
#                 st.image(gif_bytes, caption="시간에 따른 데이터 변화")  # Display the GIF
#             except Exception as e:
#                 st.error(f"애니메이션 생성 중 오류 발생: {e}")
#         else:
#             st.warning("X축과 Y축을 모두 선택하세요.")
#     else:
#         st.warning("CSV 데이터를 먼저 업로드하세요.")

#     if st.button("홈으로 돌아가기"):
#         set_page("home")

# if current_page == "csv":
#     st.title("🎈 CSV 데이터의 축 선택 및 정적 그래프")
#     uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

#     if uploaded_file is not None:
#         try:
#             # Read and display the CSV file
#             csv_data = load_csv(uploaded_file)
#             st.session_state.csv_data = csv_data  # Store data in session state
#             st.write("업로드된 데이터 (처음 100줄):")
#             st.dataframe(csv_data.head(100))  # Display the first 100 rows
    
#             # Select column for X-axis
#             x_axis = st.selectbox("X 축 선택", csv_data.columns)
    
#             # Select columns for Y-axis (multiple features)
#             y_axes = st.multiselect("Y 축 선택 (복수 가능)", csv_data.columns)
    
#             if x_axis and y_axes:
#                 st.session_state.x_axis = x_axis  # Store selected X-axis in session state
#                 st.session_state.y_axes = y_axes  # Store selected Y-axis in session state
    
#                 # Prepare data for plotting
#                 chart_data = csv_data[[x_axis] + y_axes]
#                 chart_data = chart_data.set_index(x_axis)  # Set X-axis as index
    
#                 # Create and render the line chart with multiple Y axes
#                 st.line_chart(chart_data)
                
#                 if st.button("운동 분석"):
#                     if "Pitch" in csv_data.columns and "Time (ms)" in csv_data.columns:
#                         try:
#                             # Pitch와 Time 데이터 추출
#                             pitch = csv_data["Pitch"].to_numpy()
#                             time_ms = csv_data["Time (ms)"].to_numpy()
    
#                             # 분석 파라미터
#                             offset = -35  # 기준 오프셋 값
    
#                             # 운동 횟수 계산 함수 정의
#                             def count_reps(data, time, offset):
#                                 reps = 0
#                                 above_offset = False
#                                 below_offset = False
#                                 below_times = []
#                                 above_times = []
    
#                                 for i in range(1, len(data)):
#                                     if data[i] > offset:
#                                         if below_offset:
#                                             below_offset = False
#                                             above_times.append(time[i])
#                                     elif data[i] <= offset:
#                                         if above_offset:
#                                             above_offset = False
#                                             below_times.append(time[i])
#                                             if len(below_times) > 0 and len(above_times) > 0:
#                                                 if below_times[-1] > above_times[-1]:
#                                                     reps += 1
#                                         below_offset = True
#                                     above_offset = data[i] > offset
#                                 return reps, below_times, above_times
    
#                             # 운동 횟수 계산
#                             reps, below_times, above_times = count_reps(pitch, time_ms, offset)
    
#                             # 결과 출력
#                             st.write(f"총 운동 횟수: {reps}")
    
#                             # 데이터 시각화
#                             st.line_chart({"Pitch": pitch, "Offset": [offset] * len(pitch)})
#                         except Exception as e:
#                             st.error(f"분석 중 오류 발생: {e}")
#                     else:
#                         st.warning("'Pitch'와 'Time' 열이 데이터에 포함되어야 합니다.")

#         except Exception as e:
#             st.error(f"오류가 발생했습니다: {e}")
#     else:
#         st.warning("CSV 파일을 업로드하세요.")


# # 실시간 그래프 분석 추가
# if st.button("실시간 분석"):
#     st.title("📈 실시간 그래프 애니메이션")
#     try:
#         # Downsample the data for better performance
#         max_points = 100
#         if len(csv_data) > max_points:
#             csv_data = csv_data.iloc[::len(csv_data) // max_points, :]

#         # Select X and Y axes for real-time visualization
#         realtime_x_axis = st.selectbox("X 축 선택 (실시간)", csv_data.columns, key="realtime_x_axis")
#         realtime_y_axis = st.selectbox("Y 축 선택 (실시간)", csv_data.columns, key="realtime_y_axis")

#         if realtime_x_axis and realtime_y_axis:
#             # matplotlib Figure 생성
#             fig, ax = plt.subplots()

#             # Update 함수 정의 (애니메이션 프레임별 업데이트)
#             def update(frame):
#                 ax.clear()
#                 x_data = csv_data[realtime_x_axis].iloc[:frame]
#                 y_data = csv_data[realtime_y_axis].iloc[:frame]
#                 ax.plot(x_data, y_data, marker="o", linestyle="-", color="b")
#                 ax.set_xlabel(realtime_x_axis)
#                 ax.set_ylabel(realtime_y_axis)
#                 ax.set_title(f"{realtime_x_axis} vs {realtime_y_axis} - Frame {frame}")
#                 ax.grid(True)

#             # Limit frames to improve performance
#             max_frames = min(len(csv_data), 100)

#             # Create animation
#             anim = FuncAnimation(fig, update, frames=max_frames, interval=300)

#             # Save animation as GIF
#             gif_path = "temp_animation.gif"
#             anim.save(gif_path, writer="pillow", fps=10)

#             # Read and display the GIF
#             with open(gif_path, "rb") as gif_file:
#                 gif_bytes = gif_file.read()
#             st.image(gif_bytes, caption="시간에 따른 데이터 변화")
#         else:
#             st.warning("X축과 Y축을 모두 선택하세요.")
#     except Exception as e:
#         st.error(f"실시간 분석 중 오류 발생: {e}")
# else:
#     st.warning("X축과 Y축을 모두 선택하세요.")



# elif current_page == "analyze":
#     st.title("📊 운동 분석 결과")
#     st.write("운동 데이터를 기반으로 분석 결과를 표시합니다.")

#     if st.button("이전"):
#         set_page("csv")

#     if "csv_data" in st.session_state and st.session_state.csv_data is not None:
#         csv_data = st.session_state.csv_data

#         try:
#             # 사용자가 선택한 열 이름이 존재하는지 확인
#             if "Pitch" not in csv_data.columns or "Value" not in csv_data.columns:
#                 st.warning("'Pitch'와 'Value' 열이 데이터에 포함되어야 합니다.")
#             else:
#                 # Pitch와 Value 데이터 추출
#                 pitch = csv_data["Pitch"].to_numpy()
#                 value = csv_data["Value"].to_numpy()

#                 # 분석 파라미터
#                 threshold = st.slider("Pitch 기준값", min_value=0, max_value=100, value=70, step=1)
#                 near_zero = st.slider("Pitch 근처 0 값의 임계값", min_value=0, max_value=20, value=5, step=1)

#                 # 운동 횟수 측정 및 Value 값 저장
#                 count = 0
#                 values_at_zero = []
#                 in_motion = False

#                 for i in range(csv_data.shape[0]):  # CSV 데이터의 행 수를 사용
#                     if pitch[i] >= threshold and not in_motion:
#                         # 운동 시작
#                         in_motion = True
#                     elif pitch[i] <= near_zero and in_motion:
#                         # 운동 종료 시점
#                         in_motion = False
#                         count += 1
#                         values_at_zero.append(value[i])

#                 # 분석 결과 표시
#                 st.write(f"운동 반복 횟수: **{count}회**")
#                 st.write("운동 종료 시점에서 기록된 Value 값 변화:")

#                 # 변화 추이 그래프
#                 fig, ax = plt.subplots(figsize=(10, 5))
#                 ax.plot(values_at_zero, marker="o", linestyle="-", label="Value 변화 추이")
#                 ax.set_title("운동 종료 시점의 Value 변화 추이")
#                 ax.set_xlabel("운동 반복 횟수")
#                 ax.set_ylabel("Value")
#                 ax.legend()
#                 ax.grid()
#                 st.pyplot(fig)

#         except Exception as e:
#             st.error(f"분석 중 오류 발생: {e}")
#     else:
#         st.warning("CSV 데이터를 먼저 업로드하세요.")

#     if st.button("홈으로 돌아가기"):
#         set_page("home")


# Streamlit 앱 구성
    
 # Streamlit 앱을 새로고침하여 업데이트 반영


# elif st.session_state.page == "rr":
#     st.title("🎈 RR 데이터의 축 선택 및 정적 그래프")

#     # CSV 파일 업로드
#     uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

#     if uploaded_file is not None:
#         csv_file_path = uploaded_file

#         st.title("실시간 CSV 데이터 그래프")
#         st.text("실시간으로 업데이트되는 CSV 파일 데이터를 시각화합니다.")

#         # 실시간 업데이트 주기 설정
#         refresh_rate = st.slider("그래프 업데이트 주기 (초)", min_value=1, max_value=10, value=3)
#         st.text(f"그래프가 {refresh_rate}초마다 업데이트됩니다.")

#         # "그래프 업데이트" 버튼 클릭 시 실시간 데이터 시각화
#         if st.button("그래프 업데이트"):
#             if "last_run_time" not in st.session_state:
#                 st.session_state.last_run_time = time.time()

#             current_time = time.time()
#             elapsed_time = current_time - st.session_state.last_run_time

#             # 주기적으로 그래프를 새로 그림
#             if elapsed_time >= refresh_rate:
#                 plot_live_graph(csv_file_path)  # 실시간 데이터를 그래프로 출력
#                 st.session_state.last_run_time = current_time
#                 st.stop()  # 새로고침 없이 현재 상태 유지

#     # 업로드된 CSV 데이터 표시
#     try:
#         if uploaded_file is not None:
#             # Read and display the CSV file
#             csv_data = pd.read_csv(uploaded_file)
#             st.session_state.csv_data = csv_data  # Store data in session state
#             st.write("업로드된 데이터 (처음 100줄):")
#             st.dataframe(csv_data.head(100))  # Display the first 100 rows

#             # X축 및 Y축 선택
#             x_axis = st.selectbox("X 축 선택", csv_data.columns)
#             y_axes = st.multiselect("Y 축 선택 (복수 가능)", csv_data.columns)

#             if x_axis and y_axes:
#                 # 그래프 데이터 준비
#                 chart_data = csv_data[[x_axis] + y_axes]
#                 chart_data = chart_data.set_index(x_axis)

#                 # 그래프 그리기
#                 st.line_chart(chart_data)
#             else:
#                 st.warning("X축과 Y축을 모두 선택하세요.")
#     except Exception as e:
#         st.error(f"오류가 발생했습니다: {e}")
# else:
#     st.warning("CSV 파일을 업로드하세요.")

# 페이지 제목
if "page" not in st.session_state:
    st.session_state.page = "rs"

if st.session_state.page == "rs":
    # 페이지 제목
    st.title("📊 Muscle Fatigue Analysis")
    st.write("Analyze muscle fatigue using regression and graph plotting.")
    
    # CSV 파일 업로드
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        try:
            # 데이터 로드
            data = pd.read_csv(uploaded_file)
            
            # 필요한 열 확인
            if 'Time (ms)' in data.columns and 'Envelope' in data.columns:
                # 데이터 정규화
                envelope = data['Envelope'] * 200 / np.max(data['Envelope'])
                time_in_seconds = data['Time (ms)'] * 0.001
    
                # 키와 값 준비
                keys_array = np.arange(len(data))
                keys = keys_array.reshape(-1, 1)
                normalized_results = {i: v for i, v in zip(keys_array, envelope)}
                values = np.array(list(normalized_results.values())) * 100
    
                # 선형 회귀 수행
                model = LinearRegression()
                model.fit(keys, values)
                predicted_values = model.predict(keys)
                slope = model.coef_[0]
    
                # 분석 실행 버튼
                if st.button("Perform Regression Analysis"):
                    st.write(f"**Slope (Muscle Fatigue)**: {slope:.4f}")
    
                    # 그래프 그리기
                    fig, ax = plt.subplots(figsize=(6, 6))
                    ax.plot(time_in_seconds, envelope, label="Normalized Envelope", color="blue")
                    ax.scatter(time_in_seconds[keys_array], values, color="blue", label="Original Data")
                    ax.plot(time_in_seconds[keys_array], predicted_values, color="red", label="Linear Regression")
    
                    # 그래프 라벨 및 제목
                    ax.set_title(f"Muscle Fatigue Slope = {slope:.4f}", fontsize=16)
                    ax.set_xlabel("Time (s)", fontsize=12)
                    ax.set_ylabel("Envelope Value (Percentage)", fontsize=12)
                    ax.legend(fontsize=12)
                    ax.grid(True)
    
                    # 그래프 표시
                    st.pyplot(fig)
            else:
                st.error("The required columns ('Time (ms)', 'Envelope') are not found in the uploaded data.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.info("Please upload a CSV file.")

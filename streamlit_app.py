import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy


def update_hight_from_slider():
    st.session_state.hight_input = st.session_state.hight_slider

def update_hight_from_input():
    st.session_state.hight_slider = st.session_state.hight_input

def update_weight_from_slider():
    st.session_state.weight_input = st.session_state.weight_slider

def update_weight_from_input():
    st.session_state.weight_slider = st.session_state.weight_input

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "start"  # Initial start page

# Function to set page
def set_page(page_name):
    st.session_state.page = page_name

# Caching function for loading CSV
@st.cache_data
def load_csv(file):
    return pd.read_csv(file)

# Debugging output
st.write("현재 페이지 상태:", st.session_state.page)

# Render pages based on the session state
if st.session_state.page == "start":
    st.title("📋 앱 시작하기")
    st.text("이 앱은 운동 선택 및 CSV 데이터를 시각화하는 데 사용됩니다.")
    
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
    st.text(
        '저는 ' +  str(st.session_state.sex) + '이며 ' +
        str(st.session_state.age) + '세, ' +
        str(st.session_state.hight) + 'cm, ' +
        str(st.session_state.weight) + 'kg 입니다.'
    ) 

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
        set_page("csv")
    

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
    

elif st.session_state.page == "업데이트":
    st.title("업데이트 예정")
    st.image("https://mblogthumb-phinf.pstatic.net/MjAyMDA3MDJfMjk4/MDAxNTkzNjc1MzM5NjIx.OjEij9RK6k3yFrvDhkRC0_3NXmfFqZiHUS1tyv-Fygwg.Wk6unZQiMuqoJeqfrDhIhUNIpiuj3tumQI_WyP7a2Wog.GIF.sjlhome/Despicable_Me_2_2013_1080p_BRRip_x264_AC3-JYK.mkv_001209458.gif?type=w800", use_container_width=True)
    st.write("Coming soon~")

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

current_page = st.session_state.page

if current_page == "csv":
    st.title("🎈 CSV 데이터의 축 선택 및 정적 그래프")
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read and display the CSV file
            csv_data = load_csv(uploaded_file)
            st.session_state.csv_data = csv_data  # Store data in session state
            st.write("업로드된 데이터 (처음 100줄):")
            st.dataframe(csv_data.head(100))  # Display the first 100 rows
    
            # Select column for X-axis
            x_axis = st.selectbox("X 축 선택", csv_data.columns)
    
            # Select columns for Y-axis (multiple features)
            y_axes = st.multiselect("Y 축 선택 (복수 가능)", csv_data.columns)
    
            if x_axis and y_axes:
                st.session_state.x_axis = x_axis  # Store selected X-axis in session state
                st.session_state.y_axes = y_axes  # Store selected Y-axis in session state
    
                # Prepare data for plotting
                chart_data = csv_data[[x_axis] + y_axes]
                chart_data = chart_data.set_index(x_axis)  # Set X-axis as index
    
                # Create and render the line chart with multiple Y axes
                st.line_chart(chart_data)
                if st.button("운동 분석"):
                    if "x_axis" in st.session_state and "y_axes" in st.session_state:
                        st.title("📊 운동 분석 결과")
                        st.write("운동 데이터를 기반으로 분석 결과를 표시합니다.")

                    if "csv_data" in st.session_state and st.session_state.csv_data is not None:
                        csv_data = st.session_state.csv_data

                        try:
                            # 사용자가 선택한 열 이름이 존재하는지 확인
                            if "Pitch" not in csv_data.columns or "Value" not in csv_data.columns:
                                st.warning("'Pitch'와 'Value' 열이 데이터에 포함되어야 합니다.")
                            else:
                                # Pitch와 Value 데이터 추출
                                pitch = csv_data["Pitch"].to_numpy()
                                value = csv_data["Value"].to_numpy()
            
                                # 분석 파라미터
                                # threshold = st.slider("Pitch 기준값 (근방 값)", min_value=0, max_value=100, value=70, step=1)
                                # near_zero = st.slider("Pitch 근처 0 값의 임계값", min_value=0, max_value=20, value=5, step=1)
                                threshold = 65
                                near_zero = 15
            
                                # 운동 횟수 측정 및 Value 값 저장
                                count = 0
                                values_at_zero = []
                                in_motion = False  # 운동 중 상태
                                direction = None  # 상승 또는 하강 상태 ('down' 또는 'up')
            
                                for i in range(len(pitch)):  # CSV 데이터의 행 수를 사용
                                    if not in_motion:
                                        # 운동 시작 조건: 70 근방에서 시작하고 하강 중인 상태
                                        if abs(pitch[i] - threshold) <= 15:
                                            in_motion = True
                                            direction = 'down'
                                            st.text(in_motion) # 돌고 있다.
                                    else:
                                        # 운동 중
                                        if direction == 'down':
                                            # 하강 중이고 0 근방에 도달
                                            if abs(pitch[i]) <= near_zero:
                                                direction = 'up'  # 상승으로 전환
                                                st.text(direction)
                                        elif direction == 'up':
                                            # 상승 중이고 70 근방에 도달
                                            if abs(pitch[i] - threshold) <= 15:
                                                count += 1  # 반복 횟수 증가
                                                values_at_zero.append(value[i])  # Value 저장
                                                in_motion = False  # 운동 종료 후 대기 상태로 전환
            
                                # 분석 결과 표시
                                st.write(f"운동 반복 횟수: **{count}회**")
                                st.write("운동 종료 시점에서 기록된 Value 값 변화:")
            
                                # 변화 추이 그래프
                                fig, ax = plt.subplots(figsize=(10, 5))
                                ax.plot(values_at_zero, marker="o", linestyle="-", label="Value 변화 추이")
                                ax.set_title("운동 종료 시점의 Value 변화 추이")
                                ax.set_xlabel("운동 반복 횟수")
                                ax.set_ylabel("Value")
                                ax.legend()
                                ax.grid()
                                st.pyplot(fig)
            
                        except Exception as e:
                            st.error(f"분석 중 오류 발생: {e}")
                    else:
                        st.warning("CSV 데이터를 먼저 업로드하세요.")
                else:
                    st.warning("X축과 Y축을 모두 선택하세요.")

            else:
                st.warning("X축과 Y축을 모두 선택하세요.")
        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")
    else:
        st.warning("CSV 파일을 업로드하세요.")

# if st.button("운동 분석"):
#     if "x_axis" in st.session_state and "y_axes" in st.session_state:
#         st.title("📊 운동 분석 결과")
#         st.write("운동 데이터를 기반으로 분석 결과를 표시합니다.")

#         if "csv_data" in st.session_state and st.session_state.csv_data is not None:
#             csv_data = st.session_state.csv_data

#             try:
#                 # 사용자가 선택한 열 이름이 존재하는지 확인
#                 if "Pitch" not in csv_data.columns or "Value" not in csv_data.columns:
#                     st.warning("'Pitch'와 'Value' 열이 데이터에 포함되어야 합니다.")
#                 else:
#                     # Pitch와 Value 데이터 추출
#                     pitch = csv_data["Pitch"].to_numpy()
#                     value = csv_data["Value"].to_numpy()

#                     # 분석 파라미터
#                     threshold = st.slider("Pitch 기준값 (근방 값)", min_value=0, max_value=100, value=70, step=1)
#                     near_zero = st.slider("Pitch 근처 0 값의 임계값", min_value=0, max_value=20, value=5, step=1)

#                     # 운동 횟수 측정 및 Value 값 저장
#                     count = 0
#                     values_at_zero = []
#                     in_motion = False  # 운동 중 상태
#                     direction = None  # 상승 또는 하강 상태 ('down' 또는 'up')

#                     for i in range(csv_data.shape[0]):  # CSV 데이터의 행 수를 사용
#                         if not in_motion:
#                             # 운동 시작 조건: 70 근방에서 시작하고 하강 중인 상태
#                             if abs(pitch[i] - threshold) <= 5:
#                                 in_motion = True
#                                 direction = 'down'
#                         else:
#                             # 운동 중
#                             if direction == 'down':
#                                 # 하강 중이고 0 근방에 도달
#                                 if abs(pitch[i]) <= near_zero:
#                                     direction = 'up'  # 상승으로 전환
#                             elif direction == 'up':
#                                 # 상승 중이고 70 근방에 도달
#                                 if abs(pitch[i] - threshold) <= 5:
#                                     count += 1  # 반복 횟수 증가
#                                     values_at_zero.append(value[i])  # Value 저장
#                                     in_motion = False  # 운동 종료 후 대기 상태로 전환

#                     # 분석 결과 표시
#                     st.write(f"운동 반복 횟수: **{count}회**")
#                     st.write("운동 종료 시점에서 기록된 Value 값 변화:")

#                     # 변화 추이 그래프
#                     fig, ax = plt.subplots(figsize=(10, 5))
#                     ax.plot(values_at_zero, marker="o", linestyle="-", label="Value 변화 추이")
#                     ax.set_title("운동 종료 시점의 Value 변화 추이")
#                     ax.set_xlabel("운동 반복 횟수")
#                     ax.set_ylabel("Value")
#                     ax.legend()
#                     ax.grid()
#                     st.pyplot(fig)

#             except Exception as e:
#                 st.error(f"분석 중 오류 발생: {e}")
#         else:
#             st.warning("CSV 데이터를 먼저 업로드하세요.")
#     else:
#         st.warning("X축과 Y축을 모두 선택하세요.")



    if st.button("실시간 그래프"):
        if "x_axis" in st.session_state and "y_axis" in st.session_state:
            set_page("realtime")  # Navigate to the real-time graph page
        else:
            st.warning("X축과 Y축을 모두 선택하세요.")

elif current_page == "realtime":
    st.title("📈 실시간 그래프 애니메이션")

    if st.button("이전"):
            set_page("csv")

    if "csv_data" in st.session_state and st.session_state.csv_data is not None:
        # Downsample the data
        max_points = 100
        csv_data = st.session_state.csv_data
        if len(csv_data) > max_points:
            csv_data = csv_data.iloc[::len(csv_data)//max_points, :]

        fig, ax = plt.subplots()

        # Update function for animation
        def update(frame):
            ax.clear()
            x_data = csv_data[st.session_state.x_axis][:frame]
            y_data = csv_data[st.session_state.y_axis][:frame]
            ax.plot(x_data, y_data, marker="o", linestyle="-")
            ax.set_xlabel(st.session_state.x_axis)
            ax.set_ylabel(st.session_state.y_axis)
            ax.set_title(f"{st.session_state.x_axis} vs {st.session_state.y_axis} - Frame {frame}")

        # Limit frames to improve performance
        max_frames = 100
        frames = min(len(csv_data), max_frames)

        # Create animation
        anim = FuncAnimation(fig, update, frames=frames, interval=300)

        # Save animation as GIF
        gif_path = "temp_animation.gif"
        try:
            anim.save(gif_path, writer="pillow", fps=10)

            # Read the GIF as binary and display it
            with open(gif_path, "rb") as gif_file:
                gif_bytes = gif_file.read()
            st.image(gif_bytes, caption="시간에 따른 데이터 변화")  # Display the GIF
        except Exception as e:
            st.error(f"애니메이션 생성 중 오류 발생: {e}")
    if st.button("홈으로 돌아가기"):
        set_page("home")

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





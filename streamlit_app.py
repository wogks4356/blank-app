import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io

# Initialize session state for data and navigation
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None
if "page" not in st.session_state:
    st.session_state.page = "home"
if "x_axis" not in st.session_state:
    st.session_state.x_axis = None
if "y_axis" not in st.session_state:
    st.session_state.y_axis = None

# Function to set page
def set_page(page_name):
    st.session_state.page = page_name

# Get the current page
current_page = st.session_state.page

# Home page: Exercise selection
if current_page == "home":
    st.title("🏋️‍♂️ 운동 선택 및 데이터 시각화")
    st.write("운동 이미지를 클릭하거나 CSV 데이터를 업로드하여 관련 페이지로 이동하세요.")

    # Layout for images
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("running.png", caption="러닝", use_container_width=True)
        if st.button("러닝 페이지로 이동", key="running_button"):
            set_page("running")

    with col2:
        st.image("cycling.png", caption="사이클링", use_container_width=True)
        if st.button("사이클링 페이지로 이동", key="cycling_button"):
            set_page("cycling")

    with col3:
        st.image("yoga.png", caption="요가", use_container_width=True)
        if st.button("요가 페이지로 이동", key="yoga_button"):
            set_page("yoga")

    # Button for CSV visualization page
    if st.button("CSV 데이터 시각화"):
        set_page("csv")

# Running page
elif current_page == "running":
    st.title("🏃 러닝 페이지")
    st.write("러닝 관련 정보를 여기에 추가하세요.")
    if st.button("홈으로 돌아가기"):
        set_page("home")

# Cycling page
elif current_page == "cycling":
    st.title("🚴 사이클링 페이지")
    st.write("사이클링 관련 정보를 여기에 추가하세요.")
    if st.button("홈으로 돌아가기"):
        set_page("home")

# Yoga page
elif current_page == "yoga":
    st.title("🧘 요가 페이지")
    st.write("요가 관련 정보를 여기에 추가하세요.")
    if st.button("홈으로 돌아가기"):
        set_page("home")

# CSV visualization page
elif current_page == "csv":
    st.title("🎈 CSV 데이터의 축 선택 및 정적 그래프")
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file
            csv_data = pd.read_csv(uploaded_file)
            st.session_state.csv_data = csv_data
            st.success("CSV 파일이 업로드되었습니다!")
            st.write("업로드된 데이터:")
            st.dataframe(csv_data.head())  # Show first few rows
        except Exception as e:
            st.error(f"파일 처리 중 오류 발생: {e}")

    if "csv_data" in st.session_state and st.session_state.csv_data is not None:
        st.subheader("📊 X, Y 축 선택 및 정적 그래프")
        columns = st.session_state.csv_data.columns.tolist()
        st.session_state.x_axis = st.selectbox("X 축 선택", columns, key="x_axis_selector")
        st.session_state.y_axis = st.selectbox("Y 축 선택", columns, key="y_axis_selector")

        if st.session_state.x_axis and st.session_state.y_axis:
            # Draw static graph
            fig, ax = plt.subplots()
            ax.plot(
                st.session_state.csv_data[st.session_state.x_axis],
                st.session_state.csv_data[st.session_state.y_axis],
                marker="o"
            )
            ax.set_xlabel(st.session_state.x_axis)
            ax.set_ylabel(st.session_state.y_axis)
            ax.set_title(f"{st.session_state.x_axis} vs {st.session_state.y_axis}")
            st.pyplot(fig)

        # Button to navigate to the animation page
        if st.button("실시간 그래프"):
            if st.session_state.x_axis and st.session_state.y_axis:
                set_page("animation")
            else:
                st.warning("X축과 Y축을 모두 선택하세요.")

    if st.button("홈으로 돌아가기"):
        set_page("home")

# Animation page
elif current_page == "animation":
    st.title("🎥 실시간 그래프 애니메이션")

    if "csv_data" in st.session_state and st.session_state.csv_data is not None:
        # Downsample the data
        max_points = 500
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
        max_frames = 500
        frames = min(len(csv_data), max_frames)

        # Create animation
        anim = FuncAnimation(fig, update, frames=frames, interval=200)

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

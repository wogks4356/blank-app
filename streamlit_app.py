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
        # [수정] 러닝 이미지 링크를 여기에 입력하세요.
        st.image("data:image/jpeg;base64,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", caption="삼두", use_container_width=True)
        if st.button("삼두 페이지로 이동", key="running_button"):
            set_page("threedoo")

    with col2:
        # [수정] 사이클링 이미지 링크를 여기에 입력하세요.
        st.image("data:image/jpeg;base64,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", caption="사레레", use_container_width=True)
        if st.button("사레레 페이지로 이동", key="cycling_button"):
            set_page("side_raise")

    with col3:
        # [수정] 요가 이미지 링크를 여기에 입력하세요.
        st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEOGWEEDCo16VeeLhuwsNZQu3krtihDtHz-g&s", caption="이두", use_container_width=True)
        if st.button("이두 페이지로 이동", key="yoga_button"):
            set_page("twodoo")

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

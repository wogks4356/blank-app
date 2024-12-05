import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize session state for data and navigation
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None
if "page" not in st.session_state:
    st.session_state.page = 1
if "x_axis" not in st.session_state:
    st.session_state.x_axis = None
if "y_axis" not in st.session_state:
    st.session_state.y_axis = None

# Function to set page
def set_page(page):
    st.session_state.page = page

# Get the current page
current_page = st.session_state.page

# Page 1: Axis selection and static graph
if current_page == 1:
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

        # Button to navigate to the next page
        if st.button("실시간 그래프"):
            if st.session_state.x_axis and st.session_state.y_axis:
                set_page(2)  # Update the page number
            else:
                st.warning("X축과 Y축을 모두 선택하세요.")

# Page 2: Real-time Graph Animation
elif current_page == 2:
    st.title("📈 실시간 밀리는 그래프 애니메이션")

    if "csv_data" in st.session_state and st.session_state.csv_data is not None:
        # Downsample the data for performance
        max_points = 500
        csv_data = st.session_state.csv_data
        if len(csv_data) > max_points:
            csv_data = csv_data.iloc[::len(csv_data)//max_points, :]

        fig, ax = plt.subplots()

        # Determine x-axis window size (e.g., 50 points at a time)
        window_size = 50
        x_data = csv_data[st.session_state.x_axis]
        y_data = csv_data[st.session_state.y_axis]

        def update(frame):
            start = max(0, frame - window_size)
            end = frame
            ax.clear()
            ax.plot(x_data[start:end], y_data[start:end], marker="o", linestyle="-")
            ax.set_xlim(x_data[start], x_data[start] + (x_data[end-1] - x_data[start]))
            ax.set_xlabel(st.session_state.x_axis)
            ax.set_ylabel(st.session_state.y_axis)
            ax.set_title(f"{st.session_state.x_axis} vs {st.session_state.y_axis} - Frame {frame}")

        # Limit frames to improve performance
        max_frames = len(x_data)

        # Create animation
        anim = FuncAnimation(fig, update, frames=max_frames, interval=200)

        # Render the graph in real-time
        st.pyplot(fig)

    # Back button to return to the first page
    if st.button("이전"):
        set_page(1)  # Navigate back to Page 1

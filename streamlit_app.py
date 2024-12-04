import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import io

# Initialize session state
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

# Streamlit App
st.title("🎈 My 실시간 그래프 애니메이션")
st.write(
    """
    CSV 파일을 업로드하고 정적인 그래프를 확인한 후, 실시간처럼 움직이는 그래프(GIF)를 생성합니다.
    """
)

# File uploader
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file is not None:
    try:
        # Read the CSV file
        st.session_state.csv_data = pd.read_csv(uploaded_file)
        st.success("CSV 파일이 업로드되었습니다!")
        st.write("업로드된 데이터:")
        st.dataframe(st.session_state.csv_data.head())  # Show first few rows
    except Exception as e:
        st.error(f"파일 처리 중 오류 발생: {e}")

# Plot static graph
if st.session_state.csv_data is not None and not st.session_state.csv_data.empty:
    columns = st.session_state.csv_data.columns.tolist()
    x_axis = st.selectbox("X 축 선택", columns)
    y_axis = st.selectbox("Y 축 선택", columns)

    if x_axis and y_axis:
        # Static graph
        st.subheader("📊 정적 그래프")
        fig, ax = plt.subplots()
        ax.plot(st.session_state.csv_data[x_axis], st.session_state.csv_data[y_axis], marker="o")
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{x_axis} vs {y_axis}")
        st.pyplot(fig)

        # Animated GIF creation
        st.subheader("🎥 애니메이션 생성")
        fig, ax = plt.subplots()

        def update(frame):
            ax.clear()
            ax.plot(
                st.session_state.csv_data[x_axis][:frame],
                st.session_state.csv_data[y_axis][:frame],
                marker="o",
            )
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"{x_axis} vs {y_axis} - Frame {frame}")

        # Create animation
        frames = len(st.session_state.csv_data)
        anim = FuncAnimation(fig, update, frames=frames, interval=100)

        # Save animation as GIF
        gif_buffer = io.BytesIO()
        try:
            anim.save(gif_buffer, writer="pillow", fps=5)  # Removed 'format' argument
            gif_buffer.seek(0)
            st.image(gif_buffer, format="gif", caption="실시간 그래프 애니메이션")
        except Exception as e:
            st.error(f"GIF 생성 중 오류 발생: {e}")
    else:
        st.error("X축과 Y축 데이터를 선택하세요.")
else:
    st.warning("CSV 파일이 없거나 데이터가 비어 있습니다.")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import imageio
import io

# Initialize session state
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

# Streamlit App
st.title("🎈 My 실시간 그래프 애니메이션")
st.write(
    """
    CSV 파일을 업로드하고 실시간처럼 움직이는 그래프(GIF)를 생성합니다.
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

# Generate GIF animation
if st.session_state.csv_data is not None and not st.session_state.csv_data.empty:
    columns = st.session_state.csv_data.columns.tolist()
    x_axis = st.selectbox("X 축 선택", columns)
    y_axis = st.selectbox("Y 축 선택", columns)

    # 데이터 전처리: NaN 제거
    st.session_state.csv_data = st.session_state.csv_data.dropna(subset=[x_axis, y_axis])
    if st.session_state.csv_data.empty:
        st.error("NaN 값을 제거한 후 데이터가 비어 있습니다. CSV 파일을 확인하세요.")

    if x_axis and y_axis:
        fig, ax = plt.subplots()
        images = []  # List to store frame images

        def update(frame):
            ax.clear()
            if frame > 0:
                try:
                    # 프레임 데이터 확인
                    x_data = st.session_state.csv_data[x_axis][:frame]
                    y_data = st.session_state.csv_data[y_axis][:frame]
                    st.write(f"프레임 {frame}: X 데이터: {x_data.values}, Y 데이터: {y_data.values}")  # 디버깅

                    # 그래프 그리기
                    ax.plot(x_data, y_data, marker="o")
                    ax.set_xlabel(x_axis)
                    ax.set_ylabel(y_axis)
                    ax.set_title(f"{x_axis} vs {y_axis} - Frame {frame}")

                    # 프레임을 이미지로 저장
                    buf = io.BytesIO()
                    plt.savefig(buf, format="png")
                    buf.seek(0)
                    images.append(imageio.imread(buf))
                    buf.close()
                    st.write(f"프레임 {frame} 저장 완료")  # 디버깅 메시지
                except Exception as e:
                    st.error(f"프레임 {frame} 처리 중 오류 발생: {e}")

        # Create animation
        frames = len(st.session_state.csv_data)
        st.write(f"프레임 개수: {frames}")  # Debug
        anim = FuncAnimation(fig, update, frames=frames, interval=100)

        # Check generated images
        st.write(f"생성된 이미지 개수: {len(images)}")  # Debug

        # Generate GIF
        if len(images) == 0:
            st.error("GIF 생성을 위한 프레임이 없습니다. 데이터를 확인하세요.")
        else:
            gif_buffer = io.BytesIO()
            imageio.mimsave(gif_buffer, images, format="GIF", fps=5)
            gif_buffer.seek(0)
            st.image(gif_buffer, format="gif", caption="실시간 그래프 애니메이션")
    else:
        st.error("X축과 Y축 데이터를 선택하세요.")
else:
    st.warning("CSV 파일이 없거나 데이터가 비어 있습니다.")

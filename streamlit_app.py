import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Initialize session state
if "csv_data" not in st.session_state:
    st.session_state.csv_data = None

if "show_graph" not in st.session_state:
    st.session_state.show_graph = False

# Function to reset state
def reset_state():
    st.session_state.csv_data = None
    st.session_state.show_graph = False

# Streamlit App
st.title("🎈 My 데이터 시각화 앱")
st.write(
    """
    CSV 파일을 업로드하고 데이터를 시각화합니다.
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
        st.dataframe(st.session_state.csv_data)
    except Exception as e:
        st.error(f"파일 처리 중 오류 발생: {e}")

# Next button to show graph
if st.session_state.csv_data is not None and st.button("다음"):
    st.session_state.show_graph = True

# Graph display
if st.session_state.show_graph:
    st.subheader("📊 데이터 그래프")
    
    # Select columns for X and Y axes
    columns = st.session_state.csv_data.columns.tolist()
    x_axis = st.selectbox("X 축 선택", columns)
    y_axis = st.selectbox("Y 축 선택", columns)
    
    if x_axis and y_axis:
        # Plot the graph
        fig, ax = plt.subplots()
        ax.plot(st.session_state.csv_data[x_axis], st.session_state.csv_data[y_axis], marker='o')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{x_axis} vs {y_axis}")
        st.pyplot(fig)
    else:
        st.warning("X축과 Y축을 선택하세요.")

# Reset button
if st.session_state.show_graph and st.button("다시 시작"):
    reset_state()

import streamlit as st
import pandas as pd

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
    st.write("이 앱은 운동 선택 및 CSV 데이터를 시각화하는 데 사용됩니다.")
    
    if st.button("Run"):
        set_page("home")  # Navigate to the home page

elif st.session_state.page == "home":
    st.title("🏋️‍♂️ 운동 선택 및 데이터 시각화")

    # Layout for images with clickable buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("삼두.jpg", caption="삼두", use_column_width=True)
        if st.button("삼두 페이지로 이동"):
            set_page("csv")

    with col2:
        st.image("사레레.jpg", caption="사레레", use_column_width=True)
        if st.button("사레레 페이지로 이동"):
            set_page("csv")

    with col3:
        st.image("이두.jpg", caption="이두", use_column_width=True)
        if st.button("이두 페이지로 이동"):
            set_page("csv")

elif st.session_state.page == "csv":
    st.title("🎈 CSV 데이터 시각화")
    st.write("CSV 데이터를 업로드하세요.")

    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read and display the CSV file
            csv_data = load_csv(uploaded_file)
            st.write("업로드된 데이터 (처음 100줄):")
            st.dataframe(csv_data.head(100))  # Display the first 100 rows

            # Select columns for graph
            if not csv_data.empty:
                x_axis = st.selectbox("X 축 선택", csv_data.columns)
                y_axis = st.selectbox("Y 축 선택", csv_data.columns)

                if x_axis and y_axis:
                    st.line_chart(csv_data[[x_axis, y_axis]].head(100))  # Chart limited to 100 rows

        except Exception as e:
            st.error(f"파일 처리 중 오류 발생: {e}")

    # Back button to navigate home
    if st.button("홈으로 돌아가기"):
        set_page("home")

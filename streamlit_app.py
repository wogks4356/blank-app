import streamlit as st
import pandas as pd

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to set page
def set_page(page_name):
    st.session_state.page = page_name

# 디버깅 출력
st.write("현재 페이지 상태:", st.session_state.page)

# Render pages based on the session state
if st.session_state.page == "home":
    st.title("🏋️‍♂️ 운동 선택 및 데이터 시각화")

    # CSS for clickable images
    st.markdown(
        """
        <style>
        .clickable-image {
            width: 150px;
            height: 150px;
            object-fit: cover;
            cursor: pointer;
            margin: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Layout for images with links to pages
    col1, col2, col3 = st.columns(3)

    with col1:
        # 삼두 이미지 링크
        st.markdown(
            """
            <a href="#" onclick="window.location.reload(); document.getElementById('page_state').value = 'csv';">
                <img src="https://via.placeholder.com/150?text=삼두" class="clickable-image" alt="삼두">
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("삼두 페이지로 이동"):
            set_page("csv")

    with col2:
        # 사레레 이미지 링크
        st.markdown(
            """
            <a href="#" onclick="window.location.reload(); document.getElementById('page_state').value = 'csv';">
                <img src="https://via.placeholder.com/150?text=사레레" class="clickable-image" alt="사레레">
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("사레레 페이지로 이동"):
            set_page("csv")

    with col3:
        # 이두 이미지 링크
        st.markdown(
            """
            <a href="#" onclick="window.location.reload(); document.getElementById('page_state').value = 'csv';">
                <img src="https://via.placeholder.com/150?text=이두" class="clickable-image" alt="이두">
            </a>
            """,
            unsafe_allow_html=True,
        )
        if st.button("이두 페이지로 이동"):
            set_page("csv")

elif st.session_state.page == "csv":
    st.title("🎈 CSV 데이터 시각화")
    st.write("CSV 데이터를 업로드하세요.")

    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file
            csv_data = pd.read_csv(uploaded_file)
            st.write("업로드된 데이터:")
            st.dataframe(csv_data.head())

            # Select columns for graph
            if csv_data is not None:
                x_axis = st.selectbox("X 축 선택", csv_data.columns)
                y_axis = st.selectbox("Y 축 선택", csv_data.columns)

                if x_axis and y_axis:
                    st.line_chart(csv_data[[x_axis, y_axis]])

        except Exception as e:
            st.error(f"파일 처리 중 오류 발생: {e}")

    # Back button
    if st.button("홈으로 돌아가기"):
        set_page("home")

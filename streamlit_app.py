import streamlit as st
import pandas as pd

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "home"

# Function to set page
def set_page(page_name):
    st.session_state.page = page_name
    st.experimental_set_query_params(page=page_name)

query_params = st.query_params
st.write("쿼리 파라미터:", query_params)  # 디버깅 출력

# Handle query params safely
target_page = query_params.get("page", "home")  # 기본값을 "home"으로 설정
if isinstance(target_page, list):  # target_page가 리스트인 경우 처리
    target_page = target_page[0]

st.write("타겟 페이지:", target_page)  # 디버깅 출력
if target_page and st.session_state.page != target_page:
    st.session_state.page = target_page

# 디버깅 출력: 현재 페이지 상태
st.write("현재 페이지 상태:", st.session_state.page)
# Page: Exercise selection
# Render pages based on the session state
if st.session_state.page == "home":
    st.title("🏋️‍♂️ 운동 선택 및 데이터 시각화")

    # CSS for image size and button-like behavior
    st.markdown(
        """
        <style>
        .custom-image {
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

    # Layout for images
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("삼두 페이지로 이동"):
            set_page("csv")

    with col2:
        if st.button("사레레 페이지로 이동"):
            set_page("csv")

    with col3:
        if st.button("이두 페이지로 이동"):
            set_page("csv")


# Page: CSV Visualization
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

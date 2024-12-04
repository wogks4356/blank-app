import streamlit as st
import pandas as pd

# Define the session state for pagination
if "page" not in st.session_state:
    st.session_state.page = 1

def go_next_page():
    st.session_state.page += 1

def go_previous_page():
    st.session_state.page -= 1

# App Title
st.title("🎈 My 나의 app")
st.write(
    """
    Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).
    
    우리 같이 즐겨보아요.
    
    우리는 언제 끝나는 걸까요?? 우리 같이 해봐요.
    """
)

# Page 1: File upload and data visualization
if st.session_state.page == 1:
    st.subheader("페이지 1: CSV 파일 업로드 및 데이터 시각화")
    uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

    if uploaded_file is not None:
        try:
            # Read the CSV file
            data = pd.read_csv(uploaded_file)
            st.write("업로드된 데이터:")
            st.dataframe(data)  # Display the dataframe

            # Plotting
            st.write("📊 데이터 그래프")
            st.write("각 열 중 원하는 데이터를 선택하여 그래프를 그려보세요.")
            
            # Select columns for x and y axes
            columns = data.columns.tolist()
            x_axis = st.selectbox("X 축 선택", columns)
            y_axis = st.selectbox("Y 축 선택", columns)

            if x_axis and y_axis:
                # Use Streamlit's built-in line chart
                chart_data = data[[x_axis, y_axis]].set_index(x_axis)
                st.line_chart(chart_data)
            else:
                st.write("X축과 Y축을 선택하세요.")

        except Exception as e:
            st.error(f"파일을 처리하는 중 오류가 발생했습니다: {e}")

    # Add a "Next" button
    if st.button("다음"):
        go_next_page()

# Page 2: Next page content
elif st.session_state.page == 2:
    st.subheader("페이지 2: 다음 페이지")
    st.write("여기에서 다음 페이지의 내용을 작성할 수 있습니다.")
    
    # Add a "Previous" button
    if st.button("이전"):
        go_previous_page()

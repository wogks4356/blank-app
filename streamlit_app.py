import streamlit as st
import pandas as pd
import serial
import time
import matplotlib.pyplot as plt

# Initialize the session state for pagination and data
if "page" not in st.session_state:
    st.session_state.page = 1
if "arduino_data" not in st.session_state:
    st.session_state.arduino_data = []

def go_next_page():
    st.session_state.page += 1

def go_previous_page():
    st.session_state.page -= 1

# App Title
st.title("🎈 My 아두이노 실시간 데이터 그래프")
st.write(
    """
    아두이노에서 데이터를 받아 실시간으로 그래프를 그립니다.
    """
)

# Page 1: Connect to Arduino and receive data
if st.session_state.page == 1:
    st.subheader("페이지 1: 아두이노 연결 및 데이터 수신")
    
    # Serial port settings
    port = st.text_input("아두이노 포트를 입력하세요 (예: COM3 또는 /dev/ttyUSB0)", value="/dev/ttyUSB0")
    baud_rate = st.number_input("보드레이트를 입력하세요", value=9600, step=100)
    
    # Start/Stop toggle
    if st.button("연결 시작"):
        try:
            ser = serial.Serial(port, baud_rate, timeout=1)
            st.success(f"{port}에 연결되었습니다!")
            
            # Read data from Arduino
            st.write("데이터 수신 중...")
            while True:
                line = ser.readline().decode('utf-8').strip()  # Read a line from Arduino
                if line:
                    st.session_state.arduino_data.append(float(line))  # Convert to float and store
                    st.write(f"수신 데이터: {line}")  # Display received data
                    time.sleep(0.1)  # Slight delay to avoid overloading

                # Break condition (button to stop)
                if st.button("연결 중지"):
                    ser.close()
                    st.success("연결을 종료했습니다.")
                    break
        except Exception as e:
            st.error(f"아두이노 연결 오류: {e}")

    # Add a "Next" button to move to visualization
    if st.button("다음"):
        if len(st.session_state.arduino_data) > 0:
            go_next_page()
        else:
            st.warning("데이터를 먼저 수신하세요.")

# Page 2: Real-time visualization
elif st.session_state.page == 2:
    st.subheader("페이지 2: 실시간 데이터 그래프")
    
    # Display real-time graph
    if len(st.session_state.arduino_data) > 0:
        st.write("아두이노 데이터 실시간 그래프:")
        
        # Plotting the data
        fig, ax = plt.subplots()
        ax.plot(st.session_state.arduino_data, label="아두이노 데이터")
        ax.set_xlabel("Time")
        ax.set_ylabel("Signal")
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("데이터가 없습니다. 첫 번째 페이지로 돌아가 데이터를 수신하세요.")

    # Option to go back to the previous page
    if st.button("이전"):
        go_previous_page()

import streamlit as st
import serial
import matplotlib.pyplot as plt
import time

# Initialize session state for data storage
if "arduino_data" not in st.session_state:
    st.session_state.arduino_data = []

if "is_receiving" not in st.session_state:
    st.session_state.is_receiving = False

# Function to start serial communication
def start_serial(port, baud_rate):
    try:
        ser = serial.Serial(port, baud_rate, timeout=1)
        st.session_state.is_receiving = True
        st.success(f"{port}에 연결되었습니다!")
        return ser
    except Exception as e:
        st.error(f"아두이노 연결 오류: {e}")
        return None

# Function to stop serial communication
def stop_serial(serial_connection):
    if serial_connection and serial_connection.is_open:
        serial_connection.close()
        st.session_state.is_receiving = False
        st.success("연결을 종료했습니다.")

# Streamlit App
st.title("🎈 My 아두이노 실시간 데이터 그래프")
st.write(
    """
    아두이노에서 데이터를 받아 실시간으로 그래프를 그립니다.
    """
)

# User input for Arduino settings
port = st.text_input("아두이노 포트를 입력하세요 (예: COM3 또는 /dev/ttyUSB0)", value="/dev/ttyUSB0")
baud_rate = st.number_input("보드레이트를 입력하세요", value=9600, step=100)

# Start and Stop buttons
ser = None
if st.button("연결 시작") and not st.session_state.is_receiving:
    ser = start_serial(port, baud_rate)

if st.button("연결 중지") and st.session_state.is_receiving:
    stop_serial(ser)

# Real-time data display and graph
if st.session_state.is_receiving:
    try:
        st.write("데이터 수신 중...")
        placeholder = st.empty()  # Placeholder for the graph
        
        while True:
            if ser and ser.in_waiting > 0:
                # Read line from Arduino
                line = ser.readline().decode('utf-8').strip()
                if line:
                    # Append new data to session state
                    st.session_state.arduino_data.append(float(line))
                    st.write(f"수신 데이터: {line}")

                # Plot the graph
                fig, ax = plt.subplots()
                ax.plot(st.session_state.arduino_data, label="아두이노 데이터")
                ax.set_xlabel("Time")
                ax.set_ylabel("Signal")
                ax.legend()
                placeholder.pyplot(fig)
                
                # Add delay to avoid overloading
                time.sleep(0.1)

    except Exception as e:
        st.error(f"데이터 수신 중 오류 발생: {e}")


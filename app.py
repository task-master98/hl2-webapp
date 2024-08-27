import streamlit as st
import asyncio
import websockets
import time
import os

FRAME_PATH = "frames/captured_frame.png"

async def send_command(command):
    try:
        async with websockets.connect("wss://hololens-sense-9bd80b459134.herokuapp.com/") as websocket:
            await websocket.send(command)
            print(f"Sent command : {command}")
    except Exception as e:
        print(f"Error sending command: {e}")

def send_command_async(command):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send_command(command))

st.title("Remote Control for HoloLens")

col1, col2 = st.columns([3, 1])

with st.container():
    with col1:
        if st.button("Increase Distance"):
            send_command_async("increase_distance")

        if st.button("Decrease Distance"):
            send_command_async("decrease_distance")

        if st.button("Toggle Left"):
            send_command_async("toggle_left")       

        st.subheader("Increase Quad Size")

        left_slider = st.slider("Select aspect ratio of Quad", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
        st.write(f"Quad Aspect Ratio: {left_slider}")        

        st.subheader("Change Filter Mode")
        if st.button("Filter Point"):
            send_command_async("filter_point")
        
        if st.button("Filter Bilinear"):
            send_command_async("filter_bilinear")
        
        if st.button("Filter Trilinear"):
            send_command_async("filter_trilinear")
        
        if st.button("Toggle Grayscale"):
            send_command_async("toggle_grayscale")
    

    with col2:
        st.write("")

        if st.button("⬆️ Up"):
            send_command_async("move_up")
        
        col2_left, col2_right = st.columns(2)

        with col2_left:
            if st.button("⬅️ Left"):
                send_command_async("move_left")
        
        with col2_right:
            if st.button("➡️ Right"):
                send_command_async("move_right")
        
        st.write("")  # Add some space below the buttons
        if st.button("⬇️ Down"):
            send_command_async("move_down")
        
        st.subheader("Move Quad to Position")
        if st.button("Bottom Left"):
            send_command_async("bottom_left")

        if st.button("Bottom Right"):
            send_command_async("bottom_right")

        if st.button("Top Left"):
            send_command_async("top_left")

        if st.button("Top Right"):
            send_command_async("top_right")
        
        if st.button("Capture Frame"):

            send_command_async("capture_frame")
            st.success("Capture command sent")

            time.sleep(3)

            if os.path.exists(FRAME_PATH):
                st.image(FRAME_PATH, caption="Captured Frame", use_column_width=True)
                with open(FRAME_PATH, "rb") as file:
                    st.download_button(label="Download captured frame", data=file, file_name="captured_frame.png")
            else:
                st.warning("Frame not yet available. Please try again")

if st.session_state.get('previous_slider_value') != left_slider:
    st.session_state['previous_slider_value'] = left_slider
    send_command_async(f"slider_value:{left_slider}")
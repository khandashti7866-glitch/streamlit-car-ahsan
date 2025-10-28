import streamlit as st
import time
import random

st.set_page_config(page_title="Extreme Car Driving (Simple Version)", layout="centered")

# Initialize session variables
if "car_x" not in st.session_state:
    st.session_state.car_x = 3
if "speed" not in st.session_state:
    st.session_state.speed = 0
if "distance" not in st.session_state:
    st.session_state.distance = 0
if "obstacles" not in st.session_state:
    st.session_state.obstacles = [{"x": random.randint(1, 5), "y": 0}]
if "game_over" not in st.session_state:
    st.session_state.game_over = False

road_width = 5
road_height = 10

def draw_road():
    grid = [["⬛"] * road_width for _ in range(road_height)]
    for obs in st.session_state.obstacles:
        if 0 <= obs["y"] < road_height:
            grid[obs["y"]][obs["x"] - 1] = "🚧"
    grid[road_height - 1][st.session_state.car_x - 1] = "🚗"
    for row in grid:
        st.write("".join(row))

def move_obstacles():
    for obs in st.session_state.obstacles:
        obs["y"] += 1
    st.session_state.obstacles = [o for o in st.session_state.obstacles if o["y"] < road_height]
    if random.random() < 0.3:
        st.session_state.obstacles.append({"x": random.randint(1, road_width), "y": 0})

def check_collision():
    for obs in st.session_state.obstacles:
        if obs["y"] == road_height - 1 and obs["x"] == st.session_state.car_x:
            st.session_state.game_over = True

# Controls
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("⬅️ Left") and st.session_state.car_x > 1:
        st.session_state.car_x -= 1
with col2:
    if st.button("Accelerate ⏩"):
        st.session_state.speed += 1
with col3:
    if st.button("➡️ Right") and st.session_state.car_x < road_width:
        st.session_state.car_x += 1

st.write(f"🏎️ Speed: {st.session_state.speed}")
st.write(f"📏 Distance: {st.session_state.distance}")

if st.session_state.game_over:
    st.error("💥 Crash! Game Over 💥")
    if st.button("Restart 🔁"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
else:
    draw_road()
    move_obstacles()
    check_collision()
    st.session_state.distance += st.session_state.speed
    time.sleep(max(0.3 - st.session_state.speed * 0.02, 0.05))
    st.rerun()

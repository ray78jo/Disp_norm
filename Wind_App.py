import streamlit as st
import math

# Function to calculate true wind speed and direction
def calculate_true_wind(rel_wind_speed, rel_wind_direction, ship_heading, ship_speed):
    # Convert angles to radians
    theta_rel_wind = math.radians(rel_wind_direction)
    theta_heading = math.radians(ship_heading)

    # Components of the relative wind vector
    rel_wind_x = rel_wind_speed * math.cos(theta_rel_wind)
    rel_wind_y = rel_wind_speed * math.sin(theta_rel_wind)

    # Components of the ship's velocity vector
    ship_speed_x = ship_speed * math.cos(theta_heading)
    ship_speed_y = ship_speed * math.sin(theta_heading)

    # Combine the vectors to get the true wind vector components
    true_wind_x = rel_wind_x + ship_speed_x
    true_wind_y = rel_wind_y + ship_speed_y

    # Calculate true wind speed
    true_wind_speed = math.sqrt(true_wind_x**2 + true_wind_y**2)

    # Calculate true wind direction
    true_wind_direction = math.degrees(math.atan2(true_wind_y, true_wind_x))

    # Adjust the angle to ensure it falls within the 0-360° range
    if true_wind_direction < 0:
        true_wind_direction += 360

    return true_wind_speed, true_wind_direction

# Streamlit user interface
st.title('True Wind Calculator')

st.sidebar.header('Input Parameters')

# Input parameters
rel_wind_speed = st.sidebar.slider('Relative Wind Speed (knots)', 0, 99, 10)
rel_wind_direction = st.sidebar.slider('Relative Wind Direction (°)', 0, 359, 0)
ship_heading = st.sidebar.slider('Course of the Ship (°)', 0, 359, 0)
ship_speed = st.sidebar.slider('Speed of the Ship (knots)', 5, 20, 10)

# Calculate true wind speed and direction
true_wind_speed, true_wind_direction = calculate_true_wind(
    rel_wind_speed, rel_wind_direction, ship_heading, ship_speed
)

# Display the results
st.write(f'### True Wind Speed: {true_wind_speed:.2f} knots')
st.write(f'### True Wind Direction: {true_wind_direction:.2f}° (relative to north)')


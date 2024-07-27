import streamlit as st
import math
import plotly.graph_objects as go

def calculate_wind_components(speed, direction):
    direction_rad = direction * math.pi / 180
    x_component = speed * math.cos(direction_rad)
    y_component = speed * math.sin(direction_rad)
    return x_component, y_component

def plot_wind(ship_heading, true_wind_direction, relative_wind_direction, true_wind_speed, relative_wind_speed, ship_speed, title):
    max_radius = max(true_wind_speed, relative_wind_speed, ship_speed) + 5

    fig = go.Figure()

    # Plot ship's heading with line
    fig.add_trace(go.Scatterpolar(
        r=[0, ship_speed],
        theta=[ship_heading, ship_heading],
        mode='lines+markers',
        name='Ship Heading',
        line=dict(color='blue'),
        marker=dict(color='blue', symbol='circle', size=5)
    ))

    # Plot true wind direction with line
    fig.add_trace(go.Scatterpolar(
        r=[0, true_wind_speed],
        theta=[true_wind_direction, true_wind_direction],
        mode='lines+markers',
        name='True Wind Direction',
        line=dict(color='red'),
        marker=dict(color='red', symbol='circle', size=5)
    ))

    # Plot relative wind direction with line
    relative_wind_plot_direction = (ship_heading + relative_wind_direction) % 360
    fig.add_trace(go.Scatterpolar(
        r=[0, relative_wind_speed],
        theta=[relative_wind_plot_direction, relative_wind_plot_direction],
        mode='lines+markers',
        name='Relative Wind Direction',
        line=dict(color='green', dash='dash'),
        marker=dict(color='green', symbol='circle', size=5)
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, max_radius]),
            angularaxis=dict(direction="clockwise", rotation=90)
        ),
        showlegend=True,
        title=title
    )

    return fig

def main():
    st.title("Wind Calculator")

    col1, col2 = st.columns(2)

    with col1:
        # Option to select the type of calculation
        calc_type = st.radio(
            "True to Relative or Relative to True",
            ('Relative Wind to True Wind', 'True Wind to Relative Wind')
        )

    with col2:
        # Option to select wind speed units
        wind_speed_unit = st.selectbox(
            "Knots or m/sec",
            ('knots', 'm/s')
        )

    speed_conversion = 1.0 if wind_speed_unit == 'knots' else 0.514444

    col3, col4 = st.columns(2)

    with col3:
        if calc_type == 'Relative Wind to True Wind':
            # User inputs for relative wind
            st.header("Relative Wind Input")
            relative_wind_direction = st.slider("Relative Wind Direction (°)", min_value=0, max_value=360, step=30, value=0)
            relative_wind_speed = st.number_input(f"Relative Wind Speed ({wind_speed_unit})", min_value=0.0, value=20.0)
        else:
            # User inputs for true wind
            st.header("True Wind Input")
            true_wind_direction = st.slider("True Wind Direction (°)", min_value=0, max_value=360, step=30, value=0)
            true_wind_speed = st.number_input(f"True Wind Speed ({wind_speed_unit})", min_value=0.0, value=32.43)

    with col4:
        # User inputs for ship's heading and speed
        st.header("Heading & Spd")
        ship_heading = st.slider("Heading (°)", min_value=0, max_value=360, step=30, value=0)
        ship_speed = st.number_input("Ship Speed (knots)", min_value=0.0, value=15.0)

    if calc_type == 'Relative Wind to True Wind':
        # Convert angles to radians
        theta_rwd = (relative_wind_direction + ship_heading) % 360 * math.pi / 180
        theta_heading = ship_heading * math.pi / 180

        # Calculate components of the relative wind vector
        rwd_x = relative_wind_speed * speed_conversion * math.cos(theta_rwd)
        rwd_y = relative_wind_speed * speed_conversion * math.sin(theta_rwd)

        # Calculate components of the ship's velocity vector
        ship_speed_x = ship_speed * math.cos(theta_heading)
        ship_speed_y = ship_speed * math.sin(theta_heading)

        # Combine vectors to get the true wind vector components
        true_wind_x = rwd_x - ship_speed_x
        true_wind_y = rwd_y - ship_speed_y

        # Calculate true wind speed and direction
        true_wind_speed = math.sqrt(true_wind_x ** 2 + true_wind_y ** 2) / speed_conversion
        true_wind_speed_knots = true_wind_speed * speed_conversion if wind_speed_unit == 'm/s' else true_wind_speed
        true_wind_direction_rad = math.atan2(true_wind_y, true_wind_x)
        true_wind_direction = (true_wind_direction_rad * 180 / math.pi) % 360
        if true_wind_direction < 0:
            true_wind_direction += 360

        st.subheader("True Wind Results")
        if wind_speed_unit == 'knots':
            st.markdown(f"**<span style='color:brown'>True Wind Speed: {int(true_wind_speed)} {wind_speed_unit}</span>**", unsafe_allow_html=True)
        else:
            st.markdown(f"**<span style='color:brown'>True Wind Speed: {int(true_wind_speed)} {wind_speed_unit} ({int(true_wind_speed_knots)} knots)</span>**", unsafe_allow_html=True)
        st.markdown(f"**<span style='color:brown'>True Wind Direction: {int(true_wind_direction)}° (relative to north)</span>**", unsafe_allow_html=True)

        st.plotly_chart(plot_wind(ship_heading, true_wind_direction, relative_wind_direction, true_wind_speed, relative_wind_speed, ship_speed, "True Wind Calculation"))

    elif calc_type == 'True Wind to Relative Wind':
        # Convert angles to radians
        theta_true_wind = true_wind_direction * math.pi / 180
        theta_heading = ship_heading * math.pi / 180

        # Calculate components of the true wind vector
        true_wind_x = true_wind_speed * speed_conversion * math.cos(theta_true_wind)
        true_wind_y = true_wind_speed * speed_conversion * math.sin(theta_true_wind)

        # Calculate components of the ship's velocity vector
        ship_speed_x = ship_speed * math.cos(theta_heading)
        ship_speed_y = ship_speed * math.sin(theta_heading)

        # Combine vectors to get the relative wind vector components
        rwd_x = true_wind_x + ship_speed_x
        rwd_y = true_wind_y + ship_speed_y

        # Calculate relative wind speed and direction
        relative_wind_speed = math.sqrt(rwd_x ** 2 + rwd_y ** 2) / speed_conversion
        relative_wind_speed_knots = relative_wind_speed * speed_conversion if wind_speed_unit == 'm/s' else relative_wind_speed
        relative_wind_direction_rad = math.atan2(rwd_y, rwd_x)
        relative_wind_direction = (relative_wind_direction_rad * 180 / math.pi - ship_heading) % 360
        if relative_wind_direction < 0:
            relative_wind_direction += 360

        st.subheader("Relative Wind Results")
        if wind_speed_unit == 'knots':
            st.markdown(f"**<span style='color:brown'>Relative Wind Speed: {int(relative_wind_speed)} {wind_speed_unit}</span>**", unsafe_allow_html=True)
        else:
            st.markdown(f"**<span style='color:brown'>Relative Wind Speed: {int(relative_wind_speed)} {wind_speed_unit} ({int(relative_wind_speed_knots)} knots)</span>**", unsafe_allow_html=True)
        st.markdown(f"**<span style='color:brown'>Relative Wind Direction: {int(relative_wind_direction)}° (relative to the ship's heading)</span>**", unsafe_allow_html=True)

        st.plotly_chart(plot_wind(ship_heading, true_wind_direction, relative_wind_direction, true_wind_speed, relative_wind_speed, ship_speed, "Relative Wind Calculation"))

if __name__ == "__main__":
    main()

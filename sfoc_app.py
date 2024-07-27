import streamlit as st

def calculate_cons_day(sfoc, power):
    return sfoc * power / 1000000 * 24

def calculate_sfoc(cons_day, power):
    return cons_day * 1000000 / 24 / power

def calculate_power(cons_day, sfoc):
    return cons_day * 1000000 / 24 / sfoc

# Styling
st.markdown("""
    <style>
        .stApp {
            background-color: #1e1e1e;
            color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        .stTitle {
            color: #00ffff; /* Fluorescent blue */
            font-size: 48px;
            font-weight: bold;
            text-align: center;
            margin-bottom: 40px; /* Added space between title and buttons */
        }
        .stHeader {
            color: #ffffff; /* Bright white */
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            margin-top: 40px; /* Added space between buttons and Calculate text */
        }
        .stSlider>div>div>div {
            color: #61dafb;
        }
        .stButton>button {
            background-color: #61dafb;
            color: white;
            font-size: 18px;
        }
        .stMarkdown h3 {
            color: #61dafb;
            font-size: 38px; /* Reduced output font size by 20% */
        }
        .stSlider label {
            font-size: 22px; /* Increased font size by 25% */
            color: #ffffff; /* White color for labels */
        }
        .stNumberInput>div>div>input {
            background-color: #333333;
            color: #f0f2f6;
        }
        .button-box {
            display: flex;
            justify-content: center;
            margin-bottom: 40px; /* Added space between buttons and Calculate text */
        }
        .button-box > div {
            flex: 1;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="stTitle">SFOC - Power - Cons Calculator</h1>', unsafe_allow_html=True)

# User option selection
st.markdown('<div class="button-box">', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])

# Initialize option
if "option" not in st.session_state:
    st.session_state.option = 'Calculate Cons/Day'  # Default to 'Calculate Cons/Day'

with col1:
    if st.button('Cons/Day'):
        st.session_state.option = 'Calculate Cons/Day'
with col2:
    if st.button('SFOC'):
        st.session_state.option = 'Calculate SFOC'
with col3:
    if st.button('Power'):
        st.session_state.option = 'Calculate Power'

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.option == 'Calculate Cons/Day':
    st.markdown('<h2 class="stHeader">Calculate Cons/Day</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    sfoc = col1.slider('Enter SFOC (kg/kWh):', min_value=150, max_value=250, value=150)
    power = col2.slider('Enter Power (kWh):', min_value=1000, max_value=100000, value=10000)
    result = calculate_cons_day(sfoc, power)
    st.markdown(f'**<span style="color:#61dafb; font-size: 38px;">Daily Fuel Consumption: {result:.1f} mts/day</span>**', unsafe_allow_html=True)

elif st.session_state.option == 'Calculate SFOC':
    st.markdown('<h2 class="stHeader">Calculate SFOC</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    cons_day = col1.slider('Enter Cons/Day (mts/day):', min_value=10, max_value=75, value=25)
    power = col2.slider('Enter Power (kWh):', min_value=1000, max_value=100000, value=10000)
    result = calculate_sfoc(cons_day, power)
    st.markdown(f'**<span style="color:#61dafb; font-size: 38px;">SFOC: {result:.1f} kg/kWh</span>**', unsafe_allow_html=True)

elif st.session_state.option == 'Calculate Power':
    st.markdown('<h2 class="stHeader">Calculate Power</h2>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    cons_day = col1.slider('Enter Cons/Day (mts/day):', min_value=10, max_value=75, value=25)
    sfoc = col2.slider('Enter SFOC (kg/kWh):', min_value=150, max_value=250, value=150)
    result = calculate_power(cons_day, sfoc)
    st.markdown(f'**<span style="color:#61dafb; font-size: 38px;">Power: {result:.1f} kWh</span>**', unsafe_allow_html=True)


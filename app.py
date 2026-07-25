import streamlit as st
import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Instant Kundli & Birth Chart Finder",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Custom Styling
# -----------------------------
st.markdown("""
    <style>
    .main-title {
        font-size: 2.4rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(90deg, #7b2ff7, #f107a3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #888;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔮 Instant Kundli & Birth Chart Finder</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Discover your Rising Sign, Moon Sign, and Dominant House</div>', unsafe_allow_html=True)

# -----------------------------
# Reference Data
# -----------------------------
ZODIAC_SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
    "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]

HOUSES = [1, 4, 7, 10]

TRAIT_ENERGY = {
    "Fire/Passion": "bold, driven, and quick to act",
    "Earth/Stability": "grounded, practical, and dependable",
    "Air/Curiosity": "curious, communicative, and idea-driven",
    "Water/Intuition": "intuitive, emotional, and deeply perceptive"
}

TRAIT_HOUSE_BIAS = {
    "Fire/Passion": 1,
    "Earth/Stability": 4,
    "Air/Curiosity": 7,
    "Water/Intuition": 10
}

# -----------------------------
# Calculation Function
# -----------------------------
def calculate_chart(name, birth_date, birth_time, birth_place, trait):
    """
    A simplified, self-contained algorithmic model that generates a
    Rising Sign, Moon Sign, and Dominant House based on numerological
    combinations of birth time, birth date, and selected personality trait.
    This is a fun, illustrative model and does not use real ephemeris data.
    """
    hour = birth_time.hour
    minute = birth_time.minute
    day = birth_date.day
    month = birth_date.month

    # Rising Sign: derived from hour + minute distribution across 12 signs
    rising_index = (hour * 2 + minute // 30) % 12
    rising_sign = ZODIAC_SIGNS[rising_index]

    # Moon Sign: derived from birth day + month, offset by name length for personalization
    name_seed = sum(ord(ch) for ch in name.strip()) if name.strip() else 7
    moon_index = (day + month + name_seed) % 12
    moon_sign = ZODIAC_SIGNS[moon_index]

    # Dominant House: blend of trait bias and time-based value
    time_component = (hour + minute) % 4
    trait_bias_index = HOUSES.index(TRAIT_HOUSE_BIAS[trait])
    house_index = (trait_bias_index + time_component) % 4
    dominant_house = HOUSES[house_index]

    # Personalized reading
    energy_desc = TRAIT_ENERGY[trait]
    reading = (
        f"{name.strip() or 'You'} carry the essence of {rising_sign} rising, giving you a first impression that is "
        f"{energy_desc}. With your Moon in {moon_sign}, your inner emotional world seeks expression through "
        f"reflection and personal growth. Your energy centers strongly in the {dominant_house}th house, "
        f"marking {birth_place.strip() or 'your journey'} as a place where your core purpose continues to unfold."
    )

    return {
        "rising_sign": rising_sign,
        "moon_sign": moon_sign,
        "dominant_house": dominant_house,
        "reading": reading
    }

# -----------------------------
# Input Form
# -----------------------------
with st.container():
    st.subheader("📝 Enter Your Birth Details")

    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name", placeholder="e.g., Aarav Sharma")
        birth_date = st.date_input(
            "Birth Date",
            value=datetime.date(2000, 1, 1),
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date.today()
        )
    with col2:
        birth_time = st.time_input("Birth Time", value=datetime.time(12, 0))
        birth_place = st.text_input("Birth City & Country", placeholder="e.g., Jaipur, India")

    trait = st.selectbox(
        "Select your core personality trait",
        ["Fire/Passion", "Earth/Stability", "Air/Curiosity", "Water/Intuition"]
    )

    generate = st.button("✨ Generate My Kundli", use_container_width=True, type="primary")

# -----------------------------
# Output Section
# -----------------------------
if generate:
    if not full_name.strip() or not birth_place.strip():
        st.warning("Please fill in your Full Name and Birth City & Country to continue.")
    else:
        result = calculate_chart(full_name, birth_date, birth_time, birth_place, trait)

        st.balloons()

        st.markdown("---")
        st.subheader(f"🌟 {full_name.strip()}'s Birth Chart Summary")

        with st.container():
            m1, m2, m3 = st.columns(3)
            m1.metric("🌅 Rising Sign (Lagna)", result["rising_sign"])
            m2.metric("🌙 Moon Sign", result["moon_sign"])
            m3.metric("🏠 Dominant House", f"{result['dominant_house']}th House")

        with st.container():
            st.markdown("### 📖 Your Personalized Reading")
            st.info(result["reading"])

        with st.container():
            st.markdown("### 📍 Birth Details")
            details_col1, details_col2 = st.columns(2)
            with details_col1:
                st.write(f"**Date of Birth:** {birth_date.strftime('%B %d, %Y')}")
                st.write(f"**Time of Birth:** {birth_time.strftime('%I:%M %p')}")
            with details_col2:
                st.write(f"**Place of Birth:** {birth_place.strip()}")
                st.write(f"**Core Trait:** {trait}")

        st.caption("✨ This chart is generated using a simplified illustrative algorithm for entertainment purposes and is not based on real astronomical ephemeris data.")

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit — Instant Kundli & Birth Chart Finder")

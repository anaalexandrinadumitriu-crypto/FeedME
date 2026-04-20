import streamlit as st

st.set_page_config(layout="wide")

# Global button styling for sharp corners and touching buttons
st.markdown(
    """
    <style>
    button, .stButton button, .stButton>button, div.stButton>button {
        border-radius: 0 !important;
        margin: 0 !important;
        height: 60px !important;
        font-size: 18px !important;
    }
    div.row-widget.stButton {
        margin: 0 !important;
        padding: 0 !important;
    }
    div[data-testid="column"] > div {
        padding: 0 !important;
    }
    section[data-testid="stHorizontalBlock"], .stColumns {
        gap: 0 !important;
    }
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Top navigation buttons
col1, col2, col3 = st.columns(3, gap="small")
with col1:
    if st.button("Digital Pantry", use_container_width=True):
        st.session_state.page = 'pantry'
with col2:
    if st.button("Feed Me", use_container_width=True):
        st.session_state.page = 'feed_me'
with col3:
    if st.button("My Recipes", use_container_width=True):
        st.session_state.page = 'recipes'

# Logo and title (only show on home page)
if st.session_state.page == 'home':
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("Logo.png", width=1000)
        st.markdown("<div style='text-align: center; font-size: 60px; font-weight: bold;'>FeedME</div>", unsafe_allow_html=True)
   
# Feed Me page
elif st.session_state.page == 'feed_me':
    st.header(" Feed Me")
    st.write("Describe what kind of meal you want:")

    meal_description = st.text_area("What are you in the mood for?", height=100)

    col1, col2, col3 = st.columns(3)
    with col1:
        meal_type = st.selectbox("Meal type", ["Meal", "Snack", "Dessert"])
    with col2:
        if meal_type == "Snack":
            time_options = ["Quick (< 10 min)", "Medium (10-30 min)", "Long (> 30 min)"]
        else:
            time_options = ["Quick (< 30 min)", "Medium (30-60 min)", "Long (> 60 min)"]
        cooking_time = st.selectbox("How long should it take?", time_options)
    with col3:
        difficulty = st.slider("Cooking Difficulty (1-5)", 1, 5, 3)

    if st.button("Generate Recipe", type="primary"):
        st.write("Recipe generation would happen here...")

# Digital Pantry page
elif st.session_state.page == 'pantry':
    st.header(" Digital Pantry")
    st.write("Take a picture of your ingredients:")

    tab1, tab2 = st.tabs(["Upload Image", "Take Photo"])

    with tab1:
        uploaded_file = st.file_uploader("Upload an image of your food", type=['png', 'jpg', 'jpeg'])
        image_file = uploaded_file

    with tab2:
        camera_file = st.camera_input("Take a picture with your camera")
        image_file = camera_file

    if image_file is not None:
        st.image(image_file, caption="Captured Image")
        st.write("AI would analyze this image to detect ingredients...")

    st.subheader("Detected Ingredients:")
    st.write("No ingredients detected yet. Upload an image or take a photo to get started!")

# My Recipes page
elif st.session_state.page == 'recipes':
    st.header(" My Recipes")
    st.subheader("Recent Recipes")
    st.write("Your 5 most recent recipes will appear here...")

    st.subheader("Saved Recipes")
    st.write("Your liked and saved recipes will appear here...")

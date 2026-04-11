import streamlit as st

# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# Top navigation buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Feed Me", use_container_width=True):
        st.session_state.page = 'feed_me'
with col2:
    if st.button("Digital Pantry", use_container_width=True):
        st.session_state.page = 'pantry'
with col3:
    if st.button("My Recipes", use_container_width=True):
        st.session_state.page = 'recipes'

# Logo and title (only show on home page)
if st.session_state.page == 'home':
    col1, col2, col3 = st.columns(3)
    with col2:
        st.image("Logo.png", width=200)
        st.markdown("<div style='text-align: center; font-size: xx-large; font-weight: bold;'>FeedME</div>", unsafe_allow_html=True)
    st.write("What ingredients do you have today?")

# Feed Me page
elif st.session_state.page == 'feed_me':
    st.header("🍽️ Feed Me")
    st.write("Describe what kind of meal you want:")

    meal_description = st.text_area("What are you in the mood for?", height=100)

    col1, col2, col3 = st.columns(3)
    with col1:
        difficulty = st.slider("Cooking Difficulty (1-5)", 1, 5, 3)
    with col2:
        time_options = ["Quick (< 30 min)", "Medium (30-60 min)", "Long (> 60 min)"]
        cooking_time = st.selectbox("How long should it take?", time_options)
    with col3:
        meal_type = st.selectbox("Meal type", ["Meal", "Snack", "Dessert"])

    if st.button("Generate Recipe", type="primary"):
        st.write("Recipe generation would happen here...")

# Digital Pantry page
elif st.session_state.page == 'pantry':
    st.header("🏪 Digital Pantry")
    st.write("Take a picture of your ingredients:")

    uploaded_file = st.file_uploader("Upload an image of your food", type=['png', 'jpg', 'jpeg'])

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image")
        st.write("AI would analyze this image to detect ingredients...")

    st.subheader("Detected Ingredients:")
    st.write("No ingredients detected yet. Upload an image to get started!")

# My Recipes page
elif st.session_state.page == 'recipes':
    st.header("📖 My Recipes")
    st.subheader("Recent Recipes")
    st.write("Your 5 most recent recipes will appear here...")

    st.subheader("Saved Recipes")
    st.write("Your liked and saved recipes will appear here...")

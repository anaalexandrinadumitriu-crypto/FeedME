import streamlit as st
from openai import OpenAI
import base64
import json
from streamlit_local_storage import LocalStorage

local_storage = LocalStorage()

st.set_page_config(layout="wide")

# Global button styling for sharp corners and touching buttons
st.markdown(
    """
    <style>
    button, .stButton button, .stButton>button, div.stButton>button {
        border-radius: 0 !important;
        margin: 0 !important;
        height: 90px !important;
        font-size: 18px !important;
        zoom: 1.3 !important;
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
col1, col2, col3 = st.columns(3, gap=None)
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
        value = local_storage.getItem('saved_ingredients')
        if value is None:
            saved_ingredients = []
        else:
            saved_ingredients = json.loads(value)
        if not saved_ingredients:
            st.warning("No saved ingredients in your digital pantry. Please add some ingredients first.")
        else:
            api_key = st.secrets.get("OPENAI_API_KEY")
            if api_key:
                client = OpenAI(api_key=api_key)
                saved_ings_str = ", ".join(saved_ingredients)
                prompt = f"Generate a {meal_type} recipe using these ingredients: {saved_ings_str}. Description: {meal_description}. Cooking time: {cooking_time}. Difficulty level: {difficulty}/5. Provide a detailed recipe with title, ingredients list (using the provided ingredients where possible), and step-by-step instructions."
                messages = [{"role": "user", "content": prompt}]
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                        max_tokens=1000
                    )
                    recipe = response.choices[0].message.content.strip()
                    st.session_state['current_recipe'] = recipe
                    st.subheader("Generated Recipe:")
                    st.write(recipe)
                    # Optionally save to recent recipes
                    value = local_storage.getItem('recent_recipes')
                    if value is None:
                        recent_recipes = []
                    else:
                        recent_recipes = json.loads(value)
                    recent_recipes.append(recipe)
                    if len(recent_recipes) > 5:
                        recent_recipes = recent_recipes[-5:]
                    local_storage.setItem('recent_recipes', json.dumps(recent_recipes))
                except Exception as e:
                    st.error(f"Error generating recipe: {str(e)}")
            else:
                st.error("OpenAI API key not configured. Please set it in st.secrets.")

    if 'current_recipe' in st.session_state:
        if st.button("Save Recipe"):
            value = local_storage.getItem('saved_recipes')
            if value is None:
                saved_recipes = []
            else:
                saved_recipes = json.loads(value)
            saved_recipes.append(st.session_state['current_recipe'])
            local_storage.setItem('saved_recipes', json.dumps(saved_recipes))
            st.success("Recipe saved!")

# Digital Pantry page
elif st.session_state.page == 'pantry':
    st.header(" Digital Pantry")
    st.write("Take a picture of your ingredients:")

    tab1, tab2 = st.tabs(["Upload Image", "Take Photo"])

    image_file = None

    with tab1:
        uploaded_file = st.file_uploader("Upload an image of your food", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            image_file = uploaded_file

    with tab2:
        camera_file = st.camera_input("Take a picture with your camera")
        if camera_file is not None:
            image_file = camera_file

    if image_file is not None:
        st.image(image_file, caption="Captured Image")
        
        if st.button("Detect Ingredients"):
            # Analyze image with OpenAI
            api_key = st.secrets.get("OPENAI_API_KEY")
            if api_key:
                client = OpenAI(api_key=api_key)
                # Encode image to base64
                image_bytes = image_file.read()
                base64_string = base64.b64encode(image_bytes).decode('utf-8')
                
                # Prepare message for OpenAI
                messages = [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Identify the ingredients visible in this image. Return ONLY a comma-separated list of ingredient names with no other text or explanation."},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_string}"}}
                        ]
                    }
                ]
                
                try:
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=messages,
                        max_tokens=300
                    )
                    st.session_state['detected_ingredients'] = response.choices[0].message.content.strip()
                except Exception as e:
                    st.session_state['detected_ingredients'] = f"Error analyzing image: {str(e)}"
            else:
                st.session_state['detected_ingredients'] = "OpenAI API key not configured. Please set it in st.secrets."

    st.subheader("Detected Ingredients:")
    if 'detected_ingredients' in st.session_state:
        st.write(st.session_state['detected_ingredients'])
        if st.button("Save to Pantry"):
            # Parse detected ingredients (assuming comma-separated)
            ingredients_list = [ing.strip() for ing in st.session_state['detected_ingredients'].split(',')]
            # Add to saved ingredients, avoiding duplicates
            value = local_storage.getItem('saved_ingredients')
            if value is None:
                saved_ingredients = []
            else:
                saved_ingredients = json.loads(value)
            for ing in ingredients_list:
                if ing and ing not in saved_ingredients:
                    saved_ingredients.append(ing)
            local_storage.setItem('saved_ingredients', json.dumps(saved_ingredients))
            st.success("Ingredients saved to pantry!")
    else:
        st.write("No ingredients detected yet. Upload an image or take a photo, then click 'Detect Ingredients' to get started!")

    st.subheader("Saved Ingredients:")
    value = local_storage.getItem('saved_ingredients')
    if value is None:
        saved_ingredients = []
    else:
        saved_ingredients = json.loads(value)
    if saved_ingredients:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(", ".join(saved_ingredients))
        with col2:
            if st.button("Clear All"):
                local_storage.setItem('saved_ingredients', json.dumps([]))
                st.rerun()
    else:
        st.write("No saved ingredients yet. Detect ingredients from an image and save them!")

# My Recipes page
elif st.session_state.page == 'recipes':
    st.header(" My Recipes")
    st.subheader("Recent Recipes")
    value = local_storage.getItem('recent_recipes')
    if value is None:
        recent_recipes = []
    else:
        recent_recipes = json.loads(value)
    if recent_recipes:
        for i, recipe in enumerate(reversed(recent_recipes), 1):
            st.markdown(f"**Recipe {i}:**")
            st.write(recipe)
            st.markdown("---")
    else:
        st.write("No recent recipes yet. Generate some in the Feed Me tab!")

    st.subheader("Saved Recipes")
    value = local_storage.getItem('saved_recipes')
    if value is None:
        saved_recipes = []
    else:
        saved_recipes = json.loads(value)
    if saved_recipes:
        for i, recipe in enumerate(saved_recipes, 1):
            st.markdown(f"**Saved Recipe {i}:**")
            st.write(recipe)
            st.markdown("---")
    else:
        st.write("No saved recipes yet. Save some from the Feed Me tab!")

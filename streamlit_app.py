import streamlit as st

col1, col2, col3 = st.columns(3)
with col2:
    st.image("Logo.png", width=200)
    st.markdown("<div style='text-align: center; font-size: xx-large; font-weight: bold;'>FeedME</div>", unsafe_allow_html=True)
st.write(
    "What ingredients do you have today?"
)

import streamlit as st


st.markdown("""
<style>
.custom-font {
    font-size: 22px;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)




def styled_write(text):
    """
    This function takes in the text and applies styling.
    """
    st.markdown(f'<p class="custom-font">{text}</p>', unsafe_allow_html=True)
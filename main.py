import streamlit as st
from few_shot_posts import FewShotPosts
from generate_post import post_generator

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hindi", "Hinglish"]

def main():
    st.title("Social Media Post Generator")
    col1, col2, col3 = st.columns(3)
    fsp = FewShotPosts()
    with col1:
        selected_tag = st.selectbox("Topic", options=fsp.get_tags())

    with col2:
        selected_length = st.selectbox("Length", options=length_options)
        
    with col3:
        selected_lang = st.selectbox("Language", options=language_options)

    if st.button("Generate"):
        post = post_generator(selected_length, selected_lang, selected_tag)
        st.write(post)
        
if __name__ == '__main__':
    main()
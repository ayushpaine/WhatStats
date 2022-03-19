import streamlit as st
import preprocessor
import helper
from PIL import Image
import matplotlib.pyplot as plt

img = Image.open('./images/dataanalysis.png')

st.set_page_config(
    layout="wide", page_title="WhatStats - Stats for your WhatsApp chats", page_icon=img)

st.sidebar.image('./images/whatsapplogo.png', width=100)
st.sidebar.markdown(
        '# **WhatStats**', unsafe_allow_html=True
)

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    file_name = uploaded_file.name

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    dataset, uni, store, words_count = preprocessor.preprocess(data)

    user_list = dataset['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'All')

    most_used_msg_count = st.slider('Enter Number of Most Used Words to be Displayed', min_value = 1, max_value = helper.find_max_word_count(words_count), value = int(helper.find_max_word_count(words_count)/3))
    st.write(most_used_msg_count)

    most_active_user_count = st.slider('Enter Number of Most Active Users to be Displayed', min_value = 1, max_value = len(uni), value = int(len(uni)/2))
    st.write(most_active_user_count)  

    selected_user = st.sidebar.selectbox("Show Statistics of", user_list)

    if(st.sidebar.button("Show Statistics")):

        number_of_messages, words, number_of_media, modified_dataset, links = helper.fetch_stats(
            selected_user, dataset, file_name)

        st.write(modified_dataset.astype('object'))

        col11, col12, col13, col14, col21 = st.columns((1.25,1,1,1,1))
       
        with col11:
            st.header("Total Messages")
            st.title(number_of_messages)

        with col12:
            st.header("Total Words")
            st.title(len(words))

        with col13:
            st.header("Total Media")
            st.title(number_of_media)

        with col14:
            st.header("Total Links")
            st.title(len(links))
       
        with col21:
            st.header("Total letters")
            st.title(sum(len(i) for i in words))

        if selected_user == "All":
            st.title('Most Active Users')

            helper.plot_bar_graph(uni, most_active_user_count)

        most_common_words = helper.most_used_words(selected_user, store, words_count, most_used_msg_count)

        st.title("Most Common Words")        
        st.dataframe(most_common_words)


        
           
            
            

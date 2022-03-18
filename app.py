import streamlit as st
import preprocessor
import helper
from PIL import Image
from helper import *

img = Image.open('Data-Analysis-256.png')

st.set_page_config(
    layout="wide", page_title="WhatStats - Stats for your WhatsApp chats", page_icon=img)

st.sidebar.title("WhatsApp Chat Statistics")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:

    file_name = uploaded_file.name

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    dataset, uni = preprocessor.preprocess(data)

    user_list = dataset['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, 'All')

    selected_user = st.sidebar.selectbox("Show Statistics of", user_list)

    if(st.sidebar.button("Show Statistics")):

        number_of_messages, words, number_of_media, modified_dataset, links = helper.fetch_stats(
            selected_user, dataset, file_name)

        st.write(modified_dataset.astype('object'))

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(number_of_messages)

        with col2:
            st.header("Total Words")
            st.title(len(words))

        with col3:
            st.header("Total Media")
            st.title(number_of_media)

        with col4:
            st.header("Total Links")
            st.title(len(links))

        if selected_user == "All":
            st.title('Most Active Users')
            
            curr = len(uni["User"])

            plot_bar_graph(uni, curr)
        
        dataset_wc = helper.gen_wordcloud(selected_user, dataset)
        st.image(dataset_wc)
           
            
            

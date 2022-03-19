import numpy as np
from sklearn import datasets
import streamlit as st
from urlextract import URLExtract
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
from collections import Counter
import pandas as pd

extract = URLExtract()

def fetch_stats(selected_user, dataset, file_name):

    if(selected_user == 'All'):
        number_of_messages = dataset.shape[0]
        number_of_media = dataset[dataset['message'] == '<Media omitted>'].shape[0]
        
        words = []
        
        for message in dataset['message']:
            words.extend(message.split())
        modified_dataset = dataset

        links = []

        for message in modified_dataset['message']:
            links.extend(extract.find_urls(message))

        st.title("Overall Statistics for" + " " + "chat with" + " " +file_name[19:-4])

        return number_of_messages, words, number_of_media, modified_dataset, links
    
    else:
        user_dataset = dataset[dataset['user'] == selected_user]
        number_of_messages = user_dataset.shape[0]
        number_of_media = user_dataset[user_dataset['message'] == '<Media omitted>'].shape[0]
        words = []

        for message in user_dataset['message']:
            words.extend(message.split())

        modified_dataset = user_dataset.drop(columns = ['user'])
        modified_dataset.index = np.arange(len(modified_dataset))

        links = []

        for message in modified_dataset['message']:
            links.extend(extract.find_urls(message))

        st.title("Statistics for"+ " " + selected_user +" "+ "in Chat with" + " " + file_name[19:-4])

        return number_of_messages, words, number_of_media, modified_dataset, links
        


def plot_bar_graph(uni, most_active_user_count):
    fig = px.bar(uni.iloc[0:most_active_user_count], x='Count',
                         y='User_short', text='Count', height = 850, width = 1300, hover_data = {
                             'User_short': False,
                             'User': True,
                             'Count': True
                         })
    
    fig.update_traces(width = 1)
    fig.update_traces(textfont_size=12, textangle=0, textposition="auto", cliponaxis=False)
    fig.update_yaxes(tickangle=-35)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(ticksuffix="  ", automargin=False, tickmode = 'linear')
    fig.update_layout(yaxis_title_text="")
    fig.update_layout(xaxis_title_text="")
    fig.update_layout(margin=dict(l= 100, r=0, t=30, b=50))
    st.plotly_chart(fig, use_container_width=True)

def most_used_words(selected_user, store, words, most_used_msg_count):

    if selected_user != 'All':
        store = store[store['user'] == selected_user]
   
    if(most_used_msg_count > len(words)):
        most_used_msg_count = len(words)

    most_common_words = pd.DataFrame(Counter(words).most_common(most_used_msg_count))
    most_common_words.columns = ["Word", "Count"]

    return most_common_words
        
def find_max_word_count(words_count):
    if len(words_count) > 100:
        return 100
    else :
        return len(words_count)


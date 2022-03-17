from matplotlib.pyplot import bar
import numpy as np
import streamlit as st
from urlextract import URLExtract
import pandas as pd
import plotly.express as px

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
        


def plot_bar_graph(uni, total_rank):
    fig = px.bar(uni.iloc[0:total_rank], x='Count',
                         y='User', text='Count', height = 850, width = 1300, custom_data = ['User_tooltip', 'Count'])
    
    fig.update_traces(width = 1)
    fig.update_traces(textfont_size=12, textangle=0, textposition="auto", cliponaxis=False)
    fig.update_layout(hovermode="y unified")
    fig.update_yaxes(tickangle=-35)
    fig.update_xaxes(showticklabels=False)
    fig.update_yaxes(ticksuffix="  ", automargin=False, tickmode = 'linear')
    fig.update_layout(yaxis_title_text="")
    fig.update_layout(xaxis_title_text="")
    fig.update_layout(margin=dict(l= 100, r=0, t=30, b=50))
    st.plotly_chart(fig, use_container_width=True)

import numpy as np
import streamlit as st
from urlextract import URLExtract
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

def most_active_users(dataset):
    uni = pd.DataFrame(dataset['user'].value_counts())
    uni.rename(columns = {'user': 'Count'}, inplace = True)
    uni['User'] = uni.index
    uni.reset_index(drop = True)
    uni.sort_values(by = 'Count', ascending = False, inplace = True)

    return uni
        

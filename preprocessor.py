from cmath import nan
import re
from time import strftime
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st


def preprocess(data):
    patternAMPM = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    pattern247 = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    pattern_remove_changed = ' changed the '

    messagesAMPM = re.split(patternAMPM, data)
    messages247 = re.split(pattern247, data)

    datesAMPM = re.findall(patternAMPM, data)
    dates247 = re.findall(pattern247, data)

    datesto247 = []

    def convertto247(dates):
        dateL = ''
        for date in dates:
            dateL = (datetime.strptime(
                date, '%m/%d/%y, %I:%M %p - ').strftime('%m/%d/%y, %H:%M - '))
            datesto247.append(dateL)

    messages = ''
    dates = ''

    if(len(messagesAMPM) > 0):
        messages = messagesAMPM
        dates = datesAMPM
        convertto247(dates)
    else:
        messages = messages247
        dates = dates247

    messages = messages[1:]

    dates = datesto247

    dataset = pd.DataFrame({'user_message': messages, 'message_date': dates})
    dataset.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in dataset['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    dataset['user'] = users
    dataset['message'] = messages
    dataset.drop(columns=['user_message'], inplace=True)

    dataset = dataset.loc[~dataset['user'].str.contains(pattern_remove_changed)]

    dataset['date'] = dataset['date'].apply(lambda x: x[0:-3])
    dataset['year'] = pd.to_datetime(dataset['date']).dt.year
    dataset['month'] = pd.to_datetime(dataset['date']).dt.month_name()
    dataset['day'] = pd.to_datetime(dataset['date']).dt.day
    dataset['hour'] = pd.to_datetime(dataset['date']).dt.hour
    dataset['minute'] = pd.to_datetime(dataset['date']).dt.minute

    dataset['message'] = dataset['message'].apply(lambda x: x[:-1])
    dataset = dataset[dataset['user'] != 'group_notification']
    dataset.index = np.arange(len(dataset))

    maxstartingdate = dataset['date'].iloc[0][0:8]
    maxendingdate = dataset['date'].iloc[-1][0:8]

    compiledstarting = pd.to_datetime(maxstartingdate, format='%m/%d/%y')
    compiledending = pd.to_datetime(maxendingdate, format='%m/%d/%y')

    with st.expander("Enter Starting and Ending Dates"):
        startdate = st.date_input("Select Starting Date", key='start', min_value=(
            compiledstarting), max_value=(compiledending), value=(compiledstarting))
        endingdate = st.date_input("Select Ending Date", key='end', min_value=(
            startdate), max_value=(compiledending), value=(compiledending))
    
    
    startingdate_check = datetime.strptime(str(startdate), '%Y-%m-%d').strftime('%m/%d/%y')
    endingdate_check = datetime.strptime(str(endingdate), '%Y-%m-%d').strftime('%m/%d/%y')

    dataset = dataset[dataset['date'].apply(lambda x: datetime.strptime(x[0:8], '%m/%d/%y').strftime('%m/%d/%y') >= startingdate_check)]
    dataset = dataset[dataset['date'].apply(lambda x: datetime.strptime(x[0:8], '%m/%d/%y').strftime('%m/%d/%y') <= endingdate_check)]

    uni = pd.DataFrame(dataset['user'].value_counts())

    uni.rename(columns={'user': 'Count'}, inplace=True)
    uni['User'] = uni.index
    uni['User_short'] = uni['User']
    uni.reset_index(drop=True)
    uni['User_short'] = uni['User_short'].apply(
        lambda x: x[:18] + "..." if len(x) > 18 else x)
    uni.sort_values(by='Count', ascending=True, inplace=True)

    stop = open('./helpers/stopwords.txt', 'r')
    stopwords = stop.read()
    
    store = dataset.copy()

    store = dataset[dataset['message'] != '<Media omitted>']
    store = store[store['user'] != 'group_notification']

    words_count = []
    store['message'] = store['message'].str.lower()

    for message in store['message']:
        for word in message.split():
            if word not in stopwords:
                words_count.append(word)

    return dataset, uni, store, words_count

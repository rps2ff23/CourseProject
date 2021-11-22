import streamlit as st
import pandas as pd
import numpy as np
import time
import random

st.markdown('# CS410 Project: Course Review Sentiment Tagging :sparkles:')
st.markdown('An application that performs sentiment analysis on course/professor reviews and provides a (+/-) rating and relevant key tags.')
#st.subheader("Using data from Rate My Professor")

DATA_URL = ('sentiment-analysis/spreadsheet.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def formatkeyword():
    t = "<div>"
    keywords = ['Keyword1', 'Keyword2', 'Keyword3']
    colors = ['red', 'blue']
    for keyword in keywords:
        t = t + " <span class='highlight " + random.choice(colors) + "'>" + keyword + '</span> '
    t = t + '</div>'
    return t

data_load_state = st.markdown('Loading data...')
data = load_data(10000)
data_load_state.markdown("Data loaded! (using st.cache)")

#if st.checkbox('Show raw data'):
#    st.subheader('Raw data')
#    st.dataframe(data)

st.header('Try it!')
text = st.text_area('Write review.')
clicked = st.button('Submit! 👈')
local_css("sentiment-analysis/style.css")
 
# Make predictions
if text != '' and clicked:
    with st.spinner('Calculating...'):
        time.sleep(5)
    st.subheader('Sentiment Prediction')
    st.success('Positive Sentiment (0.88)')
    st.subheader('These are the keywords relevant to review..')
    st.markdown(formatkeyword(), unsafe_allow_html=True)
elif text == '' and clicked:
    st.error('No input text')

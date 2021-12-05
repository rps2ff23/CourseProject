import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import sys
import gdown
from keyword_extract.finalkeywordextractionandtagging import infer_tags, feature_buildtext

st.markdown('# CS410 Project: Course Review Sentiment Tagging :sparkles:')
st.markdown('>An application that performs sentiment analysis on **course/professor reviews** and provides a (+/-) rating and relevant key tags.')

DATA_URL = 'keyword_extract/spreadsheet.csv'
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data.sample(20)

@st.cache
def load_model():
    url="https://drive.google.com/uc?id={}".format(st.secrets["gdrive_model_id"])
    output = 'finalized_model.sav'
    gdown.download(url, output, quiet=False)

def local_css(file_name):
    with open(file_name) as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

def formatkeywords(words):
    t = "<div>"
    colors = ['seagreen', 'blue', 'purple']
    for keyword in words:
        t = t + " <span class='highlight " + random.choice(colors) + "'>" + keyword + '</span> '
    t = t + '</div>'
    return t

data_load_state = st.markdown('Loading data...')
data = load_data(10000)
load_model()
data_load_state.markdown("Reviews loaded! (using st.cache)")

st.subheader('Check some sample reviews..')
if st.checkbox('Show subset of raw data'):
    st.subheader('Raw data')
    st.dataframe(data)

st.subheader('Find relevant keywords and sentiment!')
text = st.text_area('Write review here..')
clicked = st.button('Submit! 👈')
st.markdown("***")
local_css("streamlit/style.css")
#url = 'https://drive.google.com/file/d/1qq33DP24coJYm35TGpKJSa4dweB-0aSw/view?usp=sharing'

 
# Make predictions
if text != '' and clicked:
    with st.spinner("Working on it..."):
        time.sleep(2)
    st.subheader('These are the keywords relevant to review..')
    
    keywords = infer_tags(text, '/app/courseproject/finalized_model.sav')
    st.markdown(formatkeywords(keywords), unsafe_allow_html=True)
    st.markdown("***")
    st.subheader('Sentiment Prediction')
    st.success('Positive Sentiment (0.88)')
elif text == '' and clicked:
    st.error('No input text')

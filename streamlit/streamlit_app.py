import streamlit as st
import pandas as pd
import numpy as np
import time
import random
import sys
import gdown
sys.path.append('../../code/keyword-extract')
from finalkeywordextractionandtagging import feature_buildtext, infer_tags

st.markdown('# CS410 Project: Course Review Sentiment Tagging :sparkles:')
st.markdown('>An application that performs sentiment analysis on **course/professor reviews** and provides a (+/-) rating and relevant key tags.')
#st.subheader("Using data from Rate My Professor")

#DATA_URL = ('/Users/riyasimon/Documents/UIUC/CS410/project/code/keyword-extract/spreadsheet.csv')
DATA_URL = 'https://github.com/rps2ff23/CourseProject/blob/main/keyword-extract/spreadsheet.csv'
@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data.sample(20)

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
data_load_state.markdown("Reviews loaded! (using st.cache)")

st.subheader('Check some sample reviews..')
if st.checkbox('Show subset of raw data'):
    st.subheader('Raw data')
    st.dataframe(data)

st.subheader('Find relevant keywords and sentiment!')
text = st.text_area('Write review here..')
clicked = st.button('Submit! 👈')
st.markdown("***")
#local_css("/Users/riyasimon/Documents/UIUC/CS410/project/code/streamlit/style.css")
local_css("https://github.com/rps2ff23/CourseProject/blob/main/streamlit/style.css")
url = 'https://drive.google.com/file/d/1qq33DP24coJYm35TGpKJSa4dweB-0aSw/view?usp=sharing'
output = 'finalized_model.sav'
gdown.download(url, output, quiet=False)
 
# Make predictions
if text != '' and clicked:
    with st.spinner("Working on it..."):
        time.sleep(2)
    st.subheader('These are the keywords relevant to review..')
    
    keywords = infer_tags(text, '/Users/riyasimon/Documents/UIUC/CS410/project/code/keyword-extract/finalized_model.sav')
    st.markdown(formatkeywords(keywords), unsafe_allow_html=True)
    st.markdown("***")
    st.subheader('Sentiment Prediction')
    st.success('Positive Sentiment (0.88)')
elif text == '' and clicked:
    st.error('No input text')

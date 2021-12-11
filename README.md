# Course Review Sentiment Tagging

An application that performs sentiment analysis on course/professor reviews and provides a (+/-) rating and relevant key tags.

### Presentation

In Illinois Media Space: https://mediaspace.illinois.edu/media/t/1_n3sykavy

### Application 

https://share.streamlit.io/rps2ff23/courseproject/main

### How to use

1. Enter review text. 
2. Click submit!
3. Fetch results
    - Keywords: relevant keywords found in review text (Trained based on RateMyProfessor and Kaggle's Coursera review datasets)
    - Sentiment: one of (strongly negative, negative, positive, strongly positive)
    - Tags: predicted tags for the review, these tags are what are available to select in RateMyProfessor.

### File Structure

- /keyword_extract
- /reports: proposal, progress report and final report
- /sentiment_analysis
- /streamlit: code for providing a user interface for the application and deploying the app
- /web_scraping: code for fetching data from RateMyProfessor
- requirements.txt: packages needed for running the app

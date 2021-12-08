# Course Review Sentiment Tagging

An application that performs sentiment analysis on course/professor reviews and provides a (+/-) rating and relevant key tags.

### Application 

https://share.streamlit.io/rps2ff23/courseproject/main

### How to use

1. Enter review text. 
2. Click submit!
3. Fetch results
    - Keywords: relevant keywords found in review
    - Sentiment: one of (strongly negative, negative, positive, strongly positive)
    - Tags: predicted tags for the review, these tags are what are available to select in RateMyProfessor

https://user-images.githubusercontent.com/26610573/145153135-8d846f01-ea24-4165-b9a4-e01212dbce98.mov

### File Structure

- /keyword_extract
- /reports: proposal, progress report and final report
- /sentiment_analysis
- /streamlit: code for providing a user interface for the application and deploying the app
- /web_scraping: code for fetching data from RateMyProfessor
- requirements.txt: packages needed for running the app

import string
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re

def preprocess_comments(comment):
    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', comment)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence

def main(input):
    labels = ["don't skip class", 'get ready to read', 'hilarious',
       'gives good feedback', 'respected', 'amazing lectures',
       'tough grader', 'inspirational', 'clear grading criteria',
       'lots of homework', 'graded by few things', 'test heavy',
       'accessible outside class', 'group projects', 'caring',
       'lecture heavy', 'participation matters', 'beware of pop quizzes',
       'extra credit', 'so many papers', 'tests are tough']

    input = preprocess_comments(input)
    labels.append(input)
    vectorizer = CountVectorizer().fit_transform(labels)
    vectors = vectorizer.toarray()
    csim = []
    for i in range(len(labels) - 1):
        csim.append(cosine_similarity(vectors[-1].reshape(1, -1), vectors[i].reshape(1, -1))[0][0])
    csim = np.array(csim)
    idx = np.argpartition(csim, -3)[-3:]
    print([labels[i] + " " for i in idx])
    return [labels[i] + " " for i in idx]

if __name__ == "__main__":
    import sys

    sample_args = sys.argv[1:]
    sample_data = ''
    for i in sample_args:
        sample_data += i + ' '
    sample_data = sample_data[0:len(sample_data)-1]
    main(sample_data)
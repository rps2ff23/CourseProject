from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import re


labels = ["do not skip class", 'get ready to read', 'hilarious',
       'gives good feedback', 'respected', 'amazing lectures',
       'tough grader', 'inspirational', 'clear grading criteria',
       'lots of homework', 'graded by few things', 'test heavy',
       'accessible outside class', 'group projects', 'caring',
       'lecture heavy', 'participation matters', 'beware of pop quizzes',
       'extra credit', 'so many papers', 'tests are tough']

def preprocess_comments(comment):
    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', comment)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence.lower()


def create_dataframe(matrix, tokens):
    doc_names = [f'doc_{i+1}' for i, _ in enumerate(matrix)]
    df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
    return(df)

def main(input):
    input = input.split('.')
    input = [preprocess_comments(i) for i in input]

    tags = set()
    for l in labels:
      for i in input:
        data = [l, i]
        
        labels_vect = TfidfVectorizer() 
        vector_matrix = labels_vect.fit_transform(data)
        cosine_similarity_matrix = cosine_similarity(vector_matrix)
        df = create_dataframe(cosine_similarity_matrix,['labels','input'])

        if df['labels']['doc_2'] != 0:
          tags.add((l, df['labels']['doc_2']))

    sorted_tags = sorted(tags, key=lambda x: x[1], reverse=True)[0:3]
    return [x[0] for x in sorted_tags]

if __name__ == "__main__":
    import sys

    sample_args = sys.argv[1:]
    sample_data = ''

    for i in sample_args:
        sample_data += i + ' '

    sample_data = sample_data[0:len(sample_data)-1]
    print(main(sample_data))
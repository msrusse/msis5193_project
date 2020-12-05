import pandas as pd
import os
import nltk
nltk.download('stopwords')
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from sklearn.model_selection import train_test_split
from numpy import median
import text2emotion as te
from textblob import TextBlob

#import data----------------------------------
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
csv_path = os.path.join(data_path, 'csv_files')
merger = pd.read_csv(os.path.join(csv_path, 'all_movie_reviews.csv'))

#view data ----------------------------------
#merger.head(10)
#Convert to lowercase
merger['review'] = merger['review'].apply(lambda x: " ".join(x.lower() for x in str(x).split()))
# merger['review'][2]

#Remove numerical values
patterndigits = '\\b[0-9]+\\b'
merger['review'] = merger['review'].str.replace(patterndigits,'')
# merger['review'][2]

#Remove punctuation 
patternpunc = '[^\w\s]'
merger['review'] = merger['review'].str.replace(patternpunc,'')
# merger['review'][2]

#Remove Stop Words
stop = stopwords.words('english')
merger['review'] = merger['review'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
# merger['review'][2]

#Stem the words
porstem = PorterStemmer()
merger['review'] = merger['review'].apply(lambda x: " ".join([porstem.stem(word) for word in x.split()]))
# merger['review'][2]

#creating a document-term matrix
#library update to use CountVectorized
from sklearn.feature_extraction.text import CountVectorizer
vectorizer = CountVectorizer()

#Convert the data into a document-term matrix
vectorizer = CountVectorizer()
tokens_data = pd.DataFrame(vectorizer.fit_transform(merger['review']).toarray(), columns=vectorizer.get_feature_names())
# tokens_data.columns
# print(tokens_data.columns.tolist())

#top 10
freq = pd.Series(' '.join(merger['review']).split()).value_counts()[:10]
# freq

#top 20
freq1 = pd.Series(' '.join(merger['review']).split()).value_counts()[:20]
# freq1

"""## Sentiment Analysis"""

#############################################
#=============Read in Libraries=============#
# Read in the necessary libraries.          #
#############################################

"""### Topic Modeling """

#============================================
# Perform Latent Dirichlet Allocation (LDA)
#============================================
vectorizer = CountVectorizer(max_df=0.8, min_df=4, stop_words='english')

doc_term_matrix = vectorizer.fit_transform(merger['review'].values.astype('U'))

doc_term_matrix.shape

# Generate the LDA with 5 topics to divide
# the text into; set the seed to 35 so that
# we end up with the same result
LDA = LatentDirichletAllocation(n_components=5, random_state=35)
LDA.fit(doc_term_matrix)

# Retrieve words in the first topic
first_topic = LDA.components_[0]

# Sort the indexes according to probability 
# values using argsort()
top_topic_words = first_topic.argsort()[-10:]

# Output the words to the console screen
for i in top_topic_words:
    print(vectorizer.get_feature_names()[i])

# Print the 10 words with highest 
# probabilities for all five topics
for i,topic in enumerate(LDA.components_):
    print(f'Top 10 words for topic #{i}:')
    print([vectorizer.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')

# Add a new column to your dataframe containing the LDA topic number

# Add a column in the dataset with the topic number
topic_values = LDA.transform(doc_term_matrix)
topic_values.shape
merger['topic'] = topic_values.argmax(axis=1)

merger.head()

#Generate 3 to 4 topics using Non-Negative Matrix Factorization (NMF). 
tfidf_vect = TfidfVectorizer(max_df=0.8, min_df=5, stop_words='english')
doc_term_matrix2 = tfidf_vect.fit_transform(merger['review'].values.astype('U'))

nmf = NMF(n_components=4, random_state=42)
nmf.fit(doc_term_matrix2)
first_topic = nmf.components_[0]
top_topic_words = first_topic.argsort()[-10:]

for i in top_topic_words:
    print(tfidf_vect.get_feature_names()[i])

# Top 10 words for each topic
for i,topic in enumerate(nmf.components_):
    print(f'Top 10 words for topic #{i}:')
    print([tfidf_vect.get_feature_names()[i] for i in topic.argsort()[-10:]])
    print('\n')

# Add a column with the topic values. 
topic_values2 = nmf.transform(doc_term_matrix2)
merger['topic2'] = topic_values2.argmax(axis=1)
merger.head()

"""### **Creating function for porlarity value**"""
def polarity_value(review):
    return TextBlob(review).sentiment.polarity

merger.head()

merger['sentiment_score'] = merger['review'].apply(polarity_value)

def label(row):
    if row['sentiment_score'] > 0 :
        return 'Positive'
    if row['sentiment_score'] < 0 :
        return 'Negative'
    if row['sentiment_score'] == 0 :
        return 'Neutral'

merger['label'] = merger.apply (lambda row: label(row), axis=1)

merger.head()

emo_list= []
for i in merger['review']:
    emo_list.append(te.get_emotion(i))

merger2 = merger

angry = []
fear = []
happy = []
sad = []
surprise = []
for i in emo_list:
    angry.append(i['Angry'])
    fear.append(i['Fear'])
    happy.append(i['Happy'])
    sad.append(i['Sad'])
    surprise.append(i['Surprise'])

#we have emotion vales and reshaping then adding back to data, neeed to know how many rows we have

angry = np.reshape(angry,(115,1))

fear = np.reshape(fear,(115,1))

happy = np.reshape(happy,(115,1))

sad = np.reshape(sad,(115,1))

surprise = np.reshape(surprise,(115,1))

new_data = np.concatenate((angry,fear,happy,sad,surprise),axis=1)
data = pd.DataFrame(data=new_data ,columns=["angry","fear","happy","sad","surprise"])
merger2 = pd.concat([merger2,data],axis=1)

merger2.head()
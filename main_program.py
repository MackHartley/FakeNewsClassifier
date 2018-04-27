from webpage_parser import *
from clean_text import *
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from scipy.sparse import hstack


def get_tfidf(title, text, title_vocab, text_vocab):
    # Get tfidf matrices for title and text separately and stack them together
    count_vect_title = CountVectorizer(vocabulary = title_vocab)
    count_vect_text = CountVectorizer(vocabulary = text_vocab)
    title_counts = count_vect_title.fit_transform([title])
    text_counts = count_vect_text.fit_transform([text])

    tfidf_transformer = TfidfTransformer()
    title_tfidf = tfidf_transformer.fit_transform(title_counts)
    text_tfidf = tfidf_transformer.fit_transform(text_counts)
    tfidf = hstack([title_tfidf, text_tfidf])
    return tfidf


#Change the title here
title = 'Was the Body of a Dead Pedophile Dumped in Front of Parliament?'

#Put the text into text.txt file
text = read_text('text.txt')


title_text_classifier = pickle.load(open('news_clf/title_text_classifier.sav', 'rb'))
title_vocab = pickle.load(open('news_clf/title_vocab.sav', 'rb'))
text_vocab = pickle.load(open('news_clf/text_vocab.sav', 'rb'))

tfidf = get_tfidf(title, text, title_vocab, text_vocab)

news_reliability = title_text_classifier.predict(tfidf)
print('The news is predicted to be: ')
print(news_reliability)


#domain_classifier = pickle.load(open('domain_clf.sav', 'rb'))

# domain = get_domain(title)
# dict = {'bbc.com' : [1000, 1000]}
# harmonic_pagerank = dict[domain]


# domain_reliability = domain_classifier.predict(harmonic_pagerank)
#
# print('The domain is predicted to be: ')


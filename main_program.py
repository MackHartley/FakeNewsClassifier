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

def search_site(site):
    """Looks for a site in page rank file. Input can include .com or not"""
    with open('ranks.txt','r') as f:
        next(f)
        for line in f:
            lst = line.split()
            if ('.' in site and '.'.join(site.split('.')[::-1])== lst[4]) or site in lst[4].split('.'):
                return lst
        return False

def find_ranks(lst):
    """Generalized version of find_authority. Takes a little while to run for long lists."""
    ranks = {}
    for i in lst:
        if search_site(i) is not False:
            ranks[i] = [search_site(i)[0], search_site(i)[2]]
        else:
            continue
    return ranks

#Change the title here
title = 'Why Answering Mueller’s Questions Could Be a Minefield for Trump'

#Put the text into text.txt file
text = read_text('text.txt')

#Put in domain if known. Otherwise we will use Google API to search the title to get the domain.
domain = None


title_text_classifier = pickle.load(open('news_clf/title_text_classifier.sav', 'rb'))
title_vocab = pickle.load(open('news_clf/title_vocab.sav', 'rb'))
text_vocab = pickle.load(open('news_clf/text_vocab.sav', 'rb'))

tfidf = get_tfidf(title, text, title_vocab, text_vocab)

news_reliability = title_text_classifier.predict(tfidf)
print('The news is predicted to be: ')
print(news_reliability)


domain_classifier = pickle.load(open('domain_classifier.sav', 'rb'))

if domain is None:
    domain = get_domain(title)
if domain is not None:
    print("Domain is: " + domain)
    centralities = [[search_site('themacweekly')[2], search_site('themacweekly')[0]]]

    domain_reliability = domain_classifier.predict(centralities)

    print('The domain is predicted to be: ')
    if domain_reliability[0] == 1:
        print('Reliable')
    else:
        print('Unreliable')
else:
    print("Domain not found on Google NewsAPI.")


from webpage_parser import *
import pickle

title = ''
text = ''

title_text_classifier = pickle.load(open('title_text_clf.sav', 'rb'))
domain_classifier = pickle.load(open('domain_clf.sav', 'rb'))

domain = get_domain(title)
dict = {'bbc.com' : [1000, 1000]}
harmonic_pagerank = dict[domain]

news_reliability = title_text_classifier.fit([text, title])

print('The news is predicted to be: ')


domain_reliability = domain_classifier.fit(harmonic_pagerank)

print('The domain is predicted to be: ')


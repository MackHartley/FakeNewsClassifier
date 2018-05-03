from lib.webpage_parser import *
from lib.clean_text import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from scipy.sparse import hstack
import pickle
from tkinter import *



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
    with open('centrality_rank.txt','r') as f:
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

def reliability(result):
    if result is None:
        return "Not Found"
    elif result[0] == 0:
        return "Reliable"
    else:
        return "Unreliable"


def predict(title, text):

    title_text_classifier = pickle.load(open('models/title_text_classifier.sav', 'rb'))
    title_vocab = pickle.load(open('models/title_vocab.sav', 'rb'))
    text_vocab = pickle.load(open('models/text_vocab.sav', 'rb'))

    tfidf = get_tfidf(title, text, title_vocab, text_vocab)

    news_reliability = title_text_classifier.predict(tfidf)
    print('The news is predicted to be: ')
    print(news_reliability)


    # Domain classifier
    # The rank file in this folder is the top 10k websites.
    # The whole file has 90 millions website. To download the whole file, follow the link in README.


    domain_classifier = pickle.load(open('models/domain_classifier.sav', 'rb'))

    domain = get_domain(title)

    if domain is not None:
        print("Domain is: " + domain)
        domain = ''.join(domain.lower().split())
        result = search_site(domain)
        if result is not False:
            centralities = [[result[2], result[0]]]
            domain_reliability = domain_classifier.predict(centralities)

            print('The domain is predicted to be: ')
            if domain_reliability[0] == 0:
                print('Reliable')
            else:
                print('Unreliable')
        else:
            print("Domain not found in our dataset.")
            domain_reliability = None
    else:
        print("Domain not found on Google News API.")
        domain_reliability = None

    return news_reliability, domain_reliability


window = Tk()

window.title("Fake or Real??")

title_label = Label(window, text="Title")
title_label.grid(column=0, row=0)

title_box = Entry(window)
title_box.focus_set()
title_box.grid(column=0, row=1)

text_label = Label(window, text="Text")
text_label.grid(column=0, row=2)

text_box = Entry(window)
text_box.focus_set()
text_box.grid(column=0, row=3)


def callback():
    title = title_box.get()
    text = text_box.get()
    news_reliability, domain_reliability = predict(title, text)
    txt_window = Tk()
    lb = Label(txt_window, text='News is '+ news_reliability[0] + '!!!')
    lb.grid(column=0, row=1)
    if news_reliability[0] == 'FAKE':
        lb['fg']='red'
    else:
        lb['fg']='blue'
    dm_window = Tk()
    lb2 = Label(dm_window, text='Domain is ' + reliability(domain_reliability) + '!!!')
    lb2.grid(column=5, row=5)
    if reliability(domain_reliability) == 'Unreliable':
        lb2['fg']='red'
    elif reliability(domain_reliability) == 'Reliable':
        lb2['fg']='blue'
    else:
        lb2['fg']='black'

predict_button = Button(window, text="Predict", bg='yellow', command = callback)
predict_button.grid(column=0, row=6)


window.mainloop()



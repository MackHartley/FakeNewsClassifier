# Fake News Classifier

Fake news is a growing problem in the world, especially within the US. Fake news not only sows unrest and distrust in our media institutions, but also damages the discourse between both citizens and politicians in the US. According to the [Brookings Institute](https://www.brookings.edu/research/how-to-combat-fake-news-and-disinformation/) in Washington DC: 

“Algorithms are powerful vehicles in the digital era, and they can help establish automatic hoax detection systems.”

With this in mind, we set out to make our own systems which could identify hoaxes and fake news. To do this, we made two different fake news classifiers and trained them both to classify articles as “Real” or “Fake”. The first algorithm classifies fake news by using [TF-IDF](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) and text classification to analyze the collection of words used in an article’s text and body. The second algorithm determines news source legitimacy by looking at the pagerank and harmonic values of the news source’s website on the web.

## Installation

This project was largely made using Python 3 and Jupyter Notebook. The easiest way to get started using this project is to download Jupyter Notebook on your own machine. Additionally, you will need to have Python 3 to run this project. A tutorial for installing Jupyter Notebook (and by extension Python 3) can be found [here](http://jupyter.readthedocs.io/en/latest/install.html).

### Getting Started: TF-IDF Classifier

To use the TF-IDF classifier you will first need to have a trained classifier. If you are downloading the entire project directly and would like to use our general purpose classifier, then you can skip the next paragraph. 

To train a new TF-IDF classifier you must first open the `text_classifier.ipynb` file in Jupyter and run all cells. Once that has finished a cPickle file containing the classifier will be stored on your computer. This file contains the classifier that is used for classifying fake news. 

With the classifier ready, you can open the `main_program.py` file and begin to classify news articles. Note that `main_program.py` is not a Jupyter notebook so you should run the file seperate of Jupyter. After doing so you will recieve a pop up box to input your news article information.

### Getting Started: Domain Classifier

The process here is much the same as the process found in "Getting Started: TF_IDF Classifier." If you with to use the pretrained model we include, you can skip the next paragraph.

To train a new domain classifier you must first open the `exploratory.ipynb` file and run all the cells in it. After doing so a cPickle file containing the domain classifier will be stored on your computer. 

Once you have a trained domain classifier you can now open the `main_program.py` file and start classifying with it. Note that `main_program.py` is not a Jupyter notebook so you should run the file seperate of Jupyter. After doing so you will receive a pop up box to input your news article information.

## Data

In this project, we used three datasets to train and test our classifiers:

* News dataset to train and test the TF-IDF classifier (80% training - 20% testing). It has 6335 rows with title, text, and label (fake/real). You can find the original dataset in this [repository](https://github.com/GeorgeMcIntire/fake_real_news_dataset).

* Domains dataset to train the k-nearest neighbors (KNN) classifier. It contains about 200 fake sites found on Kaggle and about 200 hand-picked list of reliable sites from Google News. We used this [dataset](http://commoncrawl.org/2017/08/webgraph-2017-may-june-july/) from the [Common Crawl](http://commoncrawl.org/) to find the pagerank and harmonic centrality values for the domains in this dataset.

## Core Features

### TF-IDF Classifier

This classifier analyzes the title and body of a given news article and makes a prediction about the article’s legitimacy based on its text content. This process utilizes TF-IDF and a gradient boosting classifier for the classification capabilities.

In order to train the gradient boosting classifier for this project we followed the following procedure:

1. Split dataset into 80% training 20% testing
2. For each article in training set, extract its title and body text. 
3. Run TF-IDF on on the title text and body text separately.
4. Join the two resulting TF-IDF tables together
5. Train the classifier on the resulting joined TF-IDF table

Once the gradient boosting classifier is trained it can then be tested using the testing set we previously created. This same process can be replicated with different data sets and different training - testing ratios.

Note that for this classifier, the TF-IDF matrix can be created with the `get_tfidf()` function.

Once this matrix has been generated, it can be classified with the line of code below:

```python
news_reliability = title_text_classifier.predict(tfidf)
```

### Domain KNN Classifier

The domain classifier works slightly differently from the TF-IDF classifier. Instead of classifying individual articles, the domain classifier can be used to determine if a news source is legitimate or not. By extension, this can be used to determine if individual articles are fake or not. For example, if our project is provided with an article from a fake news website, it will just label this article as “Fake”.

In order to train the domain KNN classifier for this project we followed the following procedure:

1. Split the domain dataset into 80% training 20% testing. Each domain in the training dataset has a pagerank value and a harmonic centrality value.
2. Train the KNN classifier using the training data. You can learn more about the KNN technique [here](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm). 
3. Test the accuracy of the predictions of the KNN classifier using the testing data.

A domain can be classified using the following:

```python
domain = 'nytimes.com'
result = search_site(domain)
domain_classifier.predict([[result[2], result[0]]])
```

## Testing

### TF-IDF Classifier

Confusion matrix from running the TF-IDF classifier on the testing dataset:

| Predicted/Actual  | Fake  | Real | All  |
|---|---|---|---|
| Fake  | 32 | 3  | 35  |
| Real  | 9  | 22  | 31  |
| All | 41  | 25  | 66  |

Sensitivity: ≈ 0.71, Specificity: ≈ 0.91, Accuracy: ≈ 0.81.

### Domain KNN Classifier

Confusion matrix from running the Domain KNN classifier on the testing dataset:

| Predicted/Actual  | Fake  | Real | All  |
|---|---|---|---|
| Fake  | 594 | 57  | 651  |
| Real  | 62  | 554  | 616  |
| All | 656  | 611  | 1267  |

Sensitivity: ≈ 0.90, Specificity: ≈ 0.91, Accuracy: ≈ 0.91.

## Contributing

If you would like to contribute to this project please feel free to submit a pull request. In the event you encountered an issue or bug while using our classifiers you can log said bug using Git issues.

## References

Installing Jupyter and Python: http://jupyter.readthedocs.io/en/latest/install.html

Brookings Institute: https://www.brookings.edu/research/how-to-combat-fake-news-and-disinformation/


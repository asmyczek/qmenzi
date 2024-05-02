import nltk
import spacy
from spacy.lang.en import English
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gensim.models.ldamodel import LdaModel
from gensim import corpora
from functools import reduce

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')
spacy.load('models/en_core_web_sm-3.7.1/en_core_web_sm/en_core_web_sm-3.7.1/')

EN_PARSER = English()
EN_STOP = set(nltk.corpus.stopwords.words('english'))
SENTIMENT_ANALYZER = SentimentIntensityAnalyzer()
LEMMATIZER = WordNetLemmatizer()

def tokenize(text):
    lda_tokens = []
    tokens = EN_PARSER(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def cleanse_text(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in EN_STOP]
    tokens = [LEMMATIZER.lemmatize(token) for token in tokens]
    return tokens

def get_tokens(content):
    return [cleanse_text(line) for line in content]

def get_topics(tokens):
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]

    lda = LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)
    topics = lda.print_topics(num_words=4)

    ret = []
    for i, topic in topics:
        ret.append(lda.show_topic(i))
    return ret

def get_sentiment(content):
    return [SENTIMENT_ANALYZER.polarity_scores(c) for c in content]
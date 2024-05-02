import nltk
import spacy
from spacy.lang.en import English
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from gensim.models.ldamodel import LdaModel
from gensim import corpora

nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('vader_lexicon')
spacy.load('models/en_core_web_sm-3.7.1/en_core_web_sm/en_core_web_sm-3.7.1/')

EN_PARSER = English()
EN_STOP = set(nltk.corpus.stopwords.words('english'))
SENTIMENT_ANALYZER = SentimentIntensityAnalyzer()
LEMMATIZER = WordNetLemmatizer()


def tokenize(text):
    tokens = EN_PARSER(text)
    tokens = [token.lower_ for token in tokens if not token.orth_.isspace()]
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in EN_STOP]
    tokens = [LEMMATIZER.lemmatize(token) for token in tokens]
    return tokens


def get_tokens(content):
    return [tokenize(line) for line in content]


def get_topics(tokens, num_topics=3):
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(token) for token in tokens]

    lda = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)
    return [lda.show_topic(i) for i in range(num_topics)]


def get_sentiment(content):
    return [SENTIMENT_ANALYZER.polarity_scores(c) for c in content]
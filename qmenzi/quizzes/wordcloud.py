import logging
import matplotlib.pyplot as plot
from wordcloud import WordCloud, STOPWORDS
from functools import reduce
from qmenzi import config

logger = logging.getLogger("qmenzi-wordcloud")

WORDCLOUD_MAX_WORDS         = config('wordcloud.wordcloud_max_words') or 60
WORDCLOUD_SIZE_WIDHT        = config('wordcloud.wordcloud_size_widht') or 900
WORDCLOUD_SIZE_HIGHT        = config('wordcloud.wordcloud_size_hight') or 600
WORDCLOUD_MARGIN            = config('wordcloud.wordcloud_margin') or 5
WORDCLOUD_BACKGROUND_COLOR  = config('wordcloud.wordcloud_background_color') or 'white'


def generate_wordcloud():
    wordcloud = WordCloud(max_words=WORDCLOUD_MAX_WORDS,
                          width=WORDCLOUD_SIZE_WIDHT,
                          height=WORDCLOUD_SIZE_HIGHT,
                          margin=WORDCLOUD_MARGIN,
                          background_color=WORDCLOUD_BACKGROUND_COLOR,
                          stopwords=STOPWORDS, 
                          relative_scaling=0.2)
    return wordcloud


def generate_stopwords_wordcloud(content):
    # TODO: generate wordcloud for stopwards
    pass


def filter_frequencies(frequencies, filter_words):
    if len(filter_words) > 0:
        def filter(r, item):
            k, v = item
            if k not in filter_words:
                r[k] = v
            return r
        return reduce(filter, frequencies.items(), {})
    return frequencies


def create_wordcloud_for_content(content, filter_words=[], save_to_file=None, dpi=600):
    wordcloud = generate_wordcloud()
    frequencies = filter_frequencies(wordcloud.process_text(content), filter_words)
    wordcloud.generate_from_frequencies(frequencies)
    img = plot.figure()
    plot.imshow(wordcloud.to_array(), interpolation="bilinear")
    plot.axis(False)
    plot.tight_layout()
    if save_to_file:
        img.savefig(save_to_file, dpi=dpi)
    return plot

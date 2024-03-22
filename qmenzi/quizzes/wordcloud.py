import logging
import matplotlib.pyplot as plot
from wordcloud import WordCloud, STOPWORDS
from qmenzi import config

logger = logging.getLogger("qmenzi-wordcloud")

WORDCLOUD_MAX_WORDS         = config('wordcloud.wordcloud_max_words') or 50
WORDCLOUD_SIZE_WIDHT        = config('wordcloud.wordcloud_size_widht') or 900
WORDCLOUD_SIZE_HIGHT        = config('wordcloud.wordcloud_size_hight') or 600
WORDCLOUD_MARGIN            = config('wordcloud.wordcloud_margin') or 5
WORDCLOUD_BACKGROUND_COLOR  = config('wordcloud.wordcloud_background_color') or 'white'


def generate_wordcloud(content):
    wordcloud = WordCloud(max_words=WORDCLOUD_MAX_WORDS,
                          width=WORDCLOUD_SIZE_WIDHT,
                          height=WORDCLOUD_SIZE_HIGHT,
                          margin=WORDCLOUD_MARGIN,
                          background_color=WORDCLOUD_BACKGROUND_COLOR,
                          stopwords=STOPWORDS, 
                          relative_scaling=0.2)

    return wordcloud.generate(content)


def create_wordcloud_for_content(content, save_to_file=None, dpi=600):
    wordcloud = generate_wordcloud(content)
    img = plot.figure()
    plot.imshow(wordcloud.to_array(), interpolation="bilinear")
    plot.axis(False)
    plot.tight_layout()
    if save_to_file:
        img.savefig(save_to_file, dpi=dpi)
    return plot

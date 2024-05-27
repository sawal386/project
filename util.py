## This file contain useful functions

import spacy
import re

def year_checker(collection, year):
    """
    check the correctness of get_article_date() method

    Args:
        collection: (ArticleCollection)
        year: (int)
    """

    months = [12]
    total = 0
    for m in months:
        coll = collection.get_articles_date(year, m)
        total += coll.get_size()

    print(total, collection.get_size())


def tokenize(text, nlp, min_words=1):
    """
    code from: https://github.com/Weixin-Liang/Mapping-the-Increasing-Use-of-LLMs-in-Scientific-Papers

    Processes the input text, splits it into sentences, and further processes each sentence
    to extract non-numeric words. It constructs a list of these words for each sentence.

    Args:
        text: (str) A string containing multiple sentences.
        nlp: (spacy.lang.en.English)
        min_words: (int) minimum number of words needed in a sentence

    Returns:
    list: A list of lists, where each inner list contains the words from one sentence,
          excluding any numeric strings.
    """
    # remove newline characters, this line is not necessary for all cases
    # the reason it is included here is because the abstracts in the dataset contain abnormal newline characters
    # e.g. Recent works on diffusion models have demonstrated a strong capability for\nconditioning image generation,
    text = text.replace('\n',' ')
    # Initialize an empty list to store the list of words for each sentence
    sentence_list=[]
    # Process the sentence using the spacy model to extract linguistic features and split into components
    doc=nlp(text)
    # Iterate over each sentence in the processed text
    for sent in doc.sents:
        # Extract the words from the sentence
        if len(sent) > min_words:
            words = re.findall(r'\b\w+\b', sent.text.lower())
            # Remove any words that are numeric
            words_without_digits=[word for word in words if not word.isdigit()]
            # If the list is not empty, append the list of words to the sentence_list
            if len(words_without_digits)!=0:
                sentence_list.append(words_without_digits)
    return sentence_list


def get_year_month(input_str):
    """
    returns the year and month
    Args:
        input_str: (str) the input string

    Returns: (int, int) year, month
    """
    parts = input_str.split('_')
    year = int(parts[0])
    month = int(parts[1].split('.')[0])

    return year, month
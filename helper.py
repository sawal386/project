from base import Article, ArticleCollection

def convert_raw_json(json_orig):
    """
    create an Article collection from the raw json file

    Args:
        json_orig:

    Returns:
        (ArticleCollection)
    """

    collection = ArticleCollection("all")
    for key in json_orig:
        for i in range(len(json_orig[key])):
            article = Article(json_orig[key][i], key)
            collection.add_article(article)

    return collection
# This file defines classes to store articles
from pathlib import Path
import spacy
from util import tokenize
import pandas as pd
from tqdm import tqdm

class ArticleCollection:
    """
    Base class to hold all articles
    Attributes:
        subject: (str) subject of the article
        all_articles: (dict) (int) article id -> (Article)
        current_id: (int) the id that will be assigned to the next article
        month: (int) the month of publication
        year: (int) the year of publication
    """

    def __init__(self, subject="all", year=None, month=None):
        self.subject = subject
        self.month = month
        self.year = year
        self.all_articles = {}
        self.current_id = len(self.all_articles)


    def add_article(self, article, article_id=None):
        """
        adds an article to the collection

        Args:
            article: (Article)
            article_id: (int) article id
        """

        if article_id is None:
            article_id = self.current_id
        self.all_articles[article_id] = article
        self.current_id = len(self.all_articles)

    def get_article(self, article_id):
        """
        returns the article associated with given id

        Args:
            article_id: (int)

        Returns: (Article)
        """

        if article_id in self.all_articles:
            return self.all_articles[article_id]
        else:
            raise KeyError("No such article with id:{}".format(article_id))

    def get_size(self):
        """
        Returns: (int) the number of articles in the collection
        """

        return len(self.all_articles)

    def get_articles_subject(self, subject):
        """
        get articles according to subject and time

        Args:
            subject: (subject)

        Returns: (SubjectCollection)
        """

        if subject is not None:
            subject = subject.lower()

        subject_coll = SubjectCollection(subject)
        for i in self.all_articles:
            if self.all_articles[i].subject == subject:
                subject_coll.add_article(self.all_articles[i], i)

        return subject_coll

    def get_articles_time(self, year=None, month=None):
        """
        obtain all articles published on the given year and month
        Args:
            year: (int) year
            month: (int) month
        Returns:
            (ArticleCollec

        """
        if year is None and month is None:
            raise ValueError("At least of of the year or month needs to be not none")
        time_coll = TimeCollection(year, month)
        for i in self.all_articles:
            date_split = self.all_articles[i].date.split("-")
            try:
                if month is not None:
                    if int(date_split[0]) == year and int(date_split[1]) == month:
                        time_coll.add_article(self.all_articles[i], i)
                else:
                    if int(date_split[0]) == year:
                        time_coll.add_article(self.all_articles[i], i)
            except IndexError:
                if int(date_split[0]) == "year":
                    time_coll.add_article(self.all_articles[i], i)

        return time_coll

    def assign_year(self, year):
        """
        Args:
            year: (int) the year of publications in the collection
        """
        self.year = year

    def assign_month(self, month):
        """
        Args:
            month: (int) the month of publications in the collection
        """
        self.month = month

    def assign_subject(self, subject):
        """
        Args:
            subject: (str) the subject of the publications in the collection
        """
        self.subject = subject

    def export_parquet(self, folder_name, file_name,
                       col_name="inference_sentence"):
        """
        Exports the data in parquet format. It is the format that is compatible with
        the inference code
        Args:
            folder_name: (str) name of the folder
            file_name: (str) name of the file
            col_name: (str) name of the column defining the tokenized sentences
        """
        print("Exporting parquet")
        try:
            nlp = spacy.load("en_core_web_lg")
        except OSError:
            from spacy.cli import download
            print("Downloading model")
            download("en_core_web_lg")
            nlp = spacy.load("en_core_web_lg")

        meta_data = {"article_id": [], "sentence_no": []}
        path = Path(folder_name)
        path.mkdir(parents=True, exist_ok=True)
        meta_name = "meta_" + file_name + ".csv"
        if ".parquet" not in file_name:
            file_name = file_name + ".parquet"

        full_path = path / "{}".format(file_name)
        meta_path = path / "{}".format(meta_name)

        sentence_dict = {col_name: []}
        count = 0

        for at_id in tqdm(self.all_articles):
            description = self.all_articles[at_id].description
            if len(description) != 0:
                sentences = tokenize(description, nlp)
                sentence_dict[col_name] += sentences
                meta_data["article_id"] += [at_id] * len(sentences)
                count_next = count + len(sentences)
                meta_data["sentence_no"] += list(range(count, count_next))
                count = count_next

        df_sentences = pd.DataFrame.from_dict(sentence_dict)
        df_meta = pd.DataFrame.from_dict(meta_data)

        df_sentences.to_parquet(full_path)
        df_meta.to_csv(meta_path)
        print("File Exported as: {}".format(full_path))


class SubjectCollection(ArticleCollection):

    def __init__(self, subject_name):
        super().__init__(subject=subject_name)

class TimeCollection(ArticleCollection):

    def __init__(self, year, month):
        super().__init__(year=year, month=month)

class Article:
    """
    base class for an article
    Attributes:
        date: (str) the date when the article was published
        subject: (str) the subject the article is associated with
        subject_score: (float) the score for the subject prediction
        language: (str) the language in which the article was written
        language_score: (float) the score for language prediction
        description: (str) the description of the article
        title: (str) the title of the article
        identifier: (str) the identifier in the source json file
        base_key: (str) the key in the json file associated with the article
        source: (str)
    """

    def __init__(self, source_json, base_key=None, subject_key="predicted_fos"):
        """
        Args:
            source_json: (dict) the source json data
        """

        self.date = source_json["date"][0]
        all_subjects = source_json[subject_key]
        if len(all_subjects) != 0:
            self.subject = all_subjects[0][0].lower()
            self.subject_score = float(all_subjects[0][1])
        else:
            self.subject = None
            self.subject_score = None
        try:
            self.description = source_json["description"][0]
        except IndexError:
            self.description = ""

        try:
            self.title = source_json["title"][0]
        except IndexError:
            self.title = None

        try:
            self.identifier = source_json["identifier"][0]
        except IndexError:
            self.identifier = None

        try:
            self.pred_language = source_json["predicted_language"][0][0]
            self.pred_language_score = float(source_json["predicted_language"][0][1])
        except IndexError:
            self.pred_language = None
            self.pred_language_score = None
        try:
            self.language = source_json["language"][0]
        except IndexError:
            self.language = None

        try:
            self.source = source_json["source"][0]
        except IndexError:
            self.source = None



        self.base_key = base_key

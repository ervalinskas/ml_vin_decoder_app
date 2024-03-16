import pandas as pd
import numpy as np
import joblib

from sklearn.feature_extraction.text import CountVectorizer
from config import VectorizerConfig


class FeatureEngineering:

    def __init__(self, vectorizer):
        self.vectorizer = vectorizer

    def fit_transform(self, texts):
        processed_texts = self._preprocess_texts(texts)
        features = self.vectorizer.fit_transform(processed_texts)
        return features

    def transform(self, texts):
        processed_texts = self._preprocess_texts(texts)
        features = self.vectorizer.transform(processed_texts)
        return features

    def _preprocess_texts(self, texts):
        return [self._extract_characters(text) for text in texts]

    def _extract_characters(self, text):
        return text[3:10]

    # def save_vectorizer(self, path):
    #     joblib.dump(self.vectorizer, path)
    #     mlflow.log_artifact(path)

    @classmethod
    def from_config(cls, config: VectorizerConfig):
        vectorizer = CountVectorizer(
            ngram_range=config.ngram_range, analyzer=config.analyzer
        )
        return cls(vectorizer=vectorizer)

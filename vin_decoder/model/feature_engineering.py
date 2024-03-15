import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import (
    CountVectorizer,
    HashingVectorizer,
    TfidfVectorizer,
)


def vectorize_text(
    vectorizer: CountVectorizer | HashingVectorizer | TfidfVectorizer,
    X_train: pd.Series,
    X_valid: pd.Series,
) -> tuple[np.ndarray]:
    X_train_featurized = vectorizer.fit_transform(X_train)
    X_valid_featurized = vectorizer.transform(X_valid)
    return (X_train_featurized, X_valid_featurized)


def extract_features_labels(
    df: pd.DataFrame, label: str
) -> tuple[pd.Series | np.ndarray]:
    df["wmi"] = df["vin"].apply(lambda x: x[0:3])
    df["vehicle_attrs"] = df["vin"].apply(lambda x: x[3:10])
    corpus = df.vehicle_attrs
    targets = df[label]
    class_names = targets.unique()
    return corpus, targets, class_names

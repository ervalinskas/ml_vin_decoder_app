from __future__ import annotations

from pathlib import Path
from typing import Literal
from sklearn.feature_extraction.text import CountVectorizer

import loguru
import optuna
import pandas as pd
import numpy as np
import xgboost as xgb

from vin_decoder.data.feature_engineering import extract_features_labels
from vin_decoder.config import DataConfig, ParamGridConfig


class Classifier:

    def __init__(self) -> None:
        pass

    @classmethod
    def from_config(cls):
        pass

    def fit(sefl, X, y):
        pass

    def predict_proba(self):
        pass

    def predict(self, X):
        pass


class Objective(object):
    def __init__(self, iris):
        self.iris = iris

    def __call__(self, trial):
        x, y = self.iris.data, self.iris.target

        classifier_name = trial.suggest_categorical("classifier", ["SVC", "RandomForest"])
        if classifier_name == "SVC":
            svc_c = trial.suggest_float("svc_c", 1e-10, 1e10, log=True)
            classifier_obj = sklearn.svm.SVC(C=svc_c, gamma="auto")
        else:
            rf_max_depth = trial.suggest_int("rf_max_depth", 2, 32, log=True)
            classifier_obj = sklearn.ensemble.RandomForestClassifier(
                max_depth=rf_max_depth, n_estimators=10
            )

        score = sklearn.model_selection.cross_val_score(classifier_obj, x, y, n_jobs=-1, cv=3)
        accuracy = score.mean()
        return accuracy


class Tuning:

    def __init__(
        self,
        param_grid: ParamGridConfig,
    ) -> None:
        self.param_grid = param_grid

    @staticmethod
    def objective(trial):
        dtrain = xgb.DMatrix(data=X, label=y)

        # Define the hyperparameter space
        param = {
            "objective": "binary:logistic",  # Example for binary classification
            "eval_metric": "auc",
            "learning_rate": trial.suggest_float("learning_rate", param_grid.),
            "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
            "max_depth": trial.suggest_int("max_depth", 3, 9),
            "subsample": trial.suggest_float("subsample", 0.8, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.8, 1.0),
        }

        # Callback to capture the stopping round for each fold
        stopping_rounds = []

        def early_stopping_rounds(stopping_rounds):
            def callback(env):
                for i, cvpack in enumerate(env.cvfolds):
                    if cvpack.bst.best_iteration != 0:
                        stopping_rounds.append(cvpack.bst.best_iteration)

            return callback

        # Perform cross-validation
        cv_results = xgb.cv(
            param,
            dtrain,
            num_boost_round=1000,  # Adjust based on your needs
            nfold=5,
            stratified=True,
            callbacks=[
                early_stopping_rounds(stopping_rounds),
                xgb.callback.early_stop(50),
            ],
            seed=42,
        )

        # Calculate the average stopping round
        avg_stopping_round = (
            np.mean(stopping_rounds) if stopping_rounds else param["n_estimators"]
        )

        # Return the metric to be maximized/minimized and average stopping round
        return cv_results["test-auc-mean"].max(), avg_stopping_round
    
    def tune_params(self):
        pass


class Training:

    def __init__(
        self,
        preprocessed_labels_dir: Path,
        vectorizer: CountVectorizer,
        target: Literal["make", "model", "year", "body"],
        logger: loguru.Logger,
    ) -> None:
        self.preprocessed_labels_dir = preprocessed_labels_dir
        self.vectorizer = vectorizer
        self.target = target
        self.logger = logger

    @classmethod
    def from_config(
        cls,
        config: DataConfig,
        target: Literal["make", "model", "year", "body"],
        logger: loguru.Logger,
    ):
        vectorizer_config = config.modeling.vectorizer
        vectorizer = CountVectorizer(
            ngram_range=vectorizer_config.ngram_range,
            analyzer=vectorizer_config.analyzer,
        )
        return cls(
            preprocessed_labels_dir=Path(config.preprocessed_labels_dir),
            vectorizer=vectorizer,
            target=target,
            logger=logger,
        )

    def train_model(self):
        pass

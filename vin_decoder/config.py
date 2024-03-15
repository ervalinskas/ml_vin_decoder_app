from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

CUSTOM_LITERAL = Literal["make", "model", "year", "body"]


class DataConfig(BaseModel):
    data_url: str
    raw_data_dir: str
    validated_data_dir: str
    preprocessed_labels_dir: str

    @property
    def raw_file_path(self):
        return Path(self.raw_data_dir) / "raw.csv"


class LogsConfig(BaseModel):
    logs_dir: str


class MLflowConfig(BaseModel):
    model_registry: str
    blob_store: str

    model_config = ConfigDict(protected_namespaces=())


class VectorizerConfig(BaseModel):
    ngram_range: list[int]
    analyzer: str


class ParamGridConfig(BaseModel):
    learning_rate: list[float]
    depth: list[int]


class HyperparamConfig(BaseModel):
    objective: Literal["binary:logistic", "multi:softprob"]
    eval_metric: Literal["accuracy"]
    param_grid: ParamGridConfig

class ModelingConfig(BaseModel):
    vectorizer: VectorizerConfig
    hyperparameters: HyperparamConfig


class AppConfig(BaseModel):
    data: DataConfig
    logs: LogsConfig
    mlflow: MLflowConfig
    modeling: ModelingConfig

    @classmethod
    def from_toml(cls, path: str) -> AppConfig:
        if isinstance(path, str):
            path = Path(path)

        with path.open(mode="rb") as f:
            data = tomllib.load(f)

        return cls(**data)

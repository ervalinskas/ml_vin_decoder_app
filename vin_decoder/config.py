from __future__ import annotations

import tomllib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

CUSTOM_LITERAL = Literal["make", "model", "year", "body"]


class PreprocessingConfig(BaseModel):
    labels_to_validate: list[CUSTOM_LITERAL]
    labels_to_preprocess: list[CUSTOM_LITERAL]


class DataConfig(BaseModel):
    data_url: str
    raw_data_dir: str
    validated_data_dir: str
    preprocessed_labels_dir: str
    preprocessing: PreprocessingConfig

    @property
    def raw_file_path(self):
        return Path(self.raw_data_dir) / "raw.csv"


class LogsConfig(BaseModel):
    logs_dir: str


class MLflowConfig(BaseModel):
    model_registry: str
    blob_store: str

    model_config = ConfigDict(protected_namespaces=())


class AppConfig(BaseModel):
    data: DataConfig
    logs: LogsConfig
    mlflow: MLflowConfig

    @classmethod
    def from_toml(cls, path: str) -> AppConfig:
        if isinstance(path, str):
            path = Path(path)

        with path.open(mode="rb") as f:
            data = tomllib.load(f)

        return cls(**data)

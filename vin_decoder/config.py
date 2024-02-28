from __future__ import annotations
from pydantic import BaseModel
import tomllib
from pathlib import Path


class DataConfig(BaseModel):
    data_url: str
    raw_data_dir: str
    validated_data_dir: str
    preprocessed_labels_dir: str


class LogsConfig(BaseModel):
    logs_dir: str


class MLflowConfig(BaseModel):
    model_registry: str
    blob_store: str


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

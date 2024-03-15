from __future__ import annotations

from pathlib import Path
from typing import Literal

import loguru
import pandas as pd

from vin_decoder.config import DataConfig


class Preprocessing:

    CUSTOM_MODEL_GROUP_1 = {
        "335": "3 Series",
        "4": "4 Series",
        "428I (USA)": "4 Series",
        "530D": "5 Series",
        "530D (EUR)": "5 Series",
        "M5": "5 Series",
        "630dx (630dx)": "6 Series",
        "640dx (640dx)": "6 Series",
        "S5": "A5",
        "rs 7": "A7",
        "SQ5": "Q5",
    }

    CUSTOM_MODEL_GROUP_2 = {
        "X1": "X Series",
        "X2": "X Series",
        "X3": "X Series",
        "X4": "X Series",
        "X5": "X Series",
        "X6": "X Series",
        "i3": "i",
        "i8": "i",
        "Z3": "Z Series",
        "Z4": "Z Series",
    }

    def __init__(
        self,
        validated_data_dir: Path,
        preprocessed_labels_dir: Path,
        target: Literal["make", "model", "year", "body"],
        logger: loguru.Logger,
    ) -> None:
        self.validated_data_dir = validated_data_dir
        self.preprocessed_labels_dir = preprocessed_labels_dir
        self.target = target
        self.logger = logger

    @classmethod
    def from_config(
        cls,
        config: DataConfig,
        target: Literal["make", "model", "year", "body"],
        logger: loguru.Logger,
    ) -> Preprocessing:
        return cls(
            validated_data_dir=Path(config.validated_data_dir),
            preprocessed_labels_dir=Path(config.preprocessed_labels_dir),
            target=target,
            logger=logger,
        )

    @staticmethod
    def map_labels(
        df: pd.DataFrame, label: Literal["make", "model", "year", "body"], d: dict
    ) -> pd.DataFrame:
        df[label] = df[label].map(d).fillna(df[label])
        return df

    @staticmethod
    def impute_missing_values(
        df: pd.DataFrame,
        label: Literal["make", "model", "year", "body"],
    ) -> pd.DataFrame:
        df[f"{label}_new"] = df.groupby("vin")[label].fillna(method="ffill")
        df[f"{label}_new"] = df.groupby("vin")[f"{label}_new"].fillna(method="bfill")

        # Some VINs consist only of NaN values
        df = df[df[f"{label}_new"].notnull()]
        df = df[["vin", f"{label}_new"]].rename(columns={f"{label}_new": label})
        return df

    def preprocess_data(self) -> None:
        df = pd.read_csv(
            Path(self.validated_data_dir, f"vin_{self.target}_pairs_good.csv")
        )
        df = df[["vin", self.target]].drop_duplicates()
        for d in [self.CUSTOM_MODEL_GROUP_1, self.CUSTOM_MODEL_GROUP_2]:
            df = self.map_labels(df=df, label=self.target, d=d)
        df = self.impute_missing_values(df=df, label=self.target)

        Path(self.preprocessed_labels_dir).mkdir(parents=True, exist_ok=True)

        df.to_csv(
            Path(self.preprocessed_labels_dir, f"vin_{self.target}_pairs_w_labels.csv"),
            index=False,
        )
        self.logger.info("✅ Label preprocessing is finished!")

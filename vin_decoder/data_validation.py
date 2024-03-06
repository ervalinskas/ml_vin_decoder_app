from __future__ import annotations
from typing import Callable
import loguru
from pathlib import Path

import pandas as pd

from vin_decoder.config import DataConfig


class Validation:

    def __init__(
        self,
        raw_file_path: Path,
        validated_data_dir: Path,
        labels_to_validate: list[str],
        logger: loguru.Logger,
    ) -> None:
        self.raw_file_path = raw_file_path
        self.validated_data_dir = validated_data_dir
        self.labels_to_validate = labels_to_validate
        self.logger = logger

    @classmethod
    def from_config(cls, config: DataConfig, logger: loguru.Logger) -> Validation:
        return cls(
            raw_file_path=config.raw_file_path,
            validated_data_dir=config.validated_data_dir,
            labels_to_validate=config.preprocessing.labels_to_validate,
            logger=logger,
        )

    @staticmethod
    def _check_for_conflicts(
        df: pd.DataFrame, col: str, gr_col: str = "vin"
    ) -> pd.DataFrame:
        vin_col_df = df[[gr_col, col]].drop_duplicates()
        non_null_vin_col_df = vin_col_df[vin_col_df[col].notnull()]
        non_null_vin_col_grouped = non_null_vin_col_df.groupby(gr_col)
        non_null_vin_col_conflicts = non_null_vin_col_grouped.filter(
            lambda x: x[col].nunique() > 1
        )
        return non_null_vin_col_conflicts

    @staticmethod
    def _get_conflicting_vins(
        df: pd.DataFrame,
        col: str,
        gr_col: str = "vin",
        func_list: list[Callable | str] = [set, "count"],
    ) -> pd.DataFrame:
        result = (
            df.groupby(gr_col).agg(func_list).rename(columns={"shortened_vin": "count"})
        )
        result.columns = result.columns.to_flat_index().str.join("_")
        result = result[result[col + "_count"] > 1].drop(columns=[col + "_count"])
        return result.reset_index()

    def validate_labels(self, df: pd.DataFrame, col: str, gr_col: str = "vin") -> None:
        check_df = self._check_for_conflicts(df=df, col=col)
        if not check_df.empty:
            self.logger.info(f"There are conflicts in the '{col}' column!")
            conflicts_df = self._get_conflicting_vins(df=check_df, col=col)

            good_vin_label_pairs = df.loc[
                ~df[gr_col].isin(conflicts_df[gr_col])
            ].sort_values(by=["vin", "make", "model", "year", "body"])

            Path(self.validated_data_dir).mkdir(parents=True, exist_ok=True)

            good_vin_label_pairs.to_csv(
                Path(self.validated_data_dir) / f"{gr_col}_{col}_pairs_good.csv",
                index=False,
                header=True,
            )

            bad_vin_label_pairs = df[
                df[gr_col].isin(conflicts_df[gr_col])
            ].sort_values(by=["vin", "make", "model", "year", "body"])
            
            bad_vin_label_pairs.to_csv(
                Path(self.validated_data_dir) / f"{gr_col}_{col}_pairs_bad.csv",
                index=False,
                header=True,
            )
        else:
            self.logger.info(f"There are no conflicts in the '{col}' column!")

    def validate_data(self) -> None:
        vins = pd.read_csv(self.raw_file_path)
        vins.drop_duplicates(inplace=True)

        for col in self.labels_to_validate:
            self.validate_labels(df=vins, col=col)

        self.logger.info("✅ Data validation is finished!")

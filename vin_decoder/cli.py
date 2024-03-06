import sys

import click
from loguru import logger

from vin_decoder.config import AppConfig
from vin_decoder.data_extraction import Extraction
from vin_decoder.data_preprocessing import Preprocessing
from vin_decoder.data_validation import Validation

logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


@click.group()
@click.option("--config_file_path", envvar="CONFIG_FILE_PATH", type=click.Path())
@click.pass_context
def vin_decoder(ctx, config_file_path):
    ctx.ensure_object(dict)
    ctx.obj["logger"] = logger
    ctx.obj["config"] = AppConfig.from_toml(path=config_file_path)


@vin_decoder.command()
@click.pass_context
def extract_data(ctx):
    extract = Extraction.from_config(
        config=ctx.obj["config"].data,
        logger=ctx.obj["logger"],
    )
    extract.extract_data()


@vin_decoder.command()
@click.pass_context
def validate_data(ctx):
    validate = Validation.from_config(
        config=ctx.obj["config"].data,
        logger=ctx.obj["logger"],
    )
    validate.validate_data()


@vin_decoder.command()
@click.pass_context
def preprocess_data(ctx):
    preprocess = Preprocessing.from_config(
        config=ctx.obj["config"].data,
        logger=ctx.obj["logger"],
    )
    preprocess.preprocess_data()

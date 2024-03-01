import click
from vin_decoder.config import AppConfig
from vin_decoder.data_extraction import Extraction


@click.group()
@click.option("--config_file_path", envvar="CONFIG_FILE_PATH", type=click.Path())
@click.pass_context
def vin_decoder(ctx, config_file_path):
    ctx.ensure_object(dict)
    ctx.obj["config"] = AppConfig.from_toml(path=config_file_path)


@vin_decoder.command()
@click.pass_context
def extract_data(ctx):
    config = ctx.obj["config"]
    extract = Extraction.from_config(config=config.data)
    extract._extract_data()

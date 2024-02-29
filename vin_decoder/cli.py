import click
from vin_decoder.config import AppConfig


@click.group()
@click.option("--config_file_path", envvar="CONFIG_FILE_PATH")
def vin_decoder(config_file_path):
    config = AppConfig.from_toml(path=config_file_path)


@vin_decoder.command()
def ingest_data():
    pass

import click
import os
from vin_decoder.config import AppConfig

CONFIG_PATH = os.environ["CONFIG_FILE_PATH"]
config = AppConfig.from_toml(path=CONFIG_PATH)


@click.command()
def ingest_data():
    pass


if __name__ == "__main__":
    ingest_data()

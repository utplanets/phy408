"""
data.py

This module contains functions for data loading for PHY408

"""
#imports
import numpy as np
import pandas as pd
import pooch
from importlib.resources import files


version = "v0.1"

registry = pooch.create(
    # Folder where the data will be stored. For a sensible default, use the
    # default cache folder for your OS.
    path=pooch.os_cache("phy408"),
    # Base URL of the remote data store. Will call .format on this string
    # to insert the version (see below).
    base_url="https://raw.githubusercontent.com/utplanets/phy408/refs/heads/{version}/",
    # Pooches are versioned so that you can use multiple versions of a
    # package simultaneously. Use PEP440 compliant version number. The
    # version will be appended to the path.
    version=version,
    # If a version as a "+XX.XXXXX" suffix, we'll assume that this is a dev
    # version and replace the version with this string.
    version_dev="main",
    # An environment variable that overwrites the path.
    env="PHY408_DATADIR",
    # The cache file registry. A dictionary with all files managed by this
    # pooch. Keys are the file names (relative to *base_url*) and values
    # are their respective SHA256 hashes. Files will be downloaded
    # automatically when needed (see fetch_gravity_data).
    # pooch.create()
    registry=None
)

reg_filename = files('phy408').joinpath('data_sources.txt')

registry.load_registry(
    reg_filename.open().read()
)


# Main function to demonstrate the usage of the module
def main():
    # Example usage
    from pathlib import Path
    root = Path(__file__).parent.parent/"data"
    for path_object in root.rglob('*'):
        if path_object.is_file():
            print(f"hi, I'm a file: {path_object}")

if __name__ == "__main__":
    main()

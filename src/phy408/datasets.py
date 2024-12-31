"""
data.py

This module contains functions for data loading for PHY408

"""
#imports
import numpy as np
import pandas as pd
import pooch
from importlib.resources import files
import os
import yaml
from pathlib import Path

version = "v0.1"

registry = pooch.create(
    # Folder where the data will be stored. For a sensible default, use the
    # default cache folder for your OS.
    path=pooch.os_cache("phy408"),
    # Base URL of the remote data store. Will call .format on this string
    # to insert the version (see below).
    base_url="https://raw.githubusercontent.com/utplanets/phy408/refs/heads/main/data",#{version}/",
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


def process_file(root,subdir, filedata,lt=None,verbose=False):
    lt = lt or ""
    filename = filedata["name"]
    sha256 = filedata["sha256"]
    path_object = root/subdir/filename
    if path_object.is_file():
        alg="sha256"
        if sha256 is None:
            if verbose:
                print(f"{lt}Processing data {filename}")
            sha256=pooch.file_hash(path_object, alg=alg)
            print(sha256)
        root_remove = os.path.normpath(str(root)) + os.sep
        po =    path_object.relative_to(root)
        return(po, sha256)
    else:
        po = path_object.relative_to(root)
        if verbose:
            print(f"File not found: {po}")
        raise NameError(f"File not found {po}")

def parse_structure(d,names, root=None,verbose=False):
    hashes=[]
    updated = False
    if root is None:
        root = Path(__file__)
    if isinstance(d,dict):
        lt = len(names)*"\t"
        name="TOP" if len(names)==0 else names[-1]
        if verbose:
            print(f"{lt}Processing files in {name}")
        if "files" in d:
            #it's data
            sub="/".join(names)
            for i,filedata in enumerate(d["files"]):
                path_object = root/sub
                po, sha256 = process_file(root,sub, filedata,lt="\t"*(len(names)),verbose=verbose)
                if sha256 != filedata["sha256"]:
                    d["files"][i]["sha256"] = sha256
                    updated=True
                hashes.append((po,"sha256",sha256))
        else:
            #directory?
            if verbose:
                print(f"{lt}Processing directory {name}")
            for k,v in d.items():
                newnames=list(names)
                newnames.append(k)
                hashdata, updated, newv = parse_structure(v,newnames,root=root,verbose=verbose)
                hashes.extend(hashdata)
                if updated:
                    d[k] = newv
    return(hashes, updated, d)



def init():
    reg_filename = files('phy408').joinpath('data_sources.yaml')
    yml = yaml.safe_load(open(reg_filename))
    hashes,updated, d = parse_structure(yml,[], root=Path(reg_filename).parents[2]/"data")
    data = dict((f"{line[0]}",f"{line[1]}:{line[2]}") for line in hashes)
    registry.registry.update(data)

init()

# Main function to demonstrate the usage of the module
def main():
    # Example usage
    from pathlib import Path
    root = Path(__file__).parents[2]/"data"
    for path_object in root.rglob('*'):
        if path_object.is_file() and path_object.suffix!=".zip":
            alg="sha256"
            hash=pooch.file_hash(path_object, alg=alg)
            root_remove = os.path.normpath(str(root)) + os.sep
            po = str(path_object).replace(root_remove,"")
            print(f"{po} {alg}:{hash}")

if __name__ == "__main__":
    main()

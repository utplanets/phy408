import click
import yaml
import pooch
import os
from pathlib import Path


@click.group()
def cli():
    pass

@cli.group()
def datasets():
    pass



@datasets.command()
@click.argument("input_filename")
def generate_registry(input_filename):
    from phy408 import datasets

    print("Generating Registry")
    yml = yaml.safe_load(open(input_filename))
    #top level is the directory
    hashes,updated, d = datasets.parse_structure(yml,[], root=Path(input_filename).parent)
#    for line in hashes:
#        print(f"{line[0]} {line[1]}:{line[2]}")
    if updated:
        yaml.safe_dump(d, open(input_filename,'w'))

if __name__ == '__main__':
    cli()

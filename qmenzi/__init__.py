import logging
import yaml
from functools import reduce

CONFIG = yaml.safe_load(open('config.yaml'))

def config(config_path):
    path = config_path.split('.')
    return reduce(lambda d, p: d.get(p, {}), path, CONFIG)

logging.basicConfig(level=logging.INFO)
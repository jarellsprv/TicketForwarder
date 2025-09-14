import os,json
from Logger import logger

directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data/input/config.json")

with open(directory, "r") as f:
    CONFIG = json.load(f)
    logger.suc("Loaded Config!")


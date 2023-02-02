import json
import logging
import os
from datetime import datetime


def get_logger(module_name: str) -> logging.Logger:  
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    return logger


logger = get_logger(__name__)


def get_env(key: str) -> str:
    try:
        return os.environ[key]
    except KeyError as e:
        logger.error(f'Environment variable {key} is not set')
        raise e
    
    
def read_json(path: str) -> dict:
    try:
        with open(path) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f'Error reading json file {path}')
        raise e

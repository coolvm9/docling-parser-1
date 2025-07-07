import logging
import logging.config
import sys
import os
import yaml

# Try root first, then fallback to app/core
ROOT_LOG_CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../logging_config.yaml'))
LOCAL_LOG_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'logging_config.yaml')


def setup_logging():
    config_path = ROOT_LOG_CONFIG_PATH if os.path.exists(ROOT_LOG_CONFIG_PATH) else LOCAL_LOG_CONFIG_PATH
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            level="INFO",
            format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            stream=sys.stdout,
            force=True,
        )

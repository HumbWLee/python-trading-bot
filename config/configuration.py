import json
import logging
import os
import pathlib
import sys
from json import JSONDecodeError


class Configuration:
    def __init__(self, config_name):
        self.__config = None
        logging.basicConfig(level=logging.INFO,
                            format='[%(asctime)s][%(levelname)s] %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            stream=sys.stdout)

        config_dir = "config/%s" % config_name

        if not os.path.isfile(config_dir):
            logging.error("[Config] Config File does not exist")
        else:
            try:
                with open(config_dir, "r", encoding="utf-8") as config_file:
                    self.__config = json.load(config_file)
            except JSONDecodeError as e:
                logging.error("[Config] Error in loading config")

    def get_connect_key(self):
        return self.__config["CONNECT_KEY"]

    def get_secret_key(self):
        return self.__config["SECRET_KEY"]

if __name__=="__main__":
    os.chdir(str(pathlib.Path(__file__).parent.parent.absolute()))
    config = Configuration('config_hhpp1231.json')
    print(config.get_secret_key())
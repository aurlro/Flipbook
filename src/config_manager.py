import configparser
import os

CONFIG_PATH = os.path.join("config", "settings.ini")

def load_config():
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_PATH):
        config.read(CONFIG_PATH, encoding="utf-8")
    else:
        create_default_config(config)
    return config

def create_default_config(config):
    config['paths'] = {
        'pdf_source': 'input/sample.pdf',
        'output_folder': 'output'
    }
    config['settings'] = {
        'quality': 'medium'
    }
    config['sharepoint'] = {
        'url': '',
        'username': '',
        'password': '',
        'folder': 'Documents/Flipbooks'
    }
    save_config(config)

def save_config(config):
    os.makedirs('config', exist_ok=True)
    with open(CONFIG_PATH, 'w', encoding="utf-8") as configfile:
        config.write(configfile)

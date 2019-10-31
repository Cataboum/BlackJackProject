import os
import json
from src.common.config import ConfigPath

def test_config_path():
    file_config_path = os.path.join("data", "config", "path.cfg.json")

    ConfigPath.initialize(file_config_path)
    with open(file_config_path) as f:
        paths = json.load(f)
    
    assert ConfigPath.get("folders", "data") == os.path.abspath(os.path.join(*paths["folders"]["data"]))
    assert ConfigPath.folder("data") == os.path.abspath(os.path.join(*paths["folders"]["data"]))

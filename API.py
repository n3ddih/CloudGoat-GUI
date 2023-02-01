import os
import yaml
import re
from flask import jsonify
from pathlib import Path
from configparser import ConfigParser
import Utils
from core.python.commands import CloudGoat
from core.python.utils import create_or_update_yaml_file

cg = CloudGoat('./')
default_profile = "cloudgoat"

def scenario_list():
    results = Utils.get_scenarios_from_markdown()
    return jsonify(results), 200

def scenario_detail(scenario_id):
    if not Utils.check_scenario_name(scenario_id):
        return "Invalid scenario id!", 400
    scenario_manifest = open(f'./scenarios/{scenario_id}/manifest.yml', 'r')
    loaded = yaml.safe_load(scenario_manifest)
    sname = list(loaded[0].values())[0]
    sauthor = list(loaded[1].values())[0]
    sversion = list(loaded[2].values())[0]
    shelp = list(loaded[3].values())[0]
    slast_updated = list(loaded[4].values())[0]
    results = {
        'name':sname,
        'author':sauthor,
        'version':sversion,
        'help':shelp,
        'last_updated':slast_updated
    }
    return jsonify(results), 200    

def config_profile(profile):
    # If the profile is not by default, use the input profile
    if profile == "" or profile is None:
        return "Profile name invalid!", 400
    create_or_update_yaml_file(cg.config_path, {"default-profile": profile})
    return "Configure successful!", 200
    
def configure_credentials(access_key_id, secret_access_key):
    aws_path = str(Path.home()) + '/.aws/'
    # Create ~/.aws directory if not exist
    if not os.path.exists(aws_path):
        os.makedirs(aws_path)

    config = ConfigParser()
    # Edit credentials file
    path = aws_path + 'credentials'
    if os.path.exists(path):
        config.read(path)
    config[default_profile] = {
        'aws_access_key_id': access_key_id,
        'aws_secret_access_key': secret_access_key
    }
    with open(path, 'w') as configfile:
        config.write(configfile)

    # Edit config file
    path = aws_path + 'config'
    if os.path.exists(path):
        config.read(path)
    config['profile ' + default_profile] = {
        'region': 'us-east-1',
        'output': 'json'
    }
    with open(path, 'w') as configfile:
        config.write(configfile)
    
    config_profile(default_profile)
    return "Configure successful!", 200
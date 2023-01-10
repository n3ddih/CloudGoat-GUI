import os
import yaml
from flask import jsonify
from core.python.commands import CloudGoat
from core.python.utils import create_or_update_yaml_file

cg = CloudGoat('./')

def scenario_list():
    results = {}
    names = os.listdir('./cloudgoat/scenarios')
    # file = open('./cloudgoat/README.md', 'r', encoding='UTF-8')
    # data = file.read()
    for name in names:
        summary = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eget arcu dictum varius duis at. Felis bibendum ut tristique et egestas. Pellentesque sit amet porttitor eget dolor morbi. Ut placerat orci nulla pellentesque dignissim enim.'
        item = {
            'summary': summary
        }
        results.update({name:item})
        print(results)
    return jsonify(results), 200

def scenario_detail(scenario_id):
    try:
        scenario_manifest = open(f'./cloudgoat/scenarios/{scenario_id}/manifest.yml', 'r')
    except FileNotFoundError:
        return "Scenario not found!", 400
    loaded = yaml.load(scenario_manifest, Loader=yaml.CLoader)
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

def config_profile(profile="cloudgoat"):
    # If the profile is not by default, use the input profile
    if profile == "" or profile is None:
        return "Profile name invalid!", 400
    create_or_update_yaml_file(cg.config_path, {"default-profile": profile})
    return "Configure successful!", 200
    
def configure_credentials(access_key_id, secret_access_key):
    credentials = open('~/.aws/credentials', 'a')
    credentials.write("\n[cloudgoat]\naws_access_key_id = "+ access_key_id +"\naws_secret_access_key = "+ secret_access_key +"\n")
    credentials.close()
    config = open('~/.aws/config', 'a')
    config.write("\n[cloudgoat]\nregion = us-east-1\noutput = json")
    config.close()
    config_profile()
    return "Configure successful!", 200
import subprocess
import sys
from flask import Flask, render_template
from flask_cors import CORS
import Utils
import datetime
import git
import shutil
import os
import yaml

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    Utils.update_cloudgoat()
    return render_template('index.html', title="Home")

@app.route('/scenario_list')
def view_scenario_list():
    return render_template('scenario/list.html', title="Scenario List")

@app.route('/scenario/<scenario_id>')
def view_scenario_detail(scenario_id):
    return render_template('scenario/detail.html', title="Scenario Detail", id=scenario_id)

@app.route('/api/scenario')
def scenario_list():
    results, code = API.scenario_list()
    return results, code

@app.route('/api/scenario/<scenario_id>')
def scenario_detail(scenario_id):
    results, code = API.scenario_detail()
    return results, code

if __name__ == '__main__':
    # clone cloudgoat if core or scenarios folder not exist
    if not os.path.exists('./core') or not os.path.exists('./scenarios'):
        print("[!] cloudgoat engine not found!")
        Utils.clone_repo("./cloudgoat", "https://github.com/RhinoSecurityLabs/cloudgoat.git")
        print("[*] Clone folder complete!")
        Utils.copy_neccessary_files()
    # Check version and requirements
    Utils.check_requirement()
    import API
    # Start server
    app.run('0.0.0.0', '5000', debug=True)
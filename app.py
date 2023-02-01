from flask import Flask, render_template, request
from flask_cors import CORS
import Utils
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    Utils.update_cloudgoat()
    return render_template('index.html', title="Home")

@app.route('/scenario_list')
def view_scenario_list():
    scenario_list = Utils.get_scenarios_from_markdown()
    return render_template('scenario/list.html', title="Scenario List", scenario_list=scenario_list, len=len(scenario_list))

@app.route('/scenario/<scenario_id>')
def view_scenario_detail(scenario_id):
    return render_template('scenario/detail.html', title="Scenario Detail", id=scenario_id)

@app.route('/api/scenario')
def scenario_list():
    results, code = API.scenario_list()
    return results, code

@app.route('/api/scenario/<scenario_id>')
def scenario_detail(scenario_id):
    results, code = API.scenario_detail(scenario_id)
    return results, code

@app.route('/api/config/profile', methods=['POST'])
def config_profile():
    data = request.get_json()
    profile = data['profile']
    if profile == '':
        return "You must include a profile name", 400
    result, code = API.config_profile(profile)
    return result, code

@app.route('/api/config/credential', methods=['POST'])
def config_credential():
    data = request.get_json()
    access_key_id = data['access_key_id']
    secret_key = data['secret_access_key']
    if access_key_id == '' or secret_key == '':
        return "You must include both keys", 400
    result, code = API.configure_credentials(access_key_id, secret_key)
    return result, code
    

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
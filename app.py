from flask import Flask, render_template, jsonify
from flask_cors import CORS
import datetime
import git
import os
import yaml

app = Flask(__name__)
CORS(app)
cloudgoat_path = './cloudgoat'

def clone_repo(dir, git_url):
    print("Clonning repo...")
    return git.Git(dir).clone(git_url)

def pull_repo(git_folder):
    print("[*] Pulling codes...")
    repo = git.Repo(git_folder)
    return repo.remotes.origin.pull()

def check_repo_changed(git_folder):
    print("[*] Checking changes in repo...")
    repo = git.Repo(git_folder)
    current = repo.head.commit
    repo.remotes.origin.pull()
    if current != repo.head.commit:
        print("[!] The repo changed!")
        return True
    return False

@app.route('/')
def index():
    # Update CloudGoat repo after 10 days and if there're any changes
    if datetime.datetime.now().day % 10 == 0:
        if check_repo_changed(cloudgoat_path):
            pull_repo(cloudgoat_path)
    
    return render_template('index.html', title="Home")

def view_scenario_list():
    return render_template('')

@app.route('/api/scenario')
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

@app.route('/api/scenario/<scenario_id>')
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

if __name__ == '__main__':
    # clone cloudgoat if folder not exist
    if not os.path.exists('./cloudgoat'):
        print("[!] cloudgoat folder not found!")
        clone_repo("./cloudgoat", "https://github.com/RhinoSecurityLabs/cloudgoat.git")
    # Start server
    app.run('0.0.0.0', '5000', debug=True)
import datetime
import shutil
import git
import sys
import subprocess
import re
import mistune
from os import listdir
from scenario import Scenario

def clone_repo(dir, git_url):
    print("Clonning repo...")
    return git.Git(dir).clone(git_url)

def update_cloudgoat():
    # Update CloudGoat repo every first day of the month and if there're any changes
    if datetime.datetime.now().day != 1:
        return False
    
    clone_repo("./cloudgoat", "https://github.com/RhinoSecurityLabs/cloudgoat.git")
    copy_neccessary_files()
    return True

def check_requirement():
    if sys.version_info[0] < 3 or (
        sys.version_info[0] >= 3 and sys.version_info[1] < 6
    ):
        print("CloudGoat requires Python 3.6+ to run.")
        sys.exit(1)

    try:
        terraform_version_process = subprocess.Popen(
            ["terraform", "--version"], stdout=subprocess.PIPE
        )
    except FileNotFoundError:
        print("Terraform not found. Please install Terraform before using CloudGoat.")
        sys.exit(1)

    terraform_version = terraform_version_process.stdout.read().decode("utf-8")
    terraform_version_process.wait()
    version_number = re.findall(
        r"^Terraform\ v(\d+\.\d+)\.\d+\s",
        terraform_version,
    )

    if not version_number:
        print("Terraform not found. Please install Terraform before using CloudGoat.")
        sys.exit(1)

    major_version, minor_version = version_number[0].split(".")
    if int(major_version) == 0 and int(minor_version) < 11:
        print(
            "Your version of Terraform is v{}. CloudGoat requires Terraform v0.12 or"
            " higher to run.".format(version_number[0])
        )
        sys.exit(1)
    return True

def copy_neccessary_files():
    print("[*] Copy neccessary files to the main working tree...")
    try:
        shutil.copytree('./cloudgoat/core', './core')
        shutil.copytree('./cloudgoat/scenarios', './scenarios')
        shutil.copy('./cloudgoat/README.md', './cg-README.md')
        print("[*] Copy complete!")
        shutil.rmtree('./cloudgoat')
    except:
        return False
    return True

def get_scenario_index(markdown_json):
    for i in range(len(markdown_json)):
        try:
            text = markdown_json[i]['children'][0]['text']
            if text == "Scenarios Available":
                return i
        except:
            continue
    return 0

def get_max_scenario_name_length():
    return len(max(listdir('./scenarios'), key=len))

def check_scenario_name(name):
    regex = r"([A-Za-z0-9]+(_[A-Za-z0-9]+)+)"
    if len(name) > get_max_scenario_name_length() or not re.match(regex, name) or name not in listdir('./scenarios'):
        return False
    return True

def check_scenario_line(line):
    regex = r"([A-Za-z0-9]+(_[A-Za-z0-9]+)+) \([^)]+\)"
    if not re.match(regex, line):
        return False
    return True

def extract_scenarios(markdown_json):
    result = []
    start_index = get_scenario_index(markdown_json)
    while True:
        try:
            text = markdown_json[start_index]['children'][0]['text']
        except:
            start_index += 1
            continue
        if text == "Usage Guide":
            break
        if not check_scenario_line(text):
            start_index += 1
            continue
        text = text.split(' ')
        name = text[0]
        size = text[1][1:]
        difficulty = text[3][:-1]
        summary = markdown_json[start_index + 2]['children'][0]['text']
        start_index += 4
        scenario = Scenario(name, summary, size, difficulty)
        result.append(scenario.get_detail_info())
    return result

def get_scenarios_from_markdown():
    filename = 'cg-README.md'
    markdown = mistune.create_markdown(renderer='ast')
    file = open(filename, 'r')
    md_json = markdown(file.read())
    file.close()
    extracted = extract_scenarios(md_json)
    return extracted
import datetime
import shutil
import git
import sys
import subprocess
import re

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

    terraform_version_process.wait()

    version_number = re.findall(
        r"^Terraform\ v(\d+\.\d+)\.\d+\s",
        terraform_version_process.stdout.read().decode("utf-8"),
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
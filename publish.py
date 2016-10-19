#!/usr/bin/env python3

import os
import platform
import shutil
import semver
import argparse
import getpass
import subprocess
from pathlib import Path

# ------------------------------------------------
#   Script used to publish the version on github
# ------------------------------------------------

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--patch", help="bump patch version",
                    action="store_true")
parser.add_argument("-m", "--minor", help="bump minor version",
                    action="store_true")
parser.add_argument("-M", "--major", help="bump major version",
                    action="store_true")

args = parser.parse_args()
if not args.patch and not args.minor and not args.major:
    print("Error: should pass as a parameter either, -p, -m or -M to bump" +
          " version")
    exit(1)

print("Generating sublime plugin from sublime package folder...")

OS = platform.system()
MAC_OS = "Darwin"
USER = getpass.getuser()
PACKAGE_DEV_DIRECTORY = "hermes"
# Exclude files patterns from copy
EXCLUDE_FILES = ["package-metadata.json", "*.pyc"]
VERSION_FILE = "VERSION"
VERSION_FILE_PATH = Path("./" + VERSION_FILE)
KEEP_FILES = [".git", ".gitignore", "publish.py", "README.md", VERSION_FILE]
CURRENT_PATH = Path.cwd()

if OS == MAC_OS:
    plugin_location = Path("/Users/" + USER + "/Library/Application Support/" +
                           "Sublime Text 3/Packages/" + PACKAGE_DEV_DIRECTORY)
else:
    print("Error: Operating system not handled, please add your OS to the" +
          "publish script")
    exit(1)
print("Locating plugin:" + str(plugin_location))

if not plugin_location.exists():
    print("Error: Could not find the sublime package to publish")
    exit(1)


# Clean up the current folder
for file in os.listdir("."):
    if file not in KEEP_FILES:
        if os.path.isdir(file):
            shutil.rmtree(file)
        else:
            os.remove(file)

# Copying files
for filePath in list(plugin_location.glob("**/*")):
    for excluded_file in EXCLUDE_FILES:
        if filePath.match(excluded_file):
            continue

    if filePath.is_file():
        print("Copying " + str(filePath))
        print("to " + str(CURRENT_PATH / filePath.name))
        shutil.copy(str(filePath), str(CURRENT_PATH / filePath.name))
    else:
        print("Directory detected in plugin folder, not implemented")
        print(str(filePath))
        exit(1)

# Bump version
version = VERSION_FILE_PATH.read_text()
if args.major:
    version = semver.bump_major(version)
elif args.minor:
    version = semver.bump_minor(version)
else:
    version = semver.bump_patch(version)
VERSION_FILE_PATH.write_text(version)

# git commit and tag
subprocess.call(["git", "add", "-A"])
subprocess.call(["git", "commit", "-m", "'Publish version" + version + "'"])
subprocess.call(["git", "tag", version])
subprocess.call(["git", "push", "--all"])

print("New version published")

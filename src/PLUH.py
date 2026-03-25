#----Imports-------
import os
import subprocess
import sys

#----Welcome-------
print("""    _          ______
            |_|  |      |          |  |
            |    |      |          |--|
            |    |_     |_____     |  |  \n""")
print("Welcome to PyLibUpdaterHelper (PLUH)!")

#----Questions-------
lib_path = input("Q0. What is the path of your library's root folder? (e.g. C:\\Users\\me\\mylib) *")
new_version = input("Q1. What is the new version? (e.g. 0.2.0) *")

if lib_path == "" or new_version == "":
    print("ERROR: both questions are required.")
    sys.exit(1)

#----Update pyproject.toml-------
toml_path = os.path.join(lib_path, "pyproject.toml")

if not os.path.exists(toml_path):
    print("ERROR: pyproject.toml not found in this folder.")
    sys.exit(1)

with open(toml_path, "r") as f:
    content = f.read()

# Remplacer la version
import re
content = re.sub(r'version = ".*?"', f'version = "{new_version}"', content)

with open(toml_path, "w") as f:
    f.write(content)

print("pyproject.toml updated!")

#----Build-------
print("Building...")
subprocess.run([sys.executable, "-m", "build"], cwd=lib_path)

#----Upload-------
print("\n⚠️  Your API key will NEVER be saved anywhere.")
api_key = input("Enter your PyPI API key (or leave blank to skip): ")

if api_key != "":
    subprocess.run([
        sys.executable, "-m", "twine", "upload",
        "--username", "__token__",
        "--password", api_key,
        "dist/*"
    ], cwd=lib_path)
    print("Library updated on PyPI!")
    del api_key
else:
    print("Skipped. You can upload manually with: twine upload dist/*")

print("Done!")

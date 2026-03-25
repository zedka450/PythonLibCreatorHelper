#----Imports-------

import subprocess
import sys

#----Help_PyPI-------

def create_pypi_account():
    print("1. Go to https://pypi.org/account/register/ and inter your username, email and password and pass the captcha. Then click on 'Register'.")
    print("2. You will receive an email with a verification link. Click on the link to verify your email.")
    print("3. after, sign in to your account https://pypi.org/account/login/ .")
    print("4. Pass 2FA, if you don't have a phone, you can use an authenticator app like Authy or Google Authenticator or KeyPassXC.")
    print("5. After you sign in, go to your account settings https://pypi.org/manage/account/ and scroll down to the 'API tokens' section. Click on 'Add API token'.")
    print("6. Enter a name for your token (e.g. 'PLCH token') and select the 'Entire account' scope. Then click on 'Add API token'.")
    print("7. You will see your API token. Copy it and save it in a safe place, you won't be able to see it again. You will need it to upload your library to PyPI.")
    print("8. Now you have a PyPI account and an API token, you can continue the program process. ")

while True:

    #----Welcome-------

    print("""_          ______
            |_|  |      |          |  |
            |    |      |          |--|
            |    |_     |_____     |  |  \n""")
    print("Welcome to PythonLibCreatorHelper (PLCH)! \n This tool will help you create a Python library. \n For create a library, you need to answer some questions. ")

    #----Questions-------

    responses = []
    print("   (Mark for required questions: '*') \n")

    responses.append(input("Q0. What is the name of your library? *"))

    responses.append(input("Q1. What is the description of your library? *"))

    responses.append(input("Q2. What is the version of your library? (e.g. 0.1.0) (or leave it blank for default 0.1.0) *"))

    responses.append(input("Q3. Who is the author of your library?  *"))

    responses.append(input("Q4. What is the email of the author? (or leave it blank for none) "))

    responses.append(input("Q5. What is the license of your library? (e.g. MIT) (or leave it blank for none) "))

    responses.append(input("Q6. What is the GitHub repository of your library? (or leave it blank for none) "))

    responses.append(input(r"Q7. What is the path+name of the file that contains the definitions of your library? (e.g. C:\Users\me\mylib.py) (or leave it blank for none) *"))

    responses.append(input("Q8. What is the PyPI username of the author? (or leave it blank for none, we'll help you create it.) "))

    responses.append(input("Q9. What is the README of your library? (or leave it blank for none, it will be replaced with the description.) *"))

    #----examination of answers-------

    if responses[0] == "" or responses[1] == "" or responses[3] == "":
        print("ERROR: questions 0, 1 and 3 are required. Please answer them and run the program again.")
        continue
    elif responses[7] =="":
        print("ERROR: need a file with the definitions of the library. Please create it and restart the program.")
        subprocess.run([sys.executable, "main.py"])
        sys.exit(1)
    elif responses[8] == "":
        print("If you don't have a PYPI account, we can help you create it. Please follow the instructions in the next steps.")
        create_pypi_account()
        responses[8] = input("What is your PyPI username? ")
    elif responses[9] == "":
        responses[9] = responses[1]
    else:
        print("Thank you for your answers! We will now create your library. Please wait...")

    #----Library creation-------

    import os
    import shutil

    root_dir = os.path.join(os.path.dirname(__file__), responses[0])
    os.makedirs(root_dir, exist_ok=True)

    code_dir = os.path.join(root_dir, responses[0])
    os.makedirs(code_dir, exist_ok=True)

    shutil.copy(responses[7], os.path.join(code_dir, "__init__.py"))

    with open(os.path.join(root_dir, "README.md"), "w") as f:
        f.write(f"# {responses[0]}\n\n{responses[9]}")

    print("Folders and files created!")

    pyproject_content = f"""[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "{responses[0]}"
version = "{responses[2] if responses[2] != "" else "0.1.0"}"
description = "{responses[1]}"
authors = [{{name = "{responses[3]}", email = "{responses[4]}"}}]
readme = "README.md"
license = {{text = "{responses[5]}"}}

[project.urls]
Homepage = "{responses[6]}"
"""

    with open(os.path.join(root_dir, "pyproject.toml"), "w") as f:
        f.write(pyproject_content)

    print("pyproject.toml created!")

    print("Installing build and twine...")
    subprocess.run([sys.executable, "-m", "pip", "install", "build", "twine"])

    print("Building the library...")
    subprocess.run([sys.executable, "-m", "build"], cwd=root_dir)

    print("Build done!")

    print("\n⚠️  Your API key will NEVER be saved anywhere.")
    api_key = input("Enter your PyPI API key to upload (or leave blank to skip): ")

    if api_key != "":
        subprocess.run([
            sys.executable, "-m", "twine", "upload",
            "--username", "__token__",
            "--password", api_key,
            "dist/*"
        ], cwd=root_dir)
        print("Library uploaded to PyPI!")
        del api_key  # supprimer la clé de la mémoire
    else:
        print("Skipped upload. You can upload manually later with: twine upload dist/*")

    print("\nDone! Your library is ready.")
    break


import os

from setuptools import setup, find_packages
from typing import List

HYPHEN_E_DOT = "-e ."
REQUIREMENTS_FILE_PATH = os.path.join(os.getcwd(), "requirements.txt")

def get_requirements() -> List[str]:
    """
    Get requirements from requirements.txt file: This function will return list of requirements from requirements.txt file.
    """
    with open(REQUIREMENTS_FILE_PATH, "r", encoding='utf-8') as requirements_file:
        requirement_list = requirements_file.readlines()
        requirement_list = [requirement.replace("\n", "") for requirement in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        print(requirement_list)
    return requirement_list

setup(
    name="FatsAPI_CRUD_APP",
    version="0.1.0",
    packages=find_packages(),
    install_requires=get_requirements(),
)

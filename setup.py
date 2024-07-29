from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    """
    This function will return a list of requirements from a given file.

    Args:
        file_path (str): Path to the requirements file.

    Returns:
        List[str]: List of requirements.
    """
    requirements = []
    with open(file_path) as file:
        requirements = [line.strip() for line in file.readlines()]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements


setup(
    name='Malaria Parasite Detection',
    version='0.0.1',
    author='Adebowale Aderogba',
    author_email='eaderogba279@stu.ui.edu.ng',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)

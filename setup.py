import pathlib

import pkg_resources
from setuptools import find_packages, setup


def requirements(filepath: str):
    with pathlib.Path(filepath).open() as requirements_txt:
        return [
            str(requirement) for requirement in pkg_resources.parse_requirements(requirements_txt)
        ]


setup(
    name='PythonDevelopment2023',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    description='repo for MSU course',
    author='Alexander Vorontsov',
    author_email='makler322@gmail.com',
    url='https://github.com/makler322/PythonDevelopment2023/',
    python_requires='>=3.9',
    packages=find_packages(include=('development',)),
    install_requires=requirements('requirements.txt'),
    extras_require={'dev': requirements('requirements.dev.txt')},
)

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="exam_manager",
    version="0.1.0",
    author="canutoilberto",
    author_email="canutoilberto@gmail.com",
    description="Sistema de gerenciamento de provas e exames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/canutoilberto/exam_manager",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
)

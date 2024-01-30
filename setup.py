from setuptools import find_packages
from setuptools import setup

# pip install setuptools wheel
# python setup.py sdist bdist_wheel
# pip install twine
# pip install --upgrade pip setuptools twine
# twine upload dist/*

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="CHA",
    version="0.1.0",
    author="Mahyar Abbasian",
    author_email="example@email.com",
    description=(
        "Conversational Health Agents (CHAs) are interactive systems designed to enhance personal"
        "healthcare services by engaging in empathetic conversations and processing multimodal data. "
    ),
    # packages=find_packages(),
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Institute4FutureHealth/CHA.git",
    download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',
    install_requires=[
        "httpcore==1.0.2",
        "requests",
        "gradio",
        "pydantic",
        "scipy",
    ],
    extras_require={
        "all": [
            # all requirements
            "anthropic",
            "aiohttp",
            "google-search-results",
            "pdfminer.six",
            "googletrans-py",
            "playwright",
            "beautifulsoup4",
            "lxml",
            "tiktoken",
            "openai~=1.2",
            "pandas",
            "scipy",
            "seaborn",
            "neurokit2",
            "torch",
            "torchvision",
            "torchdata",
        ],
        "minimum": [
            # minimum requirements for running the codes
            "aiohttp",
            "google-search-results",
            "pdfminer.six",
            "playwright",
            "beautifulsoup4",
            "lxml",
            "tiktoken",
            "openai~=1.2",
        ],
        "develop": [
            "sphinx",
            "sphinx-copybutton",
            "sphinxcontrib-video",
            "sphinxcontrib.youtube",
            "pydata_sphinx_theme",
            "pytest",
            "pytest-mock",
            "pytest-asyncio",
        ],
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9, <3.12",
)

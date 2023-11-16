from setuptools import setup, find_packages

# pip install setuptools wheel
# python setup.py sdist bdist_wheel
# pip install twine
# pip install --upgrade pip setuptools twine
# twine upload dist/*



setup(
    name='CHA',
    version='0.1.0',
    author="Mahyar Abbasian",
    description="Conversational Health Agents (CHAs) are interactive systems designed to enhance personal healthcare services by engaging in empathetic conversations and processing multimodal data. ",
    packages=find_packages(),
    url="https://github.com/Mahyar12/CHA",
    install_requires=[
        'requests',
        'gradio',
        'pydantic'
    ],
    extras_require={
        'all': [
            # all requirements
            'anthropic',
            'aiohttp',
            'google-search-results',
            'playwright',
            'beautifulsoup4',
            'lxml',
            'tiktoken',
            'openai~=1.2'
        ],
        'minimum': [
            # minimum requirements for running the codes
            'aiohttp',
            'google-search-results',
            'playwright',
            'beautifulsoup4',
            'lxml',
            'tiktoken',
            'openai~=1.2'
        ],
        'develop': [
            'sphinx',
            'sphinx-copybutton',
            'sphinxcontrib-video',
            'sphinxcontrib.youtube',
            'pydata_sphinx_theme'
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires=">=3.9, <3.12",
)
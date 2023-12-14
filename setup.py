from setuptools import setup, find_packages

setup(
    name='SVN Repository Analyser',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'matplotlib==3.7.2',
        'tk==0.1.0',
        # Add any other dependencies your project requires
    ],
    url='https://csee.essex.ac.uk/svn/ce320-07',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)


#from distutils.core import setup
from setuptools import setup

setup(
    # How you named your package folder (MyLib)
    name='diacritization_evaluation',
    packages=['diacritization_evaluation'],   # Chose the same as "name"
    version='0.5',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='This package calculates Diacritization Error Rate (DER) and Word Error Rate (WER)',
    author='Mokhtar Madhfar',                   # Type in your name
    author_email='mokhtarmodhfer@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/almodhfer/diacritization_evaluation',
    # I explain this later on
    download_url='https://github.com/almodhfer/diacritization_evaluation/archive',
    # Keywords that define your package best
    keywords=['diacritization', 'WER', 'DER'],
    install_requires=[            # I get to this in a second
        # 'validators',
        # 'beautifulsoup4',
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 5 - Production/Stable',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)

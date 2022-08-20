from setuptools import find_packages, setup

setup(
    name='Regression App',
    version='0.1',
    description='A Python GUI app for performing different types of regressions',
    author='Kevin Yang',
    author_email='kevinyang10@gmail.com',
    url='https://github.com/keviny2/Regression-App',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'regression-app=src.cli:run',
        ]
    }
)

from setuptools import setup, find_packages

VERSION="0.2.0"

setup(
    name='krita_stable_diffusion',
    version=VERSION,
    description='',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
        'tqdm',
    ],
)

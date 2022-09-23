from setuptools import setup, find_packages

VERSION="0.2.1"  # This line is required for the packager. Do not remove it.

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

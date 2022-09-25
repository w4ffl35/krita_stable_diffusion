from setuptools import setup, find_packages

# This line is required for the packager. Do not remove it.
VERSION = "0.2.1"

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

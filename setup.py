from setuptools import setup, find_packages

setup(
    name='krita_stable_diffusion',
    version='0.6.0',
    description='',
    packages=find_packages(),
    install_requires=[
        'torch',
        'numpy',
        'tqdm',
    ],
)
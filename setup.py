from setuptools import setup, find_packages

# This line is required for the packager. Do not remove it.
VERSION = "0.3.1"

setup(
    name='krita_stable_diffusion',
    version=VERSION,
    description='',
    packages=find_packages(),
    install_requires=[
        "diffusers",
        "stablediffusion @ git+https://github.com/w4ffl35/stable-diffusion.git@feature/windows-support#egg=stablediffusion",
    ],
)

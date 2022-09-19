# Krita Stable Diffusion

A Krita plugin for Stable Diffusion

[See demo video on youtube](https://www.youtube.com/watch?v=maWR7dDf4SE)

## Installation

### System requirements

This plugin will run on a variety of systems. As it is tested the results will
be listed below.

If you have a different system than the one listed below, [please post your 
results in this discussion thread](https://github.com/w4ffl35/krita_stable_diffusion/discussions/16).


| OS |    GPU    |      CPU      | HD Space | RAM | Krita | Cuda Drivers |
|:---:|:---------:|:-------------:|:---------:|:---:|:-----:|:------------:|
| Ubuntu 20.04 | RTX 2080s | Ryzen 7 2700x | 20gb | 32GB | 4.2.9 |     11.3     |

---

### Install cuda 11.3 drivers for GPU support

[Follow the instructions for your platform here](https://developer.nvidia.com/cuda-11.3.0-download-archive)

### Setup krita plugin

1. [Download the latest release from github](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.1.0/krita_stable_diffusion-0.1.0.zip) and unzip it.
2. Place `krita-stable-diffusion` folder into Krita plugins folder (usually `~/.local/share/krita/pykrita`, if `~/.local/share/krita` exists but `pykrita` doesn't, then add it). You can find

![img.png](img.png)

**Krita resources folder can be found under `Settings > Manage Resources` then click the `Open Resource Folder` button.**

### Setup the model and config file

1. [Download stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4)
2. Rename it to `model.ckpt` and place it into `krita_stable_diffusion`
3. Copy `krita_stable_diffusion/stablediffusion/configs/stable-diffusion/v1-inference.yaml` to `krita_stable_diffusion`

Your directory structure should look like this (assuming krita has a typical installation)

```
~/.local/share/krita/pykrita/
├── krita-stable-diffusion
│   ├── interface
│   ├── ...
│   └── stablediffusion
│       └── ...
│       └── model.ckpt
│       └── v1-inference.yaml
└── krita_stable_diffusion.py
└── settings.py
└── ...
```

### Create python environment

1. Create python env `conda env create -f environment.yaml`
2. Activate python env `conda activate kritastabeldiffusion`

### OPTIONAL: Install stablediffusiond

If you plan to use `stablediffusiond` daemons to run Stable Diffusion and handle
requests and responses, you will need to install `stablediffusiond`. 

#### Local installation

1. clone stablediffusiond into the `krita-stable-diffusion` directory `git clone https://github.com/w4ffl35/stablediffusiond.git`
2. [Follow installation instructions](https://github.com/w4ffl35/stablediffusiond#installation) for stablediffusiond, adapting it for your stack
3. move the `model.cpkt` and `v1-inference.yaml` file into the `stablediffusiond` directory

**Note** Although stablediffusiond was designed to be run as a distrubted service, this
has not been tested. 

Your directory structure should look like this (assuming krita has a typical installation)

```
~/.local/share/krita/pykrita/
├── krita-stable-diffusion
│   ├── interface
│   ├── ...
│   └── stablediffusion
│   └── stablediffusiond
│       └── src
│           └── settings.py
│           └── ...
│       └── model.ckpt
│       └── v1-inference.yaml
└── krita_stable_diffusion.py
└── settings.py
└── ...
```

Please post your results on the [stablediffusiond discussion board](https://github.com/w4ffl35/stablediffusiond/discussions).

### Enable the plugin

1. Start Krita (or restart if it was running)
2. Enable the plugin in the settings `Settings > Configure Krita > Python Plugin Manager`

![img_1.png](img_1.png)

**Enable the plugin from within the Python Plugin Manager**

`Settings > Configure Krita > Python Plugin Manager`

## Tools

Tools contains a custom size property (512x512) and template (single layer, no background) 
for Stable Diffusion projects.


### Conda commands

- Create `conda env create -f environment.yaml`
- Recreate `conda env update --prefix ./env --file environment.yaml  --prune`
- Activate `conda activate kritastabeldiffusion`
- Deactivate `conda deactivate`
- Destroy `conda env remove -n kritastabeldiffusion`

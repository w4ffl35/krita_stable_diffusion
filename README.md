# Krita Stable Diffusion

A Krita plugin for Stable Diffusion

[See demo video on youtube](https://www.youtube.com/watch?v=maWR7dDf4SE)

**This plugin is currently expected to run on linux.** 

Windows support coming soon.

## Installation

### Install cuda 11.3 drivers

[Follow the instructions for your platform here](https://developer.nvidia.com/cuda-11.3.0-download-archive)

### Setup krita plugin

1. [Download the latest release from github](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.1.0/krita_stable_diffusion-0.1.0.zip) and unzip it.
2. Place `krita-stable-diffusion` folder into Krita plugins folder (usually `~/.local/share/krita/pykrita`, if `~/.local/share/krita` exists but `pykrita` doesn't, then add it). You can find

### Setup the model and config file

1. [Download stable-diffusion-v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4)
2. Rename it to `model.ckpt` and place it into `krita_stable_diffusion/kritastablediffusiond`
3. Copy `krita_stable_diffusion/stablediffusion/configs/stable-diffusion/v1-inference.yaml` to `krita_stable_diffusion/stablediffusiond/`
 

### Create python environment

1. Create python env `conda env create -f environment.yaml`
2. Activate python env `conda activate kritastabeldiffusion`

### Install stable diffusiond 

`curl -s https://raw.githubusercontent.com/w4ffl35/stablediffusiond/feature/krita-plugin/install.sh | bash`

### Enable the plugin

1. Start Krita (or restart if it was running)
2. Enable the plugin in the settings `Settings > Configure Krita > Python Plugin Manager`

---

Your directory structure should look like this (assuming krita has a typical installation)

```
~/.local/share/krita/pykrita/
├── krita-stable-diffusion
│   ├── interface
│   ├── ...
│   └── stablediffusion
│   │   └── src
│   │       └── clip
│   │       └── taming-transformers
│   │       └── ...
│   │       └── src
│   │           └── ...
│   │           └── settings.py
│   │       └── ...
│   │       └── model.ckpt
│   │       └── ...
│   │       └── v1-inference.yaml
│   └── stablediffusiond
│   └── stablediffusiond
└── krita_stable_diffusion.py
└── ...
└── settings.py
```

Krita resources folder can be found under `Settings > Manage Resources` then click the `Open Resource Folder` button.

![img.png](img.png)

Enable the plugin from within the Python Plugin Manager

`Settings > Configure Krita > Python Plugin Manager`

![img_1.png](img_1.png)

## Tools

Tools contains a custom size property (512x512) and template (single layer, no background) 
for Stable Diffusion projects.

---

THIS PLUGIN IS UNDER ACTIVE DEVELOPMENT. NOTHING WORKS YET. BOOKMARK THIS PAGE AND KEEP AN EYE ON IT. MANY CHANGES WILL BE HAPPENING OVER THE NEXT WEEK.

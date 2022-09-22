# Krita Stable Diffusion

[See Releases for download link](https://github.com/w4ffl35/krita_stable_diffusion/releases)

A Krita plugin for Stable Diffusion.

- Run Stable Diffusion locally in Krita without the need for a Python environment.
- **Easy installation: no need to install Python, no need to install dependencies**
- Non-blocking image generation: continue working in Krita while your images generate
- No need for webui or a webserver at all
- Ability to enqueue multiple requests, allowing you to generate multiple prompts and come back to see them after
- NSFW toggle

This is a brand new plugin. There are undocumented issues. Some of the problems you may encounter:

- Crashes
- Threads that did not close correctly
- Not all Stable Diffusion features have been implemented yet
- Other unexpected behavior

Some of the things we are working towards:

- Implementation of all Stable Diffusion features
- Improved UX
- Improved Installation process
- The ability to use the plugin with online services
- More!

---

## Installation

1. [Download and unzip the latest release from github](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.2.0/krita_stable_diffusion-0.2.0.zip)
2. Move the contents of the PLUGIN folder into your pykrita folder `/home/USER/.local/share/krita/pykrita/`
```
~/.local/share/krita/pykrita/
└── krita-stable-diffusion
    ├── krita-stable-diffusion
    └── Krita Stable Diffusion Plugin
```
3. Move the stablediffusion folder to your home directory `/home/$USER/stablediffusion/`
4. [Download the Stable Diffusion model](https://huggingface.co/CompVis/stable-diffusion-v1-4)
5. Rename it to `model.ckpt` and place it into `/home/$HOME/stablediffusion/models/ldm/stable-diffusion-v1/model.ckpt`
```
~/stablediffusion/
├── configs
├── img2img
├── models
│   └── ldm
│       └── stable-diffusion-v1
│           └── model.ckpt
└── txt2txt
```

### Krita resources folder

If your Krita resources folder is not where you expect to find it, you open Krita
and go to **`Settings > Manage Resources` then click the `Open Resource Folder` button.**

![img.png](img.png)

---

## Enable the plugin

![img_1.png](img_1.png)

You may need to restart Krita.

---

### System requirements

This plugin will run on a variety of systems. As it is tested the results will
be listed below.

If you have a different system than the one listed below, [please post your 
results in this discussion thread](https://github.com/w4ffl35/krita_stable_diffusion/discussions/16).


| OS |    GPU    |      CPU      | HD Space | RAM | Krita | Cuda Drivers |
|:---:|:---------:|:-------------:|:---------:|:---:|:-----:|:------------:|
| Ubuntu 20.04 | RTX 2080s | Ryzen 7 2700x | 20gb | 32GB | 4.2.9 |     11.3     |

---



Please post your results on the [stablediffusiond discussion board](https://github.com/w4ffl35/stablediffusiond/discussions).

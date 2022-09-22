# Krita Stable Diffusion

[![Download Plugin](https://img.shields.io/static/v1?label=Plugin&message=Download&color=00aa00&style=for-the-badge&logo=github&logoColor=white&link=)](https://drive.google.com/file/d/183KKC-t-4eyKrU2g2F4kUW_Hya-nATaU/view)
[![Download Krita](https://img.shields.io/static/v1?label=Krita&message=Download&color=00aa00&style=for-the-badge&logoColor=white&link=)]([https://drive.google.com/file/d/183KKC-t-4eyKrU2g2F4kUW_Hya-nATaU/view](https://krita.org/en/download/krita-desktop/))
[![Discord](https://img.shields.io/discord/839511291466219541?color=5865F2&logo=discord&logoColor=white&style=for-the-badge)](https://discord.com/channels/839511291466219541/1022298294338191381)

![GitHub](https://img.shields.io/github/license/w4ffl35/krita_stable_diffusion)
![GitHub all releases](https://img.shields.io/github/downloads/w4ffl35/krita_stable_diffusion/total)
![GitHub last commit](https://img.shields.io/github/last-commit/w4ffl35/krita_stable_diffusion)
![GitHub issues](https://img.shields.io/github/issues/w4ffl35/krita_stable_diffusion)
![GitHub closed issues](https://img.shields.io/github/issues-closed/w4ffl35/krita_stable_diffusion)
![GitHub pull requests](https://img.shields.io/github/issues-pr/w4ffl35/krita_stable_diffusion)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/w4ffl35/krita_stable_diffusion)

---

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

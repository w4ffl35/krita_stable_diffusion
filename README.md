# Krita Stable Diffusion

[![test](https://img.shields.io/static/v1?label=Download&message=Download&color=00aa00&style=for-the-badge&logo=github&logoColor=white&link=)](https://drive.google.com/drive/folders/16em41HpWOjnLRlYlKgJ2adyJ16CQ937H)
[![Discord](https://img.shields.io/discord/839511291466219541?color=5865F2&logo=discord&logoColor=white&style=for-the-badge)](https://discord.com/channels/839511291466219541/1022298294338191381)

![GitHub](https://img.shields.io/github/license/w4ffl35/krita_stable_diffusion)
![GitHub all releases](https://img.shields.io/github/downloads/w4ffl35/krita_stable_diffusion/total)
![GitHub last commit](https://img.shields.io/github/last-commit/w4ffl35/krita_stable_diffusion)
![GitHub issues](https://img.shields.io/github/issues/w4ffl35/krita_stable_diffusion)
![GitHub closed issues](https://img.shields.io/github/issues-closed/w4ffl35/krita_stable_diffusion)
![GitHub pull requests](https://img.shields.io/github/issues-pr/w4ffl35/krita_stable_diffusion)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/w4ffl35/krita_stable_diffusion)

---

![img_3.png](img_3.png)

- Run Stable Diffusion locally in Krita without the need for a Python environment.
- **Easy installation: no need to install Python, no need to install dependencies**
- Non-blocking image generation: continue working in Krita while your images generate
- No need for webui or a webserver at all
- Ability to enqueue multiple requests, allowing you to generate multiple prompts and come back to see them after
- NSFW toggle

---

## Installation

1. [Download and unzip the latest release from github](https://drive.google.com/drive/folders/16em41HpWOjnLRlYlKgJ2adyJ16CQ937H)
2. Unzip
3. Run the install script `~/krita_stable_diffusion-0.2.1/install.sh`
4. Follow the prompts to download the model (requires hugging face account)
5. Start Krita and enable the plugin

Provided you have a standard Krita installation everything should work as
expected. Your directory stucture for the plugin should look like this:

```
~/.local/share/krita/pykrita/
└── krita-stable-diffusion
    ├── krita-stable-diffusion
    └── Krita Stable Diffusion Plugin
```

You stablediffusion home directory should look like this: 

```
~/stablediffusion/
├── configs
├── img2img
├── licenses
├── models
│   └── ldm
│       └── stable-diffusion-v1
│           └── model.ckpt
└── txt2img
└── stablediffusiond.log
```

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
| Ubuntu 20.04 | RTX 2080s | Ryzen 7 2700x | 20gb | 32GB | 5.1.1 |    11.3*     |

* Cuda drivers may not be required, but are recommended.

---

Please post your results on
the [stablediffusiond discussion board](https://github.com/w4ffl35/stablediffusiond/discussions).

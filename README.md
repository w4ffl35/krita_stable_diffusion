# Krita Stable Diffusion

[![Windows](https://img.shields.io/static/v1?label=Download&message=Download&color=00aa00&style=for-the-badge&logo=windows&logoColor=white&link=)](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.3.0-alpha/krita-stable-diffusion-windows-0.3.0-alpha.tar.xz)
[![Linux](https://img.shields.io/static/v1?label=Download&message=Download&color=00aa00&style=for-the-badge&logo=linux&logoColor=white&link=)](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.2.2-alpha/krita-stable-diffusion_multifile-0.2.2.tar.xz)
[![Discord](https://img.shields.io/discord/839511291466219541?color=5865F2&logo=discord&logoColor=white&style=for-the-badge)](https://discord.com/channels/839511291466219541/1022298294338191381)

![GitHub](https://img.shields.io/github/license/w4ffl35/krita_stable_diffusion)
![GitHub all releases](https://img.shields.io/github/downloads/w4ffl35/krita_stable_diffusion/total)
![GitHub last commit](https://img.shields.io/github/last-commit/w4ffl35/krita_stable_diffusion)
![GitHub issues](https://img.shields.io/github/issues/w4ffl35/krita_stable_diffusion)
![GitHub closed issues](https://img.shields.io/github/issues-closed/w4ffl35/krita_stable_diffusion)
![GitHub pull requests](https://img.shields.io/github/issues-pr/w4ffl35/krita_stable_diffusion)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/w4ffl35/krita_stable_diffusion)

---

![img_3.png](src/img_3.png)

- Runs on Windows 11 and Ubuntu 20.04
- Run Stable Diffusion locally in Krita without the need for a Python environment.
- **Easy installation: no need to install Python, no need to install dependencies (**cuda 11.3 drivers may be required**)**
- Non-blocking image generation: continue working in Krita while your images generate
- No need for webui or a webserver at all
- Ability to enqueue multiple requests, allowing you to generate multiple prompts and come back to see them after
- NSFW toggle

---

## Getting started

### Download Krita

Download and install the latest version of Krita from [krita.org](https://krita.org/en/download/krita-desktop/)

![img.png](img.png)

### Download the Stable Diffusion plugin

### [Windows](#windows)

The Windows installer will download the model, but you need a [Huggingface.co](https://huggingface.co/join) account to do so.

When you run the installer script, you will be asked to enter your hugging face credentials. 
It is recommended that you first sign up for a hugging face account, then following the remaining steps if you would like to download the model using the installer.

Otherwise, you can download the model and set it up manually.

[![Windows](https://img.shields.io/static/v1?label=Download&message=Windows&color=0044cc&style=for-the-badge&logo=windows&logoColor=white&link=)](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.3.0-alpha/krita-stable-diffusion-windows-0.3.0-alpha.tar.xz)

1. [Download the latest release](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.3.0-alpha/krita-stable-diffusion-windows-0.3.0-alpha.tar.xz)
2. Unzip it ``
3. Double click `install.bat`
4. Follow the prompts

### Enable the plugin

1. After installing, start or restart Krita
2. Enable the plugin
3. Restart Krita again

### Linux

[![Linux](https://img.shields.io/static/v1?label=Download&message=Linux&color=44aa00&style=for-the-badge&logo=linux&logoColor=white&link=)](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.2.2-alpha/krita-stable-diffusion_multifile-0.2.2.tar.xz)


1. [Download the latest release](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/0.2.2-alpha/krita-stable-diffusion_multifile-0.2.2.tar.xz)
2. Unzip it `tar -xf krita-stable-diffusion_multifile-0.2.2.tar.xz`
3. Change into the correct directory `cd plugin_dist/0.2.2/krita-stable-diffusion_multifile-0.2.2`
4. Run install script `./install`
5. Follow the prompts to download the model if you don't have it already (requires hugging face account)

---

[REQUIRES CUDA 11.3 DRIVERS](https://developer.nvidia.com/cuda-11.3.0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=Ubuntu&target_version=20.04&target_type=runfile_local)

You must manually install the drivers. This step will be added to the installation script in version 0.2.3

If you are on Ubuntu 20.04 it is recommended that you use the runfile.

```
wget https://developer.download.nvidia.com/compute/cuda/11.3.0/local_installers/cuda_11.3.0_465.19.01_linux.run
sudo sh cuda_11.3.0_465.19.01_linux.run
```

![image](https://user-images.githubusercontent.com/25737761/192189958-ca9d1587-263d-4d13-b67f-2fb66bf00451.png)


---

Start Krita and enable the plugin.

If you have difficulty finding the model, [look at the FAQ](https://github.com/w4ffl35/krita_stable_diffusion/wiki/FAQ).

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

![img_1.png](src/img_1.png)

You may need to restart Krita.

---

## Uninstall

1. `./plugin_dist/0.2.2/krita-stable-diffusion_multifile-0.2.2/uninstall`
2. Follow the prompts

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
the [discussion board](https://github.com/w4ffl35/krita_stable_diffusion/discussions).

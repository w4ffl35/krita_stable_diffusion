# Krita Stable Diffusion

[![Discord](https://img.shields.io/discord/839511291466219541?color=5865F2&logo=discord&logoColor=white)](https://discord.gg/PUVDDCJ7gz)
![GitHub](https://img.shields.io/github/license/w4ffl35/krita_stable_diffusion)
![GitHub all releases](https://img.shields.io/github/downloads/w4ffl35/krita_stable_diffusion/total)
![GitHub last commit](https://img.shields.io/github/last-commit/w4ffl35/krita_stable_diffusion)
![GitHub issues](https://img.shields.io/github/issues/w4ffl35/krita_stable_diffusion)
![GitHub closed issues](https://img.shields.io/github/issues-closed/w4ffl35/krita_stable_diffusion)
![GitHub pull requests](https://img.shields.io/github/issues-pr/w4ffl35/krita_stable_diffusion)
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed/w4ffl35/krita_stable_diffusion)

---

## Download the Stable Diffusion plugin

- [Download the latest version](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/1.0.0/krita_stable_diffusion.zip) of the plugin
- [Use the Python Plugins Manager](https://docs.krita.org/en/user_manual/python_scripting/install_custom_python_plugin.html) to install the plugin from within Krita
- [Download the model downloader script](https://github.com/w4ffl35/krita_stable_diffusion/releases/download/1.0.0/download_models.sh)
- To download models into `~/stablediffusion` run `./download_models.sh`

## Download runai socket server

[![Linux](https://img.shields.io/static/v1?label=Download&message=Download&color=00aa00&style=for-the-badge&logo=linux&logoColor=white&link=)](https://github.com/w4ffl35/run-ai-socket-server/releases/download/v1.0.0/runai.tar.xz)

- unzip and untar the xz file - you should have a folder called `runai`
- run the server: `cd runai && ./runai`

**Windows download coming soon**

---

![image](https://user-images.githubusercontent.com/25737761/210693732-004dc2f7-d496-4ad2-8c27-c74a28459901.png)

- Runs on ~~Windows and~~ Ubuntu (Windows version coming soon)
- Run locally in Krita without the need for a Python environment.
- **Easy installation: no need to install Python or other dependencies**
- Non-blocking image generation: continue working in Krita while your images generate
- Moves images from server to Krita without moving to disc first
- ~Standalone - comes bundled with required server~ Coming soon - currently have to download and run server separately
- Uses a queued request system
- Runs Stable Diffusion models v1-5 and 2-1
- Runs any diffusers or ckpt models

### Image generation features
- NSFW toggle
- No watermarking
- **Txt2Img**: create images from text prompts
- **Img2img**: create images from existing images and text prompts
- **Inpainting**: replace masked areas of images using prompts
- **Outpainting**: expand an existing image using prompts
- **Checkpoint conversion**: convert ckpt to diffusers format

---

### Update the plugin

Requires manual update for now (re-follow installation steps)

**Automatic updates under development**

---

[![Discord](https://img.shields.io/discord/839511291466219541?color=5865F2&logo=discord&logoColor=white&style=for-the-badge)](https://discord.gg/PUVDDCJ7gz)

Join us on Discord

---

# Krita Stable Diffusion

A Krita plugin for Stable Diffusion

https://www.youtube.com/watch?v=maWR7dDf4SE

## Installation

1. Download the latest release from the releases page
2. Unzip it
3. Acquire model and place into `/stablediffusiond`
4. Copy or link `v1-inference.yaml` into `/stablediffusiond`
5. Follow installation instructions in README.md in `/stablediffusion` and `/stablediffusiond`
6. Place `krita-stable-diffusion` folder into Krita plugins folder (usually `~/.local/share/krita/pykrita`, if `~/.local/share/krita` exists but `pykrita` doesn't, then add it). You can find 
7. Start Krita (or restart if it was running)
8. Enable the plugin in the settings `Settings > Configure Krita > Python Plugin Manager`

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
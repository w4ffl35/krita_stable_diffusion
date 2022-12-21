APPLICATION_ID = "krita_stable_diffusion"
SCHEDULERS = [
    "euler_a",
    "euler",
    "ddpm",
    "ddim",
    "plms",
    "lms",
    "dpm"
]
UPSCALERS = ["None", "Lanczos"]
MODELS = {
    "v1": [
        "runwayml/stable-diffusion-v1-5",
        "runwayml/stable-diffusion-inpainting",
    ],
    "v2": [
        "stabilityai/stable-diffusion-2-1-base",
        "stabilityai/stable-diffusion-x4-upscaler",
        "stabilityai/stable-diffusion-2-inpainting",
        "stabilityai/stable-diffusion-2-depth",
    ]
}
DEFAULT_MODEL = MODELS["v2"][0]
DEFAULT_SCHEDULER = SCHEDULERS[0]
MIN_SEED = 0
MAX_SEED = 4294967295
